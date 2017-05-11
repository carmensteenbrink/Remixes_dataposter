import urllib2
import json

def main():

    filename = "remixes_jan2016_dec2016.json"
    file  = open(filename, "r")
    for line in file:
        if "file_page_url" in line:
            id = line.split('/')[-1][:-3]
            filter_json(id)
            
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
    alldata = json.loads(site)
    data = alldata[0]
    
    user_name = data['user_name']
    bpm = data['upload_extra']['bpm']
    upload_name = data['upload_name']
    if data.has_key('remix_parents'):
        remix_parents = data['remix_parents'][0]['upload_id']
    else:
        remix_parents = "---"
    remix_children = data['remix_children'][0]['upload_id']
    
    print user_name
    print bpm
    print upload_name
    print remix_children
    print remix_parents



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
