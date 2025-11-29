#!/usr/bin/env python3
# spam.py — dengan fitur multiple target NGL link spammer

import requests
import time
from datetime import datetime
import getpass
import os
import sys
import base64
import itertools


PASSWORD_B64 = "Z29ibG9r"
PASSWORD = base64.b64decode(PASSWORD_B64).decode("utf-8")
MAX_ATTEMPTS = 3

# --- ANSI color codes ---
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[95m"   # NGL-like primary
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"

# --- ASCII Art Banner (from your input) ---
ascii_oscar = r"""
$$$$$$$$$$$$$%&%@$$$$$aCr|)\rYmoB$h{^  ."i?tp$$$$$
$$$av\||txYY]I"I<?|cL]`        '>\I  _{+!,. 'z$$$$
$$C^  .      '->I^    `|OkakmJf~    I8$$B81  ]$$$$
$8I  n#*hpQ~ f$$BWj  +h$$$$$$$$$k<  \$$$$&;  C$$$$
$m  ^#$$$$$0 O$$$@+ iW$$$$0+U$$$$f  0$$$$Q  ,M$$$$
$f  -@$$$$$#:k$$$h. O$$$$k' :vx/}" ^#$$$$|  }$$$$$
@+  x$$$$$$$cM$$$X ;8$$$$/~J0Zpq_  <@$$$%!  `<\b$$
#,  m$$$8&$$$$$$${ >@$$$$[_$$$$$a" {$$$$M!I<<  ^d$
w  `*$$$Oj$$$$$$%! ,W$$$$L,)q$$$${ [$$$$@&%@@(  _%
J  I8$$$J"#$$$$$*^  )B$$$$W*@$$$Z, .j8$$$$$$$M:  Y
x  ~$$$$X t$$$$$d    +J*B$$$$Bd\.    <QkmLzr(]'  X
u  !a&B$z 'nZda*U  .,  .!}//[l  .]mr"        ^I]LB
*+  ."!_;      .  .jWOj_;'  ';-nb$$$*CxjvJZdoW%$$$
$%Qt]i^.'lrJuf|1)jw$$$$$8*aa*8$$$$$$$$$$$$$$$$$$$$
"""

# --- helpers / UI animations ---
def tprint(text: str, speed: float = 0.002, color: str = MAGENTA):
    """Typewriter print with color"""
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(RESET + "\n")

def sleep_with_spinner(seconds: float, prefix: str = "", spinner_chars=None):
    """Sleep but show spinner animation (non-blocking-ish)"""
    if spinner_chars is None:
        spinner_chars = "|/-\\"
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        char = spinner_chars[i % len(spinner_chars)]
        sys.stdout.write(f"\r{DIM}{prefix} {char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.12)
        i += 1
    sys.stdout.write("\r" + " " * (len(prefix) + 4) + "\r")
    sys.stdout.flush()

def color_status(code: int) -> str:
    if 200 <= code < 300:
        return GREEN
    if 300 <= code < 400:
        return YELLOW
    return RED

# --- Password check ---
def require_password():
    attempts = MAX_ATTEMPTS
    while attempts > 0:
        try:
            entered = getpass.getpass(CYAN + "Masukkan password: " + RESET)
        except Exception:
            entered = input("Masukkan password: ")
        if entered == PASSWORD:
            print(GREEN + "Password benar. Melanjutkan...\n" + RESET)
            return True
        attempts -= 1
        print(RED + f"Password salah. Sisa percobaan: {attempts}" + RESET)
    print(RED + "Percobaan habis. Keluar." + RESET)
    return False

if not require_password():
    sys.exit(1)

# show banner with animated typing
tprint(ascii_oscar, speed=0.0008, color=MAGENTA)
print(CYAN + BOLD + "=== Simple NGL Sender (Multi-Target) by Maklu ===" + RESET + "\n")

# --- Program utama ---
URL = "https://ngl.link/api/submit"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://ngl.link",
    "Referer": "https://ngl.link/",
}

def parse_int(prompt, default=0):
    s = input(prompt).strip()
    if s == "":
        return default
    try:
        return int(s)
    except:
        print(YELLOW + "Input angka tidak valid, menggunakan default:" + RESET, default)
        return default

def parse_float(prompt, default=5.0):
    s = input(prompt).strip()
    if s == "":
        return default
    try:
        return float(s)
    except:
        print(YELLOW + "Input angka tidak valid, menggunakan default:" + RESET, default)
        return default

# --- MODIFIKASI: Input multiple username ---
# User memasukkan username dipisahkan koma atau spasi
username_input = input(CYAN + "Masukkan username target (pisahkan dengan koma/spasi, contoh: pukyy, target2): " + RESET).strip()
# Memisahkan input menjadi daftar username
usernames = [u.strip() for u in username_input.replace(',', ' ').split() if u.strip()]

if not usernames:
    print(RED + "Tidak ada username target yang dimasukkan. Keluar." + RESET)
    sys.exit(1)

pesan = input(CYAN + "Masukkan pesan yang akan dikirim: " + RESET).strip()
jumlah_per_target = parse_int(CYAN + "Jumlah pesan PER TARGET (0 = tanpa batas): " + RESET, default=0)
delay = parse_float(CYAN + "Delay antar kiriman ke target BERBEDA dalam detik (default 5): " + RESET, default=5.0)

# Menentukan perulangan
# itertools.cycle akan mengulang daftar username terus menerus jika jumlah pesan tak terbatas
target_cycle = itertools.cycle(usernames)
total_sent_limit = jumlah_per_target * len(usernames) if jumlah_per_target != 0 else 0

sent = 0
print("\n" + DIM + f"--- Mulai mengirim ke {len(usernames)} target --- (Ctrl+C untuk stop) ---" + RESET + "\n")

try:
    # Perulangan utama akan berjalan terus menerus atau sampai batas total_sent_limit
    while True:
        if total_sent_limit != 0 and sent >= total_sent_limit:
            print(GREEN + f"Selesai: {sent} pesan terkirim secara total." + RESET)
            break

        # Ambil username target berikutnya dari cycle
        current_username = next(target_cycle)

        # Cek apakah target ini sudah mencapai batas kiriman per target
        # Karena kita menggunakan cycle, kita hanya perlu membatasi total kiriman
        
        data = {
            "username": current_username,
            "deviceId": "aa",
            "gameSlug": "",
            "referrer": "",
            "question": pesan
        }

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sys.stdout.write(CYAN + f"[{now}] Mengirim ke {current_username!r}..." + RESET + " ")
        sys.stdout.flush()
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.18)
        sys.stdout.write("\n")

        try:
            resp = requests.post(URL, headers=HEADERS, data=data, timeout=15)
            sent += 1
            status = resp.status_code

            # coba parse JSON
            try:
                j = resp.json()
            except:
                j = {}

            qid = j.get("questionId") if isinstance(j, dict) else None

            # colored output
            code_color = color_status(status)
            print(f"{CYAN}[{now}]{RESET} #{sent} -> Target: {current_username!r}")
            print(f"   HTTP {code_color}{status}{RESET}")
            if qid:
                print(f"   {MAGENTA}questionId:{RESET} {qid}")
            text_preview = resp.text
            if len(text_preview) > 400:
                text_preview = text_preview[:400] + "...(truncated)"
            print(f"   Response body: {DIM}{text_preview}{RESET}\n")

        except Exception as e:
            print(f"{RED}[{now}] Error ke {current_username!r}: {e}{RESET}\n")

        # wait with spinner to look fancy
        # Delay ini berlaku setelah setiap kiriman ke target (antar kiriman ke target berbeda)
        sleep_with_spinner(delay, prefix=f"{CYAN}Waiting for next target{RESET}")

except KeyboardInterrupt:
    print("\n" + YELLOW + f"Dihentikan oleh user. Total pesan terkirim: {sent}" + RESET)
    sys.exit(0)
