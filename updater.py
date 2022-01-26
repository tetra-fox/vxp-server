import os
import sys
import semver
import requests
import zipfile
from colorama import Fore
from config import *
from logger import Logger

logger = Logger("updater", Fore.CYAN)

def check():
    response = requests.get(f"https://api.github.com/repos/{internals['Repo']}/releases/latest")
    json = response.json()

    if (response.status_code != 200):
        logger.error(f"Error checking for updates: {response.status_code}")
        return

    remote_version = json["tag_name"] # usually my tag names are pure semvers
    diff = semver.compare(remote_version, internals['Version'])

    if (diff == 1):
        logger.warn(f"Checking for GitHub for updates...")
        logger.warn(f"Update available! vxp-server v{remote_version} is now available.")
        if (parser.getboolean("Config", "AutoUpdate")): 
            download_zip(json)
        else:
            logger.warn("Auto-updates are disabled. Update for the latest features and bug fixes.")
            logger.warn(f"Download: https://github.com/{internals['Repo']}/releases/latest")
    else:
        logger.log("You are running the latest version of vxp-server.")


def download_zip(json):
    zip_url = json["zipball_url"]

    try:
        logger.log("Downloading update...")
        response = requests.get(zip_url, stream=True)
        with open("vxp-server.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        logger.log("Installing...")

        with zipfile.ZipFile("vxp-server.zip", "r") as zip:
            for file in zip.namelist():
                zip_prefix = internals["repo"].replace("/", "-")
                if file.startswith(zip_prefix):
                    zip.extract(file, "./")

        os.remove("vxp-server.zip")

        internals["Version"] = json["tag_name"]
        with open("config.ini", "w") as config_file:
            parser.write(config_file)

        logger.ok("Update complete. Restarting...")
        os.execl(sys.executable, *([sys.executable]+sys.argv))

    except Exception as e:
        logger.error(e)
        logger.error("Error downloading update. Skipping...")