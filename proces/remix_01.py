import urllib2
import json

def main():

    # Read the json file as json
    filename = "remixes_jan2016_dec2016.json"
    with open(filename, "r") as infile:
        remixes = json.load(infile)
    
    newRemixes = []
    
    print "Processing {} remixes in {}".format(len(remixes), filename)
    
    for i, remixData in enumerate(remixes):
        # The id is the last part of the file_page_url
        id = remixData["file_page_url"].split('/')[-1]
        remix = filter_json(id)
        # Check if we actually got a valid remix back
        if remix:
            print "parsed remix {:3d}: {}".format(i, remix)
            newRemixes.append(remix)
    
    outfilename = "remix_links.json"
    with open(outfilename, "w") as outfile:
        json.dump(newRemixes, outfile, indent=2, sort_keys=True)
'''
[
  {
    "artist_page_url": "http://ccmixter.org/people/JeffSpeed68",
    "file_page_url": "http://ccmixter.org/files/JeffSpeed68/52942",
    "files": [
      {
        "download_url": "http://ccmixter.org/content/JeffSpeed68/JeffSpeed68_-_Loaded_with_Vitriol.mp3",
        "file_extra": {
          "sha1": "I5QQRMLJEYTTD7RUC2OW3ZZOKI2XHFU2"
        },
        "file_filesize": " (12.38MB)",
        "file_format_info": {
          "br": "CBR",
'''

def filter_json(id):
    url = "http://ccmixter.org/api/query?f=json&t=info&ids="+id
    site = urllib2.urlopen(url).read()
    alldata = json.loads(site.decode("utf-8", "ignore"))
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


    '''
    data =  json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
    data = data.split("\n")
    
    user_name = ""
    bpm = ""
    upload_name = ""
    remix_parents = ""
    remix_children = ""
    
    #for line in data:
    for idx, line in enumerate(data):
        print line
        if "user_name" in line:
            user_name = line.split('"')[3]
        if "\"bpm\"" in line:
            bpm = line.split(':')[1][:-1]
        if "upload_name" in line:
            upload_name = line.split('"')[-2]
        if "remix_parents" in line:
            remix_parents = line.split('"')[1]
            #print ">>>>"+data[idx+1]
            #print remix_parents
    '''

if __name__ == "__main__":
    main()