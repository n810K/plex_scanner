import requests
import urllib
import json
import os.path
import shutil
import datetime

def plexscan(section, plexInfo, paths):
    plexhost = plexInfo["plexhost"]
    plexport = plexInfo["plexport"]
    plextoken = plexInfo["plex-token"]
    plexsection = plexInfo["sections"][section]
    for path in paths:
        url = requests.get(f"{plexhost}:{plexport}/library/sections/{plexsection}/refresh?path={urllib.parse.quote(path)}&X-Plex-Token={plextoken}").status_code
        print(url)

def getRadarrPaths(urlData,lastID):
    radarrhost = urlData["radarrhost"]
    radarrAPI = urlData["radarrAPI"]

    today = datetime.datetime.now()
    daysAgo = (today - datetime.timedelta(days=7)).date()
    
    url = requests.get(f"{radarrhost}/radarr/api/v3/history/since?date={daysAgo}&includeMovie=false&apikey={radarrAPI}", verify=False).json()
    moviePaths = []
    newID = 0
    for movie in url:
        if movie["movieId"] >= lastID:
            if (movie["data"].get("importedPath") != None):
                fullMoviePath = (movie["data"].get("importedPath"))
                lastSlashIndex = fullMoviePath.rfind("/")
                trimmedPath = fullMoviePath[:lastSlashIndex+1]
                moviePaths.append(trimmedPath)
                if movie["movieId"] > newID:
                    newID = movie["movieId"]

    return moviePaths, newID


def main():

    if (not os.path.exists("config.json")):
        shutil.copy("config/configDefault.json", "config.json")

    with open("config.json") as jsonConfig:
        data = json.load(jsonConfig)
    
    sectionList = []
    for section in data["sections"]:
        sectionList.append(section)

    librarySelection = input(f"Which library would you like to scan? {sectionList}: ")
    while (librarySelection not in sectionList):
        print("Invalid Selection:")
        librarySelection = input(f"Which library would you like to scan? {sectionList}: ")

    if (librarySelection == "movies"):
        moviePaths, newID = getRadarrPaths(data, newID)

        plexscan(librarySelection, data, moviePaths)

    



if __name__ == "__main__":
    main()