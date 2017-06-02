#!/usr/bin/env python

import json

global data

def main():
    global data
    
    with open("remix_recursively_scraped.json") as infile:
        data = json.load(infile)
    
    # fill just the first element
    initial = data[0]

    # Find track with highest parent
    trackWithParentLevels = []
    for t in data:
        trackId = t["id"]
        thisLevel = findParents(trackId)
        for i in range(10):
            if len(thisLevel) < 1:
                track = {}
                track["id"] = trackId
                track["parentDepth"] = i
                trackWithParentLevels.append(track)
                break
            parents = []
            for c in thisLevel:
                parents += findParents(c)
            thisLevel = parents
            
    maxDepth = max([t["parentDepth"] for t in trackWithParentLevels])
    print maxDepth
    # There are some tracks with 3 levels of parents
    
    # Print those tracks
    candidates = []
    for t in trackWithParentLevels:
        if t["parentDepth"] == maxDepth:
            print t
            candidates.append(t["id"])
    # So there are three candidates with at least 3 level deep parents
    print candidates
    
    # Follow all the parents of these candidates
    for trackId in candidates:
        print "================ data for candidate : {} ================".format(trackId)
        nestedData = insertParents([trackId], 10)
        print nestedData
    
    
    # Do the same for children
    trackWithChildLevels = []
    for t in data:
        trackId = t["id"]
        thisLevel = findChildren(trackId)
        for i in range(10):
            if len(thisLevel) < 1:
                track = {}
                track["id"] = trackId
                track["childDepth"] = i
                trackWithChildLevels.append(track)
                break
            children = []
            for c in thisLevel:
                children += findChildren(c)
            thisLevel = children
            
    # Make the ids unique
    # (And only keep the highest child level)
    uniqueIds = []
    newChildLevels = []
    for t in trackWithChildLevels:
        thisId = t["id"]
        if thisId in uniqueIds:
            thisIndex = uniqueIds.index(thisId)
            foundDict = newChildLevels[thisIndex]
            if t["childDepth"] > foundDict["childDepth"]:
                foundDict["childDepth"] = t["childDepth"]
                newChildLevels[thisIndex] = foundDict
        else:
            uniqueIds.append(thisId)
            newChildLevels.append(t)
    trackWithChildLevels = newChildLevels
    
    maxDepth = max([t["childDepth"] for t in trackWithChildLevels])
    print maxDepth
    # There are some tracks with 3 levels of parents
    
    # Print those tracks
    candidates = []
    for t in trackWithChildLevels:
        if t["childDepth"] == maxDepth:
            print t
            candidates.append(t["id"])
    # So there are three candidates with at least 3 level deep parents
    print candidates
    
    # Follow all the parents of these candidates
    
    trackIDs = [t["id"] for t in data]
    
    for trackId in candidates:
        print "================ data for candidate : {} ================".format(trackId)
        nestedData = insertChildren([trackId], 10)
        # Count the tracks in this tree
        numTracks = len(flatIdList(nestedData))
        filteredTracks = []
        for tID in flatIdList(nestedData):
            if tID in trackIDs:
                filteredTracks.append(tID)
        numTracksWithData = len(filteredTracks)
        print "num of ids:", numTracks, "including title / artist data:", numTracksWithData
        print nestedData
        
def flatIdList(nestedData):
    flatList = []
    for t in nestedData:
        flatList.append(t["id"])
        if t["children"]:
            flatList += flatIdList(t["children"])
    return flatList
    
    
    # # Follow the children recursively
    # nestedData = insertChildren([initial["id"]], 10)
    # print nestedData
    #
    # deepchild = ["53273"]
    # nestedData = insertParents(deepchild, 10)
    # print nestedData
    
    # the nested structure can simply be ["12435"]
    # or [{"id": "12435", "children": ["67890", "09876"]}]
    # "children": [] indicates that there are no further children
def insertChildren(nested, depth):
    # Make sure it is not endlessly recursing
    if depth > 0:
        depth -= 1
        # Create a new list
        newList = []
        # Loop through all children
        for child in nested:
            # String or dict
            if type(child) == str or type(child) == unicode:
                children = insertChildren(findChildren(child), depth)
                childDict = {}
                childDict["id"] = child
                childDict["children"] = children
                newList.append(childDict)
            else:
                print "no id str", child
        return newList
    return nested

    # the nested structure can simply be ["12435"]
    # or [{"id": "12435", "children": ["67890", "09876"]}]
    # "children": [] indicates that there are no further children
def insertParents(nested, depth):
    # Make sure it is not endlessly recursing
    if depth > 0:
        depth -= 1
        # Create a new list
        newList = []
        # Loop through all children
        for parent in nested:
            # String or dict
            if type(parent) == str or type(parent) == unicode:
                parents = insertParents(findParents(parent), depth)
                parentDict = {}
                parentDict["id"] = parent
                parentDict["parents"] = parents
                newList.append(parentDict)
            else:
                print "no id str", parent
        return newList
    return nested
    

def findChildren(fromId):
    global data
    for track in data:
        if track["id"] == fromId:
            return [str(c) for c in track["children"]]
    return []

def findParents(fromId):
    global data
    for track in data:
        if track["id"] == fromId:
            return [str(p) for p in track["parents"]]
    return []


if __name__ == '__main__':
    main()