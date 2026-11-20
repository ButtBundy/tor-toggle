#!/bin/bash

STATE_FILE="/tmp/tor_enabled"

tor_on() {
    touch "$STATE_FILE"
    sudo systemctl start tor
    sleep 3
    sudo iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040
    sudo iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353
}

tor_off() {
    rm -f "$STATE_FILE"
    sudo systemctl stop tor
    sudo iptables -t nat -D OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040 2>/dev/null || true
    sudo iptables -t nat -D OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353 2>/dev/null || true
}

if [ -f "$STATE_FILE" ]; then
    tor_off
else
    tor_on
fi
