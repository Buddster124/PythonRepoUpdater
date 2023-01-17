# Python Repo Updater
# Description
  This python script will check for updates on a github repo and automaticly download the latest version.

# Requirements
- Python 3
- GitPython

# Tested Systems
| OS  | Status |
| ------------- | ------------- |
| Linux (Debian Based System)  | :heavy_check_mark: |
| Windows | (Untested but should work) |

# How to use
 1. Create a file called ```Version``` in your github repo, and put the version number in the file. ex: ```1.0.0```
 2. Edit the user vars in ```Update.py```
 3. You are done.

# Notes
- Files do not have to be hosted on github, If you are self-hosting your own ```gitlab, gittea, etc``` instance. This script will work for them as well.
- This script checks the ```Version``` file in the repo and compares it against the local ```Version``` file, to determine if there is an update. 
