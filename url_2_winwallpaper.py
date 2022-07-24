import os.path
import sys

import requests
import win32api
import win32con
import win32gui
import configparser


cf = configparser.ConfigParser()
cf.read('config_url_win.ini', encoding='utf-8')
url_photo = cf.get('config', 'url_photo')
WallpaperStyle = cf.get('config', 'WallpaperStyle')
TileWallpaper = cf.get('config', 'TileWallpaper')

temp_local_photo_name = 'temp.file'

tmp_file_abs = os.path.join(os.path.abspath(os.path.dirname(__file__)), temp_local_photo_name)

try:
    # save url to local temp file
    res = requests.get(url_photo)
    with open(temp_local_photo_name, 'wb') as f:
        f.write(res.content)
except:
    print('Network error.')
    sys.exit(0)


# set local photo to windows wallpaper
key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, str(WallpaperStyle))
win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, str(TileWallpaper))
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, tmp_file_abs, 1 + 2)
