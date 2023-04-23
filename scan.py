import requests
import json
import os.path
import shutil
import datetime
import time

requests.packages.urllib3.disable_warnings() 

def setupConfig():
    if (not os.path.exists("config.json")):
        shutil.copy("config/configDefault.json", "config.json")
    if (not os.path.exists("lastid.json")):
        shutil.copy("config/idDefault.json", "lastID.json")

def plexscan(paths, plexInfo, variant):
    plexhost = plexInfo["plexhost"]
    plexport = plexInfo["plexport"]
    plextoken = plexInfo["plex-token"]
    plexsectionID = plexInfo["sections"][variant]

    for path in paths:
        statusCode = requests.get(f"{plexhost}:{plexport}/library/sections/{plexsectionID}/refresh?path={path}&X-Plex-Token={plextoken}").status_code
        if (statusCode != 200):
            print("ERROR:", path, "code:", statusCode)
        else:
            print(path, "code:", statusCode)
        time.sleep(0.5)

    
def getArrPaths(lastIDJson, configJson, variant):
    mappedArrVariant = configJson["mappings"][variant]
    arrHost = configJson["arrhost"]
    arrAPI = configJson["APIs"][variant]
    lastID = lastIDJson[mappedArrVariant]

    if ("radarr" in mappedArrVariant.lower()):
        mediaType = "Movie"
    elif ("sonarr" in mappedArrVariant.lower()):
        mediaType = "Series"

    #Limit to 1 week back, to not have a massive list of items to sort through
    today = datetime.datetime.now()
    daysAgo = (today - datetime.timedelta(days=7)).date()
    url = requests.get(f"{arrHost}/{mappedArrVariant}/api/v3/history/since?date={daysAgo}&include{mediaType}=false&apikey={arrAPI}", verify=False).json()
    mediaPaths = []
    newID = lastID
    for media in url:
        if media["id"] > lastID:
            if (media["data"].get("importedPath") != None or media["data"].get("path") != None):
                fullMediaPath = (media["data"].get("importedPath") or media["data"].get("path"))
                lastSlashIndex = fullMediaPath.rfind("/")
                trimmedPath = fullMediaPath[:lastSlashIndex+1].replace("&", "%26")
                mediaPaths.append(trimmedPath)
                if media["id"] > newID:
                    newID = media["id"]

    lastIDJson[mappedArrVariant] = newID
    with open('lastid.json', 'w') as lastIDFile:
        json.dump(lastIDJson, lastIDFile)

    #remove duplicates
    mediaPaths = sorted(set(mediaPaths))
    return mediaPaths

def main():
    setupConfig()

    with open("config.json") as jsonConfig:
        configData = json.load(jsonConfig)
    with open('lastid.json') as lastidfile:
        lastIDData = json.load(lastidfile)

    sectionList = []
    for section in configData["sections"]:
        sectionList.append(section)

    librarySelection = input(f"Which library would you like to scan? {sectionList}: ")
    while (librarySelection not in sectionList and librarySelection!="all"):
        print("Invalid Selection:")
        librarySelection = input(f"Which library would you like to scan? {sectionList}: ")
    
    if (librarySelection == "all"):
        for item in sectionList:
            librarySelection = item
            mediaPaths = getArrPaths(lastIDData, configData, librarySelection)
            plexscan(mediaPaths, configData, librarySelection)
    else:
        mediaPaths = getArrPaths(lastIDData, configData, librarySelection)
        plexscan(mediaPaths, configData, librarySelection)

if __name__ == "__main__":
    main()