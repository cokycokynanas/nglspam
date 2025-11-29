# 📨 Simple NGL Sender

**Simple NGL Sender** adalah script Python untuk mengirim pesan anonim ke **NGL.link** secara otomatis.  
Script ini dilengkapi dengan **password proteksi (Base64)**, **ASCII art banner**, serta **animasi dan warna** untuk tampilan terminal yang menarik.

---

## ✨ Fitur
- 🎨 ASCII banner "OSCAR"  
- 🌈 Animasi typewriter dan warna terminal mirip tema NGL  
- ⚡ Mengirim pesan otomatis ke akun NGL  
- ⏱️ Atur jumlah pesan dan delay antar pengiriman  
- 📝 Menampilkan log lengkap: HTTP status, questionId, timestamp, dan preview response  

---

## 📦 Instalasi

Clone repository ini:

```bash
git clone https://github.com/cokycokynanas/nglspam
cd nglspam
pip install -r requirements.txt
```
---

🚀 Cara Pakai

Jalankan script:
```
python3 spam.py
```
1. Masukkan password:****
2. Masukkan username target NGL
3. Masukkan pesan yang ingin dikirim
4. Masukkan jumlah pesan (0 = tanpa batas)
5. Masukkan delay antar pesan (detik)
