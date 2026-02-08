import json
import os
from pystyle import Colors

CONFIG_FILE = "config.json"
LOG_FILE = "logs.txt"

DEFAULT_CONFIG = {
    "owner": "User",
    "lang": "ru",
    "theme": "bw",
    "gradient": "hor",
    "save_logs": True,
    "logo_style": "classic",
    "botnet_size": 50
}

THEMES = {
    "bw": Colors.black_to_white, "ry": Colors.red_to_yellow,
    "gb": Colors.green_to_blue, "pm": Colors.purple_to_red,
    "cy": Colors.cyan_to_green, "rb": Colors.rainbow
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            updated = False
            for key, value in DEFAULT_CONFIG.items():
                if key not in data:
                    data[key] = value
                    updated = True
            if updated: save_config(data)
            return data
        except: return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(conf):
    with open(CONFIG_FILE, "w") as f:
        json.dump(conf, f, indent=4)

CONF = load_config()

STRINGS = {
    "ru": {
        "m1": "1. ЗАПУСТИТЬ АТАКУ", "m2": "2. НАСТРОЙКИ", "m3": "3. ВЫХОД",
        "choice": "ВЫБОР -> ", "boot": "ЗАГРУЗКА БОТНЕТА", "setup": "ГЛАВНЫЙ УЗЕЛ",
        "target": "ЦЕЛЬ (IP:PORT/URL) -> ", "meth": "МЕТОД (1:UDP/2:HTTP) -> ",
        "limit": "ЛИМИТ (0=INF) -> ", "threads": "БОТЫ В СЕТИ", "finished": "СЕТЬ ОТКЛЮЧЕНА",
        "owner_label": "ЛИЦЕНЗИЯ: ", "scraping": "ПОДКЛЮЧЕНИЕ ПРОКСИ...",
        "timer": "ТАЙМЕР (0 = INF) -> ", "psize": "ВЕС ПАКЕТА (kb/mb) -> "
    },
    "en": {
        "m1": "1. START ATTACK", "m2": "2. SETTINGS", "m3": "3. EXIT",
        "choice": "CHOICE -> ", "boot": "BOOTING BOTNET", "setup": "MASTER NODE",
        "target": "TARGET (IP:PORT/URL) -> ", "meth": "METHOD (1:UDP/2:HTTP) -> ",
        "limit": "LIMIT (0=INF) -> ", "threads": "BOTS IN NET", "finished": "NET DISCONNECTED",
        "owner_label": "LICENSE: ", "scraping": "CONNECTING PROXIES...",
        "timer": "TIMER (0 = INF) -> ", "psize": "PACKET SIZE (kb/mb) -> "
    }
}
