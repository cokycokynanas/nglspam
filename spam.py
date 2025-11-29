#!/usr/bin/env python3
# spam.py — NGL Spam Sender (Multi-Target) by Maklu
# Versi dengan tampilan yang lebih modern + Logo ASCII Keren

import requests
import time
from datetime import datetime
import getpass
import os
import sys
import base64
import itertools

# --- Konfigurasi password ---
# base64 dari "goblox" = "Z29ibG9r"
PASSWORD_B64 = "Z29ibG9r"
PASSWORD = base64.b64decode(PASSWORD_B64).decode("utf-8")
MAX_ATTEMPTS = 3

# --- ANSI color codes ---
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
BLUE = "\033[94m"
WHITE = "\033[97m"
BG_GREEN = "\033[42m" 

# --- LOGO ASCII BARU ---
ascii_logo_ngl = fr"""
{RED}{BOLD}  /$$   /$$ {MAGENTA}/$$$$$$$  {BLUE} /$$
{RED} | $$  | $$ {MAGENTA}| $$__  $$ {BLUE}| $$
{RED} | $$  | $$ {MAGENTA}| $$  \ $$ {BLUE}| $$
{RED} | $$$$$$$$ {MAGENTA}| $$$$$$$  {BLUE}| $$
{RED} | $$__  $$ {MAGENTA}| $$__  $$ {BLUE}| $$
{RED} | $$  | $$ {MAGENTA}| $$  | $$ {BLUE}| $$
{RED} | $$  | $$ {MAGENTA}| $$$$$$$/ {BLUE}| $$$$$$${RESET}
{RED} |__/  |__/ {MAGENTA}|_______/  {BLUE}|_______/{RESET}
{CYAN}  --- MULTI-TARGET SPAM SENDER ---{RESET}
"""

def clear_screen():
    """Membersihkan terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Mencetak header program yang rapi"""
    clear_screen()
    
    # Cetak Logo ASCII Baru
    print(ascii_logo_ngl)
    
    # Divider/Garis Pemisah
    print(f"{MAGENTA}{'=' * 60}{RESET}")
    print(f"{CYAN}{BOLD}>>> NGL.LINK AUTOMATED SENDER v2.0 <<<{RESET}")
    print(f"{MAGENTA}{'=' * 60}{RESET}\n")

# --- helpers / UI animations ---
def color_status(code: int) -> str:
    """Mengembalikan kode warna berdasarkan status HTTP"""
    if 200 <= code < 300:
        return GREEN  # Sukses
    if 300 <= code < 400:
        return YELLOW # Redirect/Warning
    return RED       # Error

def print_progress(current, total, bar_length=30):
    """Menampilkan progress bar sederhana"""
    if total <= 0:
        return
    
    percent = current / total
    filled_length = int(bar_length * percent)
    bar = BG_GREEN + ' ' * filled_length + RESET + ' ' * (bar_length - filled_length)
    
    sys.stdout.write(f"\r{CYAN}[{current}/{total}]{RESET} {bar} {percent*100:.1f}%")
    sys.stdout.flush()

# --- Password check ---
def require_password():
    """Meminta password"""
    attempts = MAX_ATTEMPTS
    while attempts > 0:
        try:
            entered = getpass.getpass(CYAN + "🔒 Masukkan password: " + RESET)
        except Exception:
            entered = input("🔒 Masukkan password: ")
        if entered == PASSWORD:
            print(f"{GREEN}✅ Password benar. Melanjutkan...\n{RESET}")
            return True
        attempts -= 1
        print(f"{RED}❌ Password salah. Sisa percobaan: {attempts}{RESET}")
    print(f"{RED}❌ Percobaan habis. Keluar.{RESET}")
    return False

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
    """Mengambil input integer dengan default"""
    s = input(prompt).strip()
    if s == "":
        return default
    try:
        return int(s)
    except:
        print(f"{YELLOW}⚠️ Input angka tidak valid, menggunakan default: {default}{RESET}")
        return default

def parse_float(prompt, default=5.0):
    """Mengambil input float dengan default"""
    s = input(prompt).strip()
    if s == "":
        return default
    try:
        return float(s)
    except:
        print(f"{YELLOW}⚠️ Input angka tidak valid, menggunakan default: {default}{RESET}")
        return default

