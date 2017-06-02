#!/usr/bin/env python

import json

global data, idsWithData

def main():
    global data, idsWithData
    
    with open("remix_recursively_scraped.json") as infile:
        data = json.load(infile)
    
    # First we run the analyze_max_depth.py script on the same data
    # This gives us a couple of candidates that would be interesting to
    # draw a network graph for because it contains the most nested childs
    # or parents.
    #
    # This analysis resulted in the conclusion that drawing a graph where
    # children are followed contains more levels of decendants than doing
    # the same with parents would.
    # Also this analysis shows that there are three possible starting points
    # which could create an interesting graph.
    # 
    # We just try to create the nested data structure from the first one:
    initialId = "43961"
    
    # Create a list of IDs from the data, so we know which IDs have actual track data
    idsWithData = [t["id"] for t in data]
    
    nestedData = insertChildren([initialId], 10)
    print nestedData

    # Save the nested data
    filename = "nested_child_structure_from_{}.json".format(initialId)
    with open(filename, 'w') as outfile:
        json.dump(nestedData, outfile, indent=2)
    
        
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
                if child in idsWithData:
                    children = insertChildren(findChildren(child), depth)
                    childDict = {}
                    trackData = dataWithId(child)
                    childDict["id"] = child
                    keys = ["artist", "bpm", "track"]
                    for k in keys:
                        childDict[k] = trackData[k]
                    childDict["children"] = children
                    newList.append(childDict)
                else:
                    print "track '{}' encountered in tree, skipped because it has no data".format(child)    
            else:
                print "no id str", child
        return newList
    return nested

def dataWithId(fromId):
    global data, idsWithData
    if fromId in idsWithData:
        for track in data:
            if track["id"] == fromId:
                return track 
    return None

def findChildren(fromId):
    global data, idsWithData
    for track in data:
        if track["id"] == fromId:
            return [str(c) for c in track["children"]]
    return []


if __name__ == '__main__':
    main()