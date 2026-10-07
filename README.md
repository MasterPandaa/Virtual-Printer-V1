# 🖨️ Virtual Printer V1 - Lightweight RAW TCP/IP Printer Emulator

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](#)
[![Protocol](https://img.shields.io/badge/Protocol-RAW%20TCP%2FIP%20(Port%209100)-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Virtual Printer V1** adalah aplikasi desktop GUI portabel dan berbobot ringan untuk mengemulasikan server printer jaringan (*network receipt/document printer*) berbasis socket **RAW TCP/IP** standar (port `9100`).

Dirancang khusus untuk **Software Engineers**, **QA/SDET Automation**, dan **DevOps** yang membutuhkan simulator perangkat cetak guna menguji *dispatching* struk POS, *billing engine*, format ESC/POS, dan logika *backend printing* tanpa bergantung pada perangkat keras printer fisik.

---

## 🌟 Mengapa Menggunakan Virtual Printer V1?

- 🚫 **Bebas Ketergantungan Hardware Fisik**: Mengeliminasi kebutuhan membeli, menghubungkan, atau merawat printer thermal/jaringan saat fase *development* dan *staging*.
- ⚡ **Verifikasi Socket Instan & Real-Time**: Memantau jabat tangan TCP (*three-way handshake*), IP/port klien, transfer ukuran *payload*, dan *event timeout* secara langsung.
- 🎯 **Dukungan Decoding Lengkap**: Mendekode teks dan byte stream secara cerdas menggunakan *fallback* `UTF-8`, `Latin-1`, serta *raw binary command stream*.
- 🛡️ **Zero Friction (Tanpa `pip install`)**: 100% dibangun menggunakan pustaka standar Python 3 bawaan (*zero external dependencies*).
- 🔒 **100% Lokal & Aman**: Berjalan sepenuhnya di lingkungan *localhost* atau LAN tanpa mengirimkan telemetri atau data keluar.

---

## 🚀 Fitur Utama

1. **Standard RAW 9100 Socket Server**:
   - Mendengarkan koneksi TCP langsung pada port `9100` (atau port kustom yang dapat dikonfigurasi).
   - Mendukung multithreaded socket handling untuk melayani koneksi masuk tanpa memblokir antarmuka GUI.
2. **Live Socket Diagnostic Log**:
   - Menampilkan catatan aktivitas jaringan secara terperinci: waktu koneksi, IP klien, port asal, durasi koneksi, hingga jumlah byte yang diterima.
3. **Payload Inspection & Stream Decoder**:
   - Otomatis melakukan parsing data cetak yang masuk dengan dukungan format teks dan karakter kontrol printer (ESC/POS).
4. **Modern High-Contrast Dark GUI**:
   - Tampilan desktop bersih berbasis Tkinter yang responsif, ergonomis untuk mata, dan mudah dioperasikan.
5. **Portabel & Ringan**:
   - Siap dijalankan langsung tanpa proses *build* atau instalasi paket eksternal tambahan.

---

## 🛠️ Tata Cara Instalasi

### 1. Prasyarat Sistem
- **Python 3.8** atau versi lebih baru (dengan modul bawaan `tkinter`).

### 2. Download / Clone Repository
```bash
git clone https://github.com/MasterPandaa/Virtual-Printer-V1.git
cd Virtual-Printer-V1
```

---

### 3. Menjalankan Aplikasi

#### 🪟 Windows
- **Cara Cepat**: Klik ganda pada file `run.bat`.
- **Melalui Terminal**:
  ```powershell
  python app.py
  ```

#### 🐧 Linux (Ubuntu / Debian / Arch / Fedora)
```bash
# Pastikan modul python3-tk terpasang (jika belum ada)
sudo apt install python3-tk  # Untuk Debian/Ubuntu

python3 app.py
```

#### 🍎 macOS
```bash
python3 app.py
```

---

## 📖 Panduan Penggunaan

```text
┌─────────────────┐     ┌───────────────────────┐     ┌─────────────────────┐
│ 1. Set Bind &   │ ──> │ 2. Klik Start Server  │ ──> │ 3. Dispatch Print   │
│    Port (9100)  │     │    Status: LISTENING  │     │    dari Aplikasi    │
└─────────────────┘     └───────────────────────┘     └─────────────────────┘
                                                                 │
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │ 4. Pantau Live Log  │
                                                      │    & Payload Data   │
                                                      └─────────────────────┘
```

1. **Konfigurasi Host & Port**: Tentukan *Bind IP* (default `0.0.0.0` atau `127.0.0.1`) dan nomor *Port* (default `9100`).
2. **Aktivasi Server**: Klik tombol **▶ Start Server** untuk mulai mendengarkan lalu lintas socket.
3. **Arahkan Aplikasi Target**: Konfigurasikan sistem backend/POS Anda ke IP mesin ini pada port `9100` dengan protokol `RAW` / `TCP Direct`.
4. **Inspeksi Data**: Data cetak yang dikirim akan langsung tampil pada jendela *Live Logs* dan *Payload Content*.
5. **Hentikan Server**: Klik **⏹ Stop Server** untuk menutup socket.

---

## 🧪 Uji Mandiri & Testing Suite

Gunakan contoh *script* simulasi pengiriman data cetak berikut untuk memverifikasi socket server:

### A. Menggunakan Python (`socket`)
```python
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9100

payload = (
    "================================\n"
    "       VIRTUAL PRINTER TEST      \n"
    "================================\n"
    "Order ID : #INV-2026-001\n"
    "Item     : Espresso Single Shot\n"
    "Total    : Rp 25.000\n"
    "Status   : PAID\n"
    "================================\n"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((SERVER_IP, SERVER_PORT))
    client.sendall(payload.encode("utf-8"))
    print("✅ Payload cetak berhasil dikirim!")
```

### B. Menggunakan PowerShell (Windows)
```powershell
$client = New-Object System.Net.Sockets.TcpClient("127.0.0.1", 9100)
$stream = $client.GetStream()
$bytes = [System.Text.Encoding]::UTF8.GetBytes("Hello from PowerShell Virtual Printer Test`r`n")
$stream.Write($bytes, 0, $bytes.Length)
$stream.Close()
$client.Close()
Write-Host "✅ Test stream terkirim"
```

### C. Menggunakan Netcat / Bash (Linux / macOS)
```bash
echo -e "\x1B\x40--- NOTA PEMBAYARAN ---\nTotal: Rp 150.000\n" | nc 127.0.0.1 9100
```

---

## 📦 Struktur Project

```text
Virtual-Printer-V1/
├── app.py              # Entry point utama aplikasi & GUI Tkinter
├── run.bat             # Launcher instan satu-klik untuk Windows
├── requirements.txt    # Spesifikasi dependensi (Standard Library)
├── .gitignore          # Konfigurasi file pengabaian Git
├── LICENSE             # Dokumen lisensi open-source MIT
└── README.md           # Dokumentasi komprehensif proyek
```

---

## 🔒 Privasi & Keamanan

- **100% Offline Runtime**: Tidak ada koneksi *outbound*, *analytic tracking*, maupun pengumpulan telemetri.
- **Isolasi Socket Aman**: Hanya melayani koneksi masuk pada port lokal yang Anda tentukan secara eksplisit.
- **Sanitasi Memori**: Buffer data socket diproses dan dibersihkan per sesi tanpa persistensi file tersembunyi.

---

## 📄 Lisensi & Kontribusi

Proyek ini dirilis di bawah lisensi [MIT](LICENSE). Bebas digunakan, didistribusikan, dan dimodifikasi untuk kebutuhan riset, pengujian internal, maupun kebutuhan komersial.

Kontribusi, *bug report*, dan saran fitur dapat diajukan melalui [GitHub Issues](https://github.com/MasterPandaa/Virtual-Printer-V1/issues) atau *Pull Request*.
