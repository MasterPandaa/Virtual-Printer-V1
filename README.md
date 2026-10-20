# Virtual Printer V1 — Lightweight RAW TCP/IP Printer Emulator

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](#)
[![Protocol](https://img.shields.io/badge/Protocol-RAW%20TCP%2FIP%20(Port%209100)-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A portable desktop GUI application that emulates a network receipt/document printer listening on standard **RAW TCP/IP socket port 9100** (JetDirect protocol).

Built for **Software Engineers**, **QA/SDET Automation**, and **DevOps** teams to test POS receipt dispatching, invoice printers, ESC/POS command sequences, and backend socket print drivers without requiring physical printer hardware.

---

## Overview

Developing and testing printing workflows in staging environments often introduces friction due to hardware maintenance, network cabling, or paper consumption. Virtual Printer V1 emulates socket reception locally:

- **Hardware-Free Testing**: Intercepts print streams over localhost or LAN during development and automated CI/CD runs.
- **Real-Time Stream Diagnostics**: Logs connection handshakes, remote client IPs/ports, payload sizes, and connection durations.
- **Multithreaded Socket Engine**: Background worker threads accept incoming socket connections without stalling the UI.
- **Dual Stream Decoding**: Decodes textual data (UTF-8, Latin-1) alongside raw binary ESC/POS command streams.
- **Zero External Dependencies**: Implemented entirely with Python's standard library (`socket`, `threading`, `tkinter`) with no `pip install` required.

---

## Technical Features

1. **RAW 9100 Socket Listener**: Configurable port binding (default `9100`) handling multiple sequential client connections.
2. **Payload Inspector**: Real-time display of incoming print streams with automatic character-set fallback decoding.
3. **Session Diagnostics**: Instant inspection of client endpoints, timestamped transactions, and socket state logs.
4. **Dark Desktop Interface**: Ergonomic Tkinter interface with single-click start/stop and clear-log operations.

---

## Quickstart

### Prerequisites

- Python 3.8+ with `tkinter` support (standard on Windows and macOS Python installers).
- *On Linux (Debian/Ubuntu)*: `sudo apt install python3-tk`

### Installation & Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MasterPandaa/Virtual-Printer-V1.git
   cd Virtual-Printer-V1
   ```

2. **Launch the emulator**:
   ```bash
   python app.py
   ```
   *(On Windows, you can also double-click `run.bat`)*

3. **Send a test print via TCP socket**:
   ```powershell
   # Windows PowerShell test
   $client = New-Object System.Net.Sockets.TcpClient("127.0.0.1", 9100)
   $stream = $client.GetStream()
   $writer = New-Object System.IO.StreamWriter($stream)
   $writer.WriteLine("Hello from Virtual Printer Test!")
   $writer.Flush()
   $client.Close()
   ```

---

## Project Structure

```text
Virtual-Printer-V1/
├── app.py                      # Application entry point, Tkinter UI & socket handler
├── run.bat                     # Windows quickstart batch launcher
├── README.md                   # Project documentation
└── LICENSE                     # MIT License
```

---

## License

This project is licensed under the [MIT License](LICENSE).
