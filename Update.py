#!/usr/bin/python3
# ==============================================================================================================================================
#    ____        __  __                   ____                      __  __          __      __           
#   / __ \__  __/ /_/ /_  ____  ____     / __ \___  ____  ____     / / / /___  ____/ /___ _/ /____  _____
#  / /_/ / / / / __/ __ \/ __ \/ __ \   / /_/ / _ \/ __ \/ __ \   / / / / __ \/ __  / __ `/ __/ _ \/ ___/
# / ____/ /_/ / /_/ / / / /_/ / / / /  / _, _/  __/ /_/ / /_/ /  / /_/ / /_/ / /_/ / /_/ / /_/  __/ /    
#/_/    \__, /\__/_/ /_/\____/_/ /_/  /_/ |_|\___/ .___/\____/   \____/ .___/\__,_/\__,_/\__/\___/_/     
#      /____/                                   /_/                  /_/                                 
# ==============================================================================================================================================
# - Script Created By: Anthony Budd
# - Last Edit Date: 1/17/2023
# - Script Version: 1.0.0

# ==============================================================================================================================================
# Imports - Do Not Edit, Unless You Know What You Are Doing
# ==============================================================================================================================================
import os
import time
import shutil
import urllib.request
from time import sleep
from pathlib import Path
from git import Repo

# ==============================================================================================================================================
# User Vars - Edit These To Fit Your Use Case
# ==============================================================================================================================================
# - update_url is the direct url to the version file on github.
update_url = 'https://raw.githubusercontent.com/Buddster124/PythonRepoUpdater/main/Version'
# - update_repo is the git url.
update_repo = 'https://github.com/Buddster124/PythonRepoUpdater.git'
# - program_name is the name of the program you are updating, This Can Be Anything You Want.
program_name = 'Python Repo Updater'


# ==============================================================================================================================================
# Do Not Edit Below This Line, Unless You Know What You Are Doing.
# ==============================================================================================================================================

# Program Vars
cwd = os.getcwd()
current_user = os.environ.get('USER')

# File Functions
def forceMergeFlatDir(srcDir, dstDir):
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    for item in os.listdir(srcDir):
        srcFile = os.path.join(srcDir, item)
        dstFile = os.path.join(dstDir, item)
        forceCopyFile(srcFile, dstFile)

def forceCopyFile (sfile, dfile):
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)

def isAFlatDir(sDir):
    for item in os.listdir(sDir):
        sItem = os.path.join(sDir, item)
        if os.path.isdir(sItem):
            return False
    return True


def copyTree(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isfile(s):
            if not os.path.exists(dst):
                os.makedirs(dst)
            forceCopyFile(s,d)
        if os.path.isdir(s):
            isRecursive = not isAFlatDir(s)
            if isRecursive:
                copyTree(s, d)
            else:
                forceMergeFlatDir(s, d)


# Main Funtions
def GetCurrentVersion():
    txt = Path('Version').read_text()
    current_installed_version = txt    
    return current_installed_version


def GetLatestVersion():
    uf = urllib.request.urlopen(update_url)
    latest_version_url = uf.read()
    latest_version_url = str(latest_version_url)
    latest_version_url = latest_version_url.replace("b","")
    latest_version_url = latest_version_url.replace("'","")
    latest_version_url = latest_version_url.replace(" ","")
    #print(f'Latest Version On Github is: {latest_version_url}')
    return latest_version_url


# Return 1 if v2 is smaller,
# -1 if v1 is smaller,,
# 0 if equal
def versionCompare(v1, v2):
      
    # This will split both the versions by '.'
    arr1 = v1.split(".") 
    arr2 = v2.split(".") 
    n = len(arr1)
    m = len(arr2)
      
    # converts to integer from string
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]
   
    # compares which list is bigger and fills 
    # smaller list with zero (for unequal delimiters)
    if n>m:
      for i in range(m, n):
         arr2.append(0)
    if m>n:
      for i in range(n, m):
         arr1.append(0)
      
    # returns 1 if version 1 is bigger and -1 if
    # version 2 is bigger and 0 if equal
    for i in range(len(arr1)):
      if arr1[i]>arr2[i]:
         return 1
      if arr2[i]>arr1[i]:
         return -1
    return 0


def recursive_chown(path, owner):
    for dirpath, dirnames, filenames in os.walk(path):
        shutil.chown(dirpath, owner)
        for filename in filenames:
            shutil.chown(os.path.join(dirpath, filename), owner)


def PullUpdate(url, dir):
    print('Creating DL Dir...')
    dl_dir = f'{dir}/Download'
    dl_git_dir = f'{dl_dir}/.git'
    if os.path.exists(dl_dir):
        recursive_chown(dl_dir, current_user)
        recursive_chown(dl_git_dir, current_user)
        #os.system(f'rm -r -f {dl_dir}')
        shutil.rmtree(dl_dir)
        os.makedirs(dl_dir)
        pass
    else:
        recursive_chown(dl_dir, current_user)
        recursive_chown(dl_git_dir, current_user)
        os.makedirs(dl_dir)
    print('Pulling Update From Repo')
    Repo.clone_from(url, dl_dir)
    print('Moving Files To Current Working Dir')
    copyTree(dl_dir, dir)
    print('Removing Download Dir')
    shutil.rmtree(dl_dir)
    shutil.rmtree(f'{dir}/.git')
    #os.system(f'rm -r -f {dl_dir}')
    print('Update Complete')


print(f'Current User is: {current_user}')
installed_version = GetCurrentVersion()
latest_version = GetLatestVersion()

# Driver program to check above comparison function
version1 = installed_version
version2 = latest_version
  
ans = versionCompare(version1, version2)
if ans < 0:
    print (f'Your Version Of {program_name} Is Out Of Date.')
    PullUpdate(update_repo, cwd)
if ans > 0:
    print (f'Your Version Of {program_name} Is Up To Date.')
else:
    print (f'Your Version Of {program_name} Is Up To Date.')   

