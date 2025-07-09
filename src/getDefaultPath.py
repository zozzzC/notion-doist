import json
import os


def getDefaultPath():
    with open("config.json", "r") as f:
        config_data = json.load(f)
        f.close()

    if config_data["default_path"] == None:
        return ""
    else:
        return os.getcwd() + "/test/"
