import os
import sys
import time
from pystyle import Colorate
import t

def get_size():
    try: return os.get_terminal_size()
    except: return (55, 24)

def apply_color(text):
    theme_color = t.THEMES.get(t.CONF["theme"], t.THEMES["bw"])
    if t.CONF["gradient"] == "hor":
        return Colorate.Horizontal(theme_color, text)
    else:
        return Colorate.Vertical(theme_color, text)

LOGOS = {
    "classic": """
      ▄█     ▄███████▄ 
     ███    ███    ███ 
     ███▌   ███    ███ 
     ███▌   ███    ███ 
     ███▌ ▀█████████▀  
     ███    ███        
     ███    ███        
     █▀    ▄████▀      """,
    "minimal": """
    [ B O T N E T - S Y S ]
       Virtual Network   """,
    "cyber": """
    █▀▀ █ █ █▀▄ █▀▀ █▀█
    █▄▄ ▀▄█ █▀▄ █▀▀ █▄█
    ╚═════════════════╝ """
}

def build_box(text_lines):
    w, _ = get_size()
    cw = 40 
    res = ["╔" + "═" * cw + "╗", "║" + " " * cw + "║"]
    for line in text_lines:
        res.append("║" + line.center(cw) + "║")
    res.extend(["║" + " " * cw + "║", "╚" + "═" * cw + "╝"])
    return [l.center(w) for l in res]

def print_ui(lines):
    w, h = get_size()
    os.system('clear')
    lang = t.CONF["lang"]
    display = list(lines)
    display.append("—" * 20)
    display.append(f"{t.STRINGS[lang]['owner_label']}{t.CONF['owner']}")
    
    logo_text = LOGOS.get(t.CONF["logo_style"], LOGOS["classic"])
    asc = [l for l in logo_text.split('\n') if l.strip()]
    box = build_box(display)
    
    total_h = len(asc) + len(box) + 2
    pad = max(0, (h - total_h) // 2)
    
    print("\n" * pad)
    for l in asc: print(apply_color(l.center(w)))
    print("\n")
    for l in box: print(apply_color(l))

def slow_loading(text):
    w, h = get_size()
    os.system('clear')
    print("\n" * (h // 2))
    for i in range(21):
        bar = "█" * (i // 2) + "░" * (10 - i // 2)
        line = f"[!] {text}: [{bar}] {i*5}%"
        sys.stdout.write('\r' + apply_color(line.center(w)))
        sys.stdout.flush()
        time.sleep(0.02)
    print()

def draw_bar(current, total):
    width = 20
    if total <= 0:
        tick = int(time.time() * 5) % width
        bar = "░" * tick + "█" + "░" * (width - tick - 1)
        return f"[{bar}] LIVE"
    percent = min(100, int((current / total) * 100))
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent}%"
  