if not require_password():
    sys.exit(1)

print_header()

# --- MODIFIKASI: Input multiple username ---
username_input = input(f"{CYAN}🎯 Masukkan username target (pisahkan dengan koma/spasi, cth: pukyy, target2): {RESET}").strip()
usernames = [u.strip() for u in username_input.replace(',', ' ').split() if u.strip()]

if not usernames:
    print(f"{RED}❌ Tidak ada username target yang dimasukkan. Keluar.{RESET}")
    sys.exit(1)

pesan = input(f"{CYAN}💬 Masukkan pesan yang akan dikirim: {RESET}").strip()
jumlah_per_target = parse_int(f"{CYAN}🔢 Jumlah pesan PER TARGET (0 = tanpa batas): {RESET}", default=0)
delay = parse_float(f"{CYAN}⏳ Delay antar kiriman ke target BERBEDA dalam detik (default 5.0): {RESET}", default=5.0)

# Menentukan perulangan
target_cycle = itertools.cycle(usernames)
total_targets = len(usernames)
total_sent_limit = jumlah_per_target * total_targets if jumlah_per_target != 0 else 0

sent = 0
print(f"\n{MAGENTA}--- RINGKASAN START ---{RESET}")
print(f"   Target: {total_targets} username ({', '.join(usernames)})")
print(f"   Pesan : {pesan[:40]}...")
print(f"   Batas Kirim: {jumlah_per_target} per target. Total Maks: {total_sent_limit if total_sent_limit != 0 else 'Tidak Terbatas'}")
print(f"   Delay: {delay} detik\n")

print(f"{BLUE}{BOLD}=== Mulai Mengirim === (Tekan Ctrl+C untuk stop){RESET}\n")

try:
    # Perulangan utama
    while True:
        if total_sent_limit != 0 and sent >= total_sent_limit:
            print_progress(total_sent_limit, total_sent_limit) # Selesai 100%
            print(f"\n{GREEN}✅ Selesai: {sent} pesan terkirim secara total.{RESET}")
            break

        # Ambil username target berikutnya
        current_username = next(target_cycle)
        now = datetime.now().strftime("%H:%M:%S")

        
        if total_sent_limit > 0:
            print_progress(sent, total_sent_limit)
        
        # Output proses
        sys.stdout.write(f"\r{MAGENTA}[{now}]{RESET} 🎯 Kirim ke: {BOLD}{current_username}{RESET} (Pesan ke #{sent+1})")
        sys.stdout.flush()
        
        data = {
            "username": current_username,
            "deviceId": "aa",
            "gameSlug": "",
            "referrer": "",
            "question": pesan
        }

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
            
            # Colored output
            code_color = color_status(status)
            status_text = "SUCCESS" if 200 <= status < 300 else "ERROR/WARN"

            # Tampilan hasil kiriman
            print(f"\r{MAGENTA}[{now}]{RESET} ✨ Status: {code_color}{BOLD}{status_text} ({status}){RESET}")
            print(f"{DIM}   -> Target: {current_username}{RESET}")
            if qid:
                print(f"{DIM}   -> Question ID: {qid}{RESET}")
            else:
                print(f"{DIM}   -> Response: {resp.text[:60]}...{RESET}")
            
        except Exception as e:
            print(f"\r{RED}[{now}] ❌ Error ke {current_username}: {e}{RESET}")
            
        # Tampilkan progress bar lagi setelah hasil
        if total_sent_limit > 0:
            print_progress(sent, total_sent_limit)
        
        # Jeda
        sys.stdout.write(f"\n{DIM}   ⏳ Jeda {delay:.1f}s sebelum target berikutnya...{RESET}\r")
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write(" " * 80 + "\r") # Membersihkan baris jeda
        
except KeyboardInterrupt:
    print_progress(sent, total_sent_limit if total_sent_limit > 0 else sent) # Tampilkan progress bar terakhir
    print(f"\n{YELLOW}⚠️ Dihentikan oleh user. Total pesan terkirim: {sent}{RESET}")
    sys.exit(0)
