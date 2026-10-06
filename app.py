"""
Virtual RAW TCP/IP Printer Server (v1)
A lightweight desktop GUI emulator for testing network printer connections and raw print jobs.
Built with Python 3 standard library (Tkinter, Sockets, Threading).
"""

import socket
import threading
import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class VirtualPrinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual RAW Printer Server")
        self.root.geometry("860x660")
        self.root.minsize(700, 500)

        # Server State
        self.server_socket = None
        self.server_thread = None
        self.is_running = False
        self.received_jobs = []

        self._apply_styles()
        self._build_ui()

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Modern Dark Color Palette (Catppuccin inspired)
        self.bg_color = "#1e1e2e"
        self.card_bg = "#252538"
        self.accent_color = "#89b4fa"
        self.text_color = "#cdd6f4"
        self.subtext_color = "#a6adc8"
        self.success_color = "#a6e3a1"
        self.danger_color = "#f38ba8"

        self.root.configure(bg=self.bg_color)

        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=self.card_bg, foreground="#ffffff", font=("Segoe UI", 12, "bold"))
        style.configure("Title.TLabel", background=self.bg_color, foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 10, "bold"))

    def _build_ui(self):
        # Header / Title Bar
        header_frame = ttk.Frame(self.root, padding="15 15 15 5")
        header_frame.pack(fill="x")

        title_lbl = ttk.Label(header_frame, text="🖨️ Virtual RAW TCP/IP Printer Server", style="Title.TLabel")
        title_lbl.pack(side="left")

        desc_lbl = ttk.Label(header_frame, text="Listening on RAW_9100 socket for network print testing", foreground=self.subtext_color)
        desc_lbl.pack(side="left", padx=(15, 0), pady=(5, 0))

        # Control Panel Card
        control_card = ttk.Frame(self.root, style="Card.TFrame", padding="15")
        control_card.pack(fill="x", padx=15, pady=10)

        # Host / Bind IP
        ttk.Label(control_card, text="Bind Host/IP:", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.ip_entry = ttk.Entry(control_card, width=15)
        self.ip_entry.insert(0, "0.0.0.0")
        self.ip_entry.grid(row=0, column=1, sticky="w", padx=(0, 15), pady=5)

        # Port
        ttk.Label(control_card, text="Port:", style="Card.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 5), pady=5)
        self.port_entry = ttk.Entry(control_card, width=8)
        self.port_entry.insert(0, "9100")
        self.port_entry.grid(row=0, column=3, sticky="w", padx=(0, 20), pady=5)

        # Start / Stop Buttons
        self.btn_toggle = tk.Button(
            control_card, text="▶ Start Server", bg="#a6e3a1", fg="#11111b",
            font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=4,
            activebackground="#94e2d5", cursor="hand2", command=self.toggle_server
        )
        self.btn_toggle.grid(row=0, column=4, padx=5, pady=5)

        # Clear Logs Button
        btn_clear = tk.Button(
            control_card, text="🧹 Clear Logs", bg="#45475a", fg="#cdd6f4",
            font=("Segoe UI", 9), relief="flat", padx=10, pady=4,
            activebackground="#585b70", cursor="hand2", command=self.clear_logs
        )
        btn_clear.grid(row=0, column=5, padx=5, pady=5)

        # Status Label
        self.status_var = tk.StringVar(value="Status: STOPPED (Idle)")
        self.lbl_status = ttk.Label(control_card, textvariable=self.status_var, foreground="#f38ba8", style="Card.TLabel", font=("Segoe UI", 10, "bold"))
        self.lbl_status.grid(row=1, column=0, columnspan=6, sticky="w", pady=(10, 0))

        # Local IP helper
        local_ip = self._get_local_ip()
        ttk.Label(
            control_card,
            text=f"💡 Connection Target: IP 127.0.0.1 (local client) or {local_ip} (LAN / Network client), Port: 9100, Protocol: RAW TCP/IP",
            foreground="#fab387", style="Card.TLabel", font=("Segoe UI", 9)
        ).grid(row=2, column=0, columnspan=6, sticky="w", pady=(6, 0))

        # Main Body: Split Logs and Preview
        body_paned = ttk.PanedWindow(self.root, orient="horizontal")
        body_paned.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Left Pane: Connection & Job History
        left_frame = ttk.Frame(body_paned, style="Card.TFrame", padding="10")
        body_paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Activity & Connection Logs", style="Header.TLabel").pack(anchor="w", pady=(0, 5))

        self.log_text = scrolledtext.ScrolledText(
            left_frame, wrap="word", bg="#181825", fg="#cdd6f4",
            insertbackground="#ffffff", font=("Consolas", 9), relief="flat"
        )
        self.log_text.pack(fill="both", expand=True)

        # Right Pane: Received Print Data (Payload Preview)
        right_frame = ttk.Frame(body_paned, style="Card.TFrame", padding="10")
        body_paned.add(right_frame, weight=2)

        preview_header_frame = ttk.Frame(right_frame, style="Card.TFrame")
        preview_header_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(preview_header_frame, text="Raw Print Job Payload Preview", style="Header.TLabel").pack(side="left")

        self.payload_info_var = tk.StringVar(value="Waiting for incoming prints...")
        ttk.Label(preview_header_frame, textvariable=self.payload_info_var, foreground=self.subtext_color, style="Card.TLabel", font=("Segoe UI", 9)).pack(side="right")

        self.payload_text = scrolledtext.ScrolledText(
            right_frame, wrap="none", bg="#11111b", fg="#a6e3a1",
            insertbackground="#ffffff", font=("Courier New", 10), relief="flat"
        )
        self.payload_text.pack(fill="both", expand=True)

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def log_message(self, msg, level="INFO"):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{now}] [{level}] {msg}\n"
        self.root.after(0, self._append_log, formatted)

    def _append_log(self, text):
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)

    def log_payload(self, client_addr, data_bytes):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        size = len(data_bytes)

        # Decode with latin1 or utf-8 fallback
        try:
            text_preview = data_bytes.decode("latin1")
        except Exception:
            text_preview = data_bytes.decode("utf-8", errors="replace")

        header_banner = f"--- [JOB RECEIVED {now}] FROM {client_addr[0]}:{client_addr[1]} ({size} bytes) ---\n"
        footer_banner = f"\n--- [END OF JOB] ---\n\n"

        self.root.after(0, self._append_payload, header_banner + text_preview + footer_banner, f"Job from {client_addr[0]}:{client_addr[1]} ({size} B)")

    def _append_payload(self, full_text, info_summary):
        self.payload_info_var.set(info_summary)
        self.payload_text.insert(tk.END, full_text)
        self.payload_text.see(tk.END)

    def toggle_server(self):
        if not self.is_running:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        ip = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()

        if not port_str.isdigit():
            messagebox.showerror("Error", "Port must be a valid integer (1-65535)")
            return

        port = int(port_str)
        if port < 1 or port > 65535:
            messagebox.showerror("Error", "Port must be between 1 and 65535")
            return

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((ip, port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)
            self.is_running = True

            self.btn_toggle.config(text="⏹ Stop Server", bg="#f38ba8", fg="#11111b")
            self.status_var.set(f"Status: LISTENING on {ip}:{port} (RAW Socket)")
            self.lbl_status.config(foreground="#a6e3a1")
            self.ip_entry.config(state="disabled")
            self.port_entry.config(state="disabled")

            self.log_message(f"Virtual Printer Server started on {ip}:{port}", "START")
            self.log_message("Ready to receive print data from backend / network client.", "READY")

            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()

        except Exception as e:
            self.is_running = False
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            messagebox.showerror("Server Error", f"Failed to start server on port {port}:\n{str(e)}")
            self.log_message(f"Error starting server: {str(e)}", "ERROR")

    def _server_loop(self):
        while self.is_running:
            try:
                client_sock, client_addr = self.server_socket.accept()
            except socket.timeout:
                continue
            except Exception:
                break

            self.log_message(f"Incoming connection accepted from {client_addr[0]}:{client_addr[1]}", "CONNECT")
            client_handler = threading.Thread(
                target=self._handle_client,
                args=(client_sock, client_addr),
                daemon=True
            )
            client_handler.start()

    def _handle_client(self, client_sock, client_addr):
        client_sock.settimeout(10.0)
        received_chunks = []
        try:
            while True:
                data = client_sock.recv(4096)
                if not data:
                    break
                received_chunks.append(data)
        except socket.timeout:
            self.log_message(f"Connection from {client_addr} timed out or finished sending", "TIMEOUT")
        except Exception as e:
            self.log_message(f"Socket read from {client_addr} ended: {str(e)}", "INFO")
        finally:
            try:
                client_sock.close()
            except Exception:
                pass

            total_data = b"".join(received_chunks)
            if total_data:
                self.log_message(f"Received {len(total_data)} bytes from {client_addr[0]}:{client_addr[1]}", "SUCCESS")
                self.log_payload(client_addr, total_data)
            else:
                self.log_message(f"Connection closed by {client_addr} with 0 bytes (Handshake/Ping)", "PING")

    def stop_server(self):
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None

        self.btn_toggle.config(text="▶ Start Server", bg="#a6e3a1", fg="#11111b")
        self.status_var.set("Status: STOPPED (Idle)")
        self.lbl_status.config(foreground="#f38ba8")
        self.ip_entry.config(state="normal")
        self.port_entry.config(state="normal")
        self.log_message("Virtual Printer Server stopped.", "STOP")

    def clear_logs(self):
        self.log_text.delete("1.0", tk.END)
        self.payload_text.delete("1.0", tk.END)
        self.payload_info_var.set("Waiting for incoming prints...")
        self.log_message("Logs cleared.", "INFO")


def main():
    root = tk.Tk()
    app = VirtualPrinterApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_server(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
