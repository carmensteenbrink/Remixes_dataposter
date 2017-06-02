#!/usr/bin/env python

import urllib2
import json

idsWithErrors = []

def main():
    # Read the json file as json
    filename = "remixes_just_one.json"
    with open(filename, "r") as infile:
        remixes = json.load(infile)
    
    newRemixes = []
    
    print "Scraping recursively from {}".format(filename)
    print "Initial pass contains {} remixes".format(len(remixes))
    
    for i, remixData in enumerate(remixes):
        # The id is the last part of the file_page_url
        id = remixData["file_page_url"].split('/')[-1]
        remix = scrape_track(id)
        # Check if we actually got a valid remix back
        if remix:
            print "parsed remix {:3d}: {}".format(i, remix)
            newRemixes.append(remix)
    
    missing = missingIds(newRemixes)
    print "After initial pass: {} tracks missing".format(len(missing)) 
    
    maxRecursion = 6
    iteration = 2
    
    while(len(missing) > 0 and iteration < maxRecursion):
        print "======= Iteration {} : Processing {} missing =======".format(iteration, len(missing))
        for i, missingId in enumerate(missing):
            # The id is the last part of the file_page_url
            id = missingId
            remix = scrape_track(id)
            # Check if we actually got a valid remix back
            if remix:
                print "extra remix {:3d}: {}".format(i, remix)
                newRemixes.append(remix)
        missing = missingIds(newRemixes)
        iteration += 1
    
    outfilename = "remix_recursively_scraped.json"
    with open(outfilename, "w") as outfile:
        json.dump(newRemixes, outfile, indent=2, sort_keys=True)
        
    print "----------------"
    print "{} ids gave an error: {}".format(len(idsWithErrors), idsWithErrors)


def missingIds(data):
    trackIds = [t["id"] for t in data]
    missingTracks = []

    # Walk through all tracks
    for track in data:
        # Walk through all parents
        for parent in track["parents"]:
            if not parent in trackIds:
                missingTracks.append(str(parent))
        # Walk through all children
        for child in track["children"]:
            if not child in trackIds:
                missingTracks.append(str(child))
                
    # Exclude the ids with errors
    return filter(lambda id: id not in idsWithErrors, missingTracks)


def scrape_track(id):
    url = "http://ccmixter.org/api/query?f=json&t=info&ids="+id
    site = urllib2.urlopen(url).read()
    try:
        alldata = json.loads(site.decode("utf-8", "ignore"))
    except ValueError:
        print "Error parsing as json in {}".format(id)
        idsWithErrors.append(id)
        return None
    try:
        data = alldata[0]
    except IndexError:
        print "data has no index 0:", alldata
        idsWithErrors.append(id)
        return None
    
    upload_id = id
    user_name = data['user_name']
    bpm = data['upload_extra']['bpm']
    upload_name = data['upload_name']
    remix_parents = []
    if data.has_key('remix_parents'):
        for parent in data['remix_parents']:
            if parent.has_key('upload_id'):
                remix_parents.append(parent['upload_id'])
            elif parent.has_key('pool_item_id'):
                remix_parents.append(parent['pool_item_id'])
    remix_children = []
    if data.has_key('remix_children'):
        for child in data['remix_children']:
            if child.has_key('upload_id'):
                remix_children.append(child['upload_id'])
            elif child.has_key('pool_item_id'):
                remix_children.append(child['pool_item_id'])
            
    # Create a new dict for this remix
    remix = {}
    remix['id'] = upload_id
    remix['artist'] = user_name
    remix['bpm'] = bpm
    remix['track'] = upload_name
    remix['children'] = remix_children
    remix['parents'] = remix_parents
    
    # Return this simple dict
    return remix

if __name__ == '__main__':
    main()