<p align="center">
  <img src="assets/banner.svg" alt="Virtual Printer V1 Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Protocol-RAW_TCP%2FIP_Socket-2563EB?style=flat-square" alt="Socket">
  <img src="https://img.shields.io/badge/Port-Port_9100_Standard-10B981?style=flat-square" alt="Port 9100">
  <img src="https://img.shields.io/badge/Standard-ESC%2FPOS_Emulation-0891B2?style=flat-square" alt="ESC/POS">
  <img src="https://img.shields.io/badge/Dependencies-Zero_External_Libs-orange?style=flat-square" alt="Zero Libs">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-gray?style=flat-square" alt="License"></a>
</p>

## Overview

Testing Point of Sale (POS) and Enterprise Resource Planning (ERP) receipt printing routines typically demands physical thermal printer hardware, wasting rolls of paper and slowing automated software release cycles. 

Virtual-Printer-V1 is a lightweight desktop network printer emulator written in Python. It listens as a RAW TCP/IP socket server on **Port 9100** (the standard JetDirect / RAW print port), captures incoming document streams in real time, and renders print payloads directly to your screen with zero external dependencies.

---

## Core Capabilities

- **Standard Port 9100 Server**: Binds to standard RAW TCP/IP printing ports, accepting streams from any POS software or network print driver.
- **Zero-Dependency Core**: Built purely on Python socket and Tkinter standard libraries, running immediately on any workstation.
- **Real-Time Stream Inspector**: Displays received byte streams and ASCII text feeds with live connection status indicators.
- **Payload Archiving**: Automatically logs received print jobs into timestamped text files for regression comparison.

---

## Quickstart

```bash
git clone https://github.com/MasterPandaa/Virtual-Printer-V1.git
cd Virtual-Printer-V1
python printer_server.py
```

Send a test stream from PowerShell:
```powershell
$client = New-Object System.Net.Sockets.TcpClient('127.0.0.1', 9100)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$writer.WriteLine("--- TEST RECEIPT ---")
$writer.WriteLine("Item: Coffee")
$writer.WriteLine("Total: $4.50")
$writer.Flush()
$client.Close()
```

---

## License

This project is licensed under the [MIT License](LICENSE).
