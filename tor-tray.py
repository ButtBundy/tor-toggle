#!/usr/bin/env python3
import os

HOME = os.path.expanduser("~")
SCRIPT = os.path.join(HOME, ".local/bin/private.sh")

os.environ["PYSTRAY_BACKEND"] = "gtk"

import pystray
from PIL import Image
import subprocess

STATE_FILE = "/tmp/tor_enabled"

def is_tor_on():
    return os.path.exists(STATE_FILE)

def make_icon(color):
    img = Image.new("RGB", (64, 64), color=color)
    return img

def toggle(icon, item):
    subprocess.run(["bash", SCRIPT, "toggle"])
    if is_tor_on():
        icon.icon = make_icon("green")
    else:
        icon.icon = make_icon("red")

def toggle_label(item):
    return "Disable Tor" if is_tor_on() else "Enable Tor"

icon = pystray.Icon(
    "tor",
    make_icon("red"),
    "TOR",
    menu=pystray.Menu(
        pystray.MenuItem(toggle_label, toggle)
    )
)

icon.run()
