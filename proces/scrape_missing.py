#!/usr/bin/env python

import urllib2
import json

def main():

    # Read the json file as json
    filename = "missing_ids.json"
    with open(filename, "r") as infile:
        missing = json.load(infile)
    
    newRemixes = []
    
    print "Processing {} missing tracks in {}".format(len(missing), filename)
    
    for i, id in enumerate(missing):
        
        remix = filter_json(str(id))
        # Check if we actually got a valid remix back
        if remix:
            print "parsed remix {:3d}: {}".format(i, remix)
            newRemixes.append(remix)
    
    outfilename = "extra_tracks.json"
    with open(outfilename, "w") as outfile:
        json.dump(newRemixes, outfile, indent=2, sort_keys=True)


def filter_json(id):
    url = "http://ccmixter.org/api/query?f=json&t=info&ids="+id
    site = urllib2.urlopen(url).read()
    try:
        alldata = json.loads(site.decode("utf-8", "ignore"))
    except ValueError:
        print "Error parsing as json:"
        print site
        return None
    try:
        data = alldata[0]
    except IndexError:
        print "data has no index 0:"
        print alldata
        return None
    
    upload_id = id
    user_name = data['user_name']
    bpm = data['upload_extra']['bpm']
    upload_name = data['upload_name']
            
    # Create a new dict for this remix
    remix = {}
    remix['id'] = upload_id
    remix['artist'] = user_name
    remix['bpm'] = bpm
    remix['track'] = upload_name
    
    # Return this simple dict
    return remix

if __name__ == "__main__":
    main()
    
    