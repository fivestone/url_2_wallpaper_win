import os.path
import sys

import requests
import win32api
import win32con
import win32gui
import configparser

exe_path = os.getcwd()
ini_file = os.path.join(exe_path, 'config_url_win.ini')
tmp_file = os.path.join(exe_path, 'temp.file')

cf = configparser.ConfigParser()
cf.read(ini_file, encoding='utf-8')
url_photo = cf.get('config', 'url_photo')
WallpaperStyle = cf.get('config', 'WallpaperStyle')
TileWallpaper = cf.get('config', 'TileWallpaper')

try:
    # save url to local temp file
    res = requests.get(url_photo)
    with open(tmp_file, 'wb') as f:
        f.write(res.content)
except:
    print('Network error.')
    sys.exit(0)

# set local photo to windows wallpaper
key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, str(WallpaperStyle))
win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, str(TileWallpaper))
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, tmp_file, 1 + 2)
