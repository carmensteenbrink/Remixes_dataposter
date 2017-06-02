#!/usr/bin/env python

import json

with open('remix_links.json') as infile:
    data = json.load(infile)
    
print "Scraped {} tracks in 2016".format(len(data))

# Analyze:
#   missing tracks (referenced, but not included)
#   most referenced as parent
#   most referenced as child

trackIds = [t["id"] for t in data]
missingTracks = []
parentFrequencies = {}
childFrequencies = {}

# Walk through all tracks
for track in data:
    # Walk through all parents
    for parent in track["parents"]:
        if not parent in trackIds:
            missingTracks.append(parent)
        if parentFrequencies.has_key(str(parent)):
            parentFrequencies[str(parent)] += 1
        else:
            parentFrequencies[str(parent)] = 1
    # Walk through all children
    for child in track["children"]:
        if not child in trackIds:
            missingTracks.append(child)
        if childFrequencies.has_key(str(child)):
            childFrequencies[str(child)] += 1
        else:
            childFrequencies[str(child)] = 1


# Print results
print "-------------------"
print "Missing {} tracks.".format(len(missingTracks))

print
print "Top 20 parent tracks:"
aux = [(parentFrequencies[k], k) for k in parentFrequencies]
aux.sort()
aux.reverse()
top = aux[:20]
for t in top:
    print "  {}: {}".format(t, t[1] in trackIds and "in data set" or "MISSING")
    
print
print "Top 20 child tracks:"
aux = [(childFrequencies[k], k) for k in childFrequencies]
aux.sort()
aux.reverse()
top = aux[:20]
for t in top:
    print "  {}: {}".format(t, t[1] in trackIds and "in data set" or "MISSING")


# Save missing ids in other json
with open('missing_ids.json', 'w') as outfile:
    json.dump(missingTracks, outfile)
