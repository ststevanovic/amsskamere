# About

_**MVP**_  
Get snapshoots from live feed. Store as Image slide preview.  


_**In its Wake**_   
Encode snapshoot to status label (cat.var.) - bussy, light, free.   
Follow averages (subscribed data usage)  


# Setup

In order to "write" poetry   
`curl -sSL https://install.python-poetry.org | python3 -`  

To use environment     
`poetry config virtualenvs.in-project true`  
`poetry install`  
`source .venv/bin/activate`  

# Pre-Run & Run (WIP):  
Note: At the moement needs full fledged Chrome, instead of chromium, so:
* Step1. `edit amsskamere/screenshots.py` and set chrome location (or choose OS -defualt location)
* Step2. `python amsskamere/screenshots.py` 

# Requirements [wip]
google-chrome-stable_current_amd64.deb - for selenium, but lets try something else...
