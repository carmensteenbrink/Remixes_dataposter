#!/usr/bin/env python

import json

global data

def main():
    global data
    
    with open("remix_recursively_scraped.json") as infile:
        data = json.load(infile)
    
    # fill just the first element
    initial = data[0]
    
    # Follow the children recursively
    nestedData = insertChildren([initial["id"]], 5)
    print nestedData
    
    deepchild = ["53273"]
    nestedData = insertParents(deepchild, 5)
    print nestedData
    
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