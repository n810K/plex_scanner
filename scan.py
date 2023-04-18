import requests
import urllib
import json
import os.path
import shutil
import datetime
import time

def setupConfig():
    if (not os.path.exists("config.json")):
        shutil.copy("config/configDefault.json", "config.json")
    
    if (not os.path.exists("lastid.json")):
        shutil.copy("config/idDefault.json", "lastID.json")

def plexscan(section, paths, plexInfo):
    plexhost = plexInfo["plexhost"]
    plexport = plexInfo["plexport"]
    plextoken = plexInfo["plex-token"]
    plexsection = plexInfo["sections"][section]

    for path in paths:
        url = requests.get(f"{plexhost}:{plexport}/library/sections/{plexsection}/refresh?path={urllib.parse.quote(path)}&X-Plex-Token={plextoken}").status_code
        print(path, "code:", url)
        time.sleep(1)

def getRadarrPaths(urlData,lastID, variant):
    radarrhost = urlData["radarrhost"]
    radarrAPI = urlData["radarrAPI"]

    #Limit to 1 week back, to not have a massive list of items to sort through
    today = datetime.datetime.now()
    daysAgo = (today - datetime.timedelta(days=7)).date()

    if (variant == "movies"):
        radarrAPI = urlData["radarrAPI"]
        url = requests.get(f"{radarrhost}/radarr/api/v3/history/since?date={daysAgo}&includeMovie=false&apikey={radarrAPI}", verify=False).json()
    elif (variant == "4k-movies"):
        radarr4kAPI = urlData["radarr4kAPI"]
        url = requests.get(f"{radarrhost}/radarr4k/api/v3/history/since?date={daysAgo}&includeMovie=false&apikey={radarr4kAPI}", verify=False).json()

    moviePaths = []
    newID = lastID
    for movie in url:
        if movie["id"] > lastID:
            if (movie["data"].get("importedPath") != None):
                fullMoviePath = (movie["data"].get("importedPath"))
                lastSlashIndex = fullMoviePath.rfind("/")
                trimmedPath = fullMoviePath[:lastSlashIndex+1]
                moviePaths.append(trimmedPath)
                if movie["id"] > newID:
                    newID = movie["id"]

    #remove duplicates
    moviePaths = set(moviePaths)
    return moviePaths, newID


def main():

    setupConfig()

    with open("config.json") as jsonConfig:
        data = json.load(jsonConfig)

    with open('lastid.json') as lastidfile:
        lastID = json.load(lastidfile)

    sectionList = []
    for section in data["sections"]:
        sectionList.append(section)

    librarySelection = input(f"Which library would you like to scan? {sectionList}: ")
    while (librarySelection not in sectionList):
        print("Invalid Selection:")
        librarySelection = input(f"Which library would you like to scan? {sectionList}: ")

    if (librarySelection == "movies"):
        moviePaths, updatedID = getRadarrPaths(data, lastID["radarr"], "movies")

        #Update lastid json to be the last processed item
        lastID["radarr"] = updatedID
        with open('lastid.json', 'w') as lastidfile:
            json.dump(lastID, lastidfile)

        plexscan(librarySelection, moviePaths, data)

    if (librarySelection == "4k-movies"):
        moviePaths, updatedID = getRadarrPaths(data, lastID["radarr4k"], "4k-movies")
        
        lastID["radarr4k"] = updatedID
        with open('lastid.json', 'w') as lastidfile:
            json.dump(lastID, lastidfile)

        plexscan(librarySelection, moviePaths, data)

    

if __name__ == "__main__":
    main()