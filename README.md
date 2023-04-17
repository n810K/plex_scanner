# plex_scanner (WIP)

## A Plex to work with the *Arrs 

Plex is unable to properly track which folders have been updated on a Google Drive mount. This is a tool to manually scan any files that have been recently changed through the *Arrs, using Plex Server URL Commands.

Currently, only Radarr is implemented. Sonarr support will be added later.

## Setup

Modify "config.json" with the appropriate information. 

Refer to [https://support.plex.tv/articles/201638786-plex-media-server-url-commands/](Plex Server Url Commands) to get any missing information for config.json.

Modify `sections` as needed, it can look like:

```    "sections":{
        "movies": "1",
        "4k-movies": "2",
        "tv": "3",
        "4k-tv": "4"
    }```
