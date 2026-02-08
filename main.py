import sys
import os
import time
import t
import an
import at

def settings_menu():
    while True:
        L = t.STRINGS[t.CONF["lang"]]
        opts = ["1. THEMES", "2. LOGO STYLE", "3. LANGUAGE", f"4. BOTS [{t.CONF['botnet_size']}]", "5. BACK"]
        an.print_ui(opts)
        c = input(an.apply_color(f"   {L['choice']}"))
        if c == "1": theme_menu()
        elif c == "2": logo_menu()
        elif c == "3": 
            t.CONF["lang"] = "en" if t.CONF["lang"] == "ru" else "ru"
            t.save_config(t.CONF)
        elif c == "4":
            try:
                t.CONF["botnet_size"] = int(input(an.apply_color("   COUNT -> ")))
                t.save_config(t.CONF)
            except: pass
        elif c == "5": break

def theme_menu():
    while True:
        opts = ["1. BW", "2. RY", "3. GB", "4. PM", "5. CY", "6. RB", "7. BACK"]
        an.print_ui(opts)
        c = input(an.apply_color("   CHOICE -> "))
        if c in ["1","2","3","4","5","6"]:
            keys = list(t.THEMES.keys())
            t.CONF["theme"] = keys[int(c)-1]
            t.save_config(t.CONF)
        elif c == "7": break

def logo_menu():
    while True:
        opts = ["1. CLASSIC", "2. MINIMAL", "3. CYBER", "4. BACK"]
        an.print_ui(opts)
        c = input(an.apply_color("   CHOICE -> "))
        if c == "1": t.CONF["logo_style"] = "classic"
        elif c == "2": t.CONF["logo_style"] = "minimal"
        elif c == "3": t.CONF["logo_style"] = "cyber"
        elif c == "4": break
        t.save_config(t.CONF)

def run():
    if t.CONF["owner"] == "User":
        an.print_ui(["REGISTRATION"])
        t.CONF["owner"] = input(an.apply_color("   NAME -> ")) or "Admin"
        t.save_config(t.CONF)
    an.slow_loading(t.STRINGS[t.CONF["lang"]]["boot"])
    while True:
        L = t.STRINGS[t.CONF["lang"]]
        an.print_ui([L["m1"], L["m2"], L["m3"]])
        c = input(an.apply_color(f"   {L['choice']}"))
        if c == "1": at.start_attack()
        elif c == "2": settings_menu()
        elif c == "3": sys.exit()

if __name__ == "__main__":
    try: run()
    except KeyboardInterrupt: sys.exit()
      
