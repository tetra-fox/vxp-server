import configparser
parser = configparser.ConfigParser()
parser.read("config.ini")

config = parser["Config"]
internals = parser["DontTouchMe"]