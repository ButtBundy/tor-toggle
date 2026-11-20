# Tor Transparent Proxy Tray

A lightweight system tray utility for Linux (GTK) to quickly toggle a system-wide Tor transparent proxy using `iptables`.

## Prerequisites

### 1. System Packages
Ensure `tor`, `iptables`, and the required GTK/GObject bindings for the system tray icon are installed.

**Debian / Ubuntu / Kali:**
```bash
sudo apt update
sudo apt install -y tor iptables python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 python3-pip
```

### 2. Python Dependencies
Install `pystray` and `Pillow` (either via `apt` or `pip`):

```bash
pip install pystray pillow
# Or via apt:
# sudo apt install -y python3-pystray python3-pil
```

---

## Configuration

### 1. Configure Tor (`torrc`)
Because the toggle script redirects TCP traffic to port `9040` and DNS queries to port `5353`, you must enable Tor's `TransPort` and `DNSPort`.

Edit `/etc/tor/torrc`:
```bash
sudo nano /etc/tor/torrc
```

Add the following lines at the bottom of the file:
```text
TransPort 9040
DNSPort 5353
```

Disable the Tor service from starting automatically at boot (since the tray app manages it):
```bash
sudo systemctl disable --now tor
```

### 2. Passwordless `sudo` for the Toggle Script
Because `tor-tray.py` runs as a regular user in your desktop session, `private.sh` needs passwordless `sudo` permissions to control `systemctl` and `iptables`.

Create a dedicated sudoers rule:
```bash
sudo visudo -f /etc/sudoers.d/tor-tray
```

Add the following rules (replace `<YOUR_USERNAME>` with your actual Linux username):
```text
<YOUR_USERNAME> ALL=(ALL) NOPASSWD: /usr/bin/systemctl start tor, /usr/bin/systemctl stop tor
<YOUR_USERNAME> ALL=(ALL) NOPASSWD: /usr/sbin/iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040
<YOUR_USERNAME> ALL=(ALL) NOPASSWD: /usr/sbin/iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353
<YOUR_USERNAME> ALL=(ALL) NOPASSWD: /usr/sbin/iptables -t nat -D OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040
<YOUR_USERNAME> ALL=(ALL) NOPASSWD: /usr/sbin/iptables -t nat -D OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353
```
*(Note: Verify the exact paths of `systemctl` and `iptables` on your system using `which systemctl iptables`—on some distros they reside in `/bin/` or `/sbin/`).*

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ButtBundy/tor-toggle.git
   cd tor-toggle
   ```

2. **Install the scripts to `~/.local/bin`:**
   ```bash
   mkdir -p ~/.local/bin
   cp private.sh tor-tray.py ~/.local/bin/
   chmod +x ~/.local/bin/private.sh ~/.local/bin/tor-tray.py
   ```

3. **Run the tray icon:**
   ```bash
   ~/.local/bin/tor-tray.py &
   ```

---

## Optional: Autostart on Login

To launch the tray icon automatically when you log into your desktop environment, create an XDG autostart entry:

```bash
mkdir -p ~/.config/autostart
cat << 'EOF' > ~/.config/autostart/tor-tray.desktop
[Desktop Entry]
Type=Application
Name=Tor Tray
Comment=Toggle Tor Transparent Proxy
Exec=/home/$USER/.local/bin/tor-tray.py
Terminal=false
Categories=Network;Security;
EOF
```

---

## Usage
* **🟥 Red icon:** Tor proxy is **OFF** (direct connection).
* **🟩 Green icon:** Tor proxy is **ON** (TCP and DNS traffic routed through Tor).
* Click the tray icon and select **Enable Tor** / **Disable Tor** to switch states.
