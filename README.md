# Virtual RAW TCP/IP Printer Server (v1)

A lightweight, portable desktop GUI application that emulates a network receipt/document printer listening on standard **RAW TCP/IP sockets** (e.g. port `9100`).

Designed for developers and QA engineers to test print dispatching, POS receipt generation, and backend printing logic without needing physical hardware.

---

## ✨ Features

- **Standard RAW TCP/IP Protocol**: Listens on port `9100` (or any custom port) using industry-standard RAW 9100 socket communication.
- **Real-Time Live Logs**: Displays socket handshakes, client IP/port, ping events, timeouts, and byte statistics.
- **Payload Previewer**: Automatically decodes incoming print streams (`latin1` / `UTF-8` / ESC codes) and displays job headers and body content.
- **Zero External Dependencies**: Built 100% on Python 3 standard libraries (`tkinter`, `socket`, `threading`). No `pip install` required.
- **Modern Dark UI**: Clean, responsive, high-contrast dark theme.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed (with Tkinter support).

### Running the Application

**Option 1: Windows Double-Click Launcher**
Double-click `run.bat` to launch immediately.

**Option 2: Terminal / Command Line**
```bash
python app.py
```

---

## ⚙️ How It Works & Testing

1. Open the application and set your desired **Bind Host/IP** (default `0.0.0.0`) and **Port** (default `9100`).
2. Click **▶ Start Server**.
3. Point your application or backend printer configuration to:
   - **Host**: `127.0.0.1` (if running on the same machine) or your LAN IP.
   - **Port**: `9100`
   - **Protocol**: `RAW` / `RAW_9100` / `TCP Direct`

### Testing Connection via CLI

#### Using Python
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9100))
sock.sendall(b"Hello from Test Client!\nOrder #12345\nTotal: $99.00\n")
sock.close()
```

#### Using Netcat (`nc`)
```bash
echo -e "Test Print Stream Data\n" | nc 127.0.0.1 9100
```

#### Using PowerShell
```powershell
$client = New-Object System.Net.Sockets.TcpClient("127.0.0.1", 9100)
$stream = $client.GetStream()
$bytes = [System.Text.Encoding]::UTF8.GetBytes("Test Print Payload`r`n")
$stream.Write($bytes, 0, $bytes.Length)
$stream.Close()
$client.Close()
```

---

## 📂 Project Structure

```text
├── app.py           # Main GUI application script
├── run.bat          # Windows double-click launcher
├── requirements.txt # Dependency specifications (Python standard library)
├── .gitignore       # Git ignore rules
└── README.md        # Public documentation
```

---

## 📄 License
MIT License. Free to use for personal and commercial development/testing.
