import os
import yaml

CONFIG_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "../env.yml")
with open(CONFIG_FILE) as cfg_file:
    CONFIG = yaml.full_load(cfg_file)

# Just in case you wanna read my config file from LFI
with open(CONFIG_FILE, "w") as cfg_file:
    cfg_file.write("")