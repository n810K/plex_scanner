# plex_scanner

## A Plex Scanner to work with Sonarr/Radarr

Plex is unable to properly track which folders have been updated on a Google Drive mount. This is a tool to manually scan any files that have been recently changed through the *Arrs, using Plex Server URL Commands.

## Setup

Modify "config.json" with the appropriate information. 

Refer to [Plex Server URL Commands](https://support.plex.tv/articles/201638786-plex-media-server-url-commands/) to get any missing information for config.json.

Modify `sections` as needed, it can look like:

```    
"sections":{
        "movies": "1",
        "4k-movies": "2",
        "tv": "3",
        "4k-tv": "4"
    }
```

API keys are stored in plaintext
