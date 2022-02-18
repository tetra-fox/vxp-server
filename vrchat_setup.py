import os

# This script will set a user environment variable pointing to the path of this
# folder which can then be used by VXP to automatically start the server upon startup.

server_path = "\\".join(__file__.split("\\")[:-1]) + "\\"

os.system(f"setx VXP_SERVER_PATH {server_path}")