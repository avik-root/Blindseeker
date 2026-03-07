<p align="center">
  <img src="static/img/logo.png" alt="Blindseeker Logo" width="120">
  <h1 align="center">BLINDSEEKER</h1>
  <p align="center">
    <strong>Advanced Username Enumeration & Digital Forensics Tool</strong>
  </p>
  <p align="center">
    <code>v1.0.0</code> · <code>Shadow Protocol</code> · Developed by <strong>MintFire</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/version-1.0.0-00ff88?style=flat-square&logo=hackthebox&logoColor=white" alt="Version">
    <img src="https://img.shields.io/badge/python-3.9+-0088ff?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/flask-3.1-red?style=flat-square&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/platforms-329+-aa66ff?style=flat-square" alt="Platforms">
    <img src="https://img.shields.io/badge/tor-supported-7d4698?style=flat-square&logo=torproject&logoColor=white" alt="Tor">
    <img src="https://img.shields.io/badge/license-restricted-ffaa00?style=flat-square" alt="License">
  </p>
</p>

---

## ⚡ Overview

**Blindseeker** is an enterprise-grade, Flask-based username enumeration tool engineered for **law enforcement**, **digital forensics investigators**, and **authorized security teams**. It performs comprehensive username search and reconnaissance across **329+ platforms** in **24 categories** — social media, developer platforms, gaming, finance, forums, shopping, travel, fitness, cybersecurity, blockchain, regional networks, and more.

Built with a focus on **operational security**, **high-speed concurrent scanning**, and **forensics-grade reporting capabilities**.

> **⚠️ LEGAL DISCLAIMER:** This tool is designed exclusively for authorized law enforcement investigations, digital forensics, and sanctioned security operations. Unauthorized use may violate applicable laws. Users are solely responsible for ensuring compliance with all relevant legislation and regulations in their jurisdiction.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **329+ Platforms** | Social, developer, gaming, creative, finance, forums, shopping, travel, fitness, cybersecurity, blockchain, regional, career, photography, podcast, food |
| **Dual Interface** | Professional Flask web UI with real-time WebSocket updates + CLI with Rich terminal output |
| **Tor Network** | Native SOCKS5 routing through Tor for anonymous scanning with circuit renewal |
| **Proxy Support** | HTTP/HTTPS/SOCKS4/SOCKS5 proxy rotation with health checking |
| **Rate Limiting** | Per-domain adaptive token bucket rate limiter with 429 backoff |
| **Multi-Format Export** | JSON, CSV, **PDF** (branded forensics reports), XML, HTML, XLSX |
| **Async Engine** | `aiohttp`-powered async scanning with configurable concurrent workers |
| **Real-Time Updates** | WebSocket-based live scan progress with per-platform results |
| **Forensics Reports** | PDF reports with timestamps, case IDs, investigator metadata |
| **User-Agent Rotation** | Randomized browser fingerprints to reduce detection |
| **Category Filtering** | Scan specific platform categories (social, developer, gaming, etc.) |

---

## 📋 Platform Categories

| Category | Count | Examples |
|----------|-------|---------|
| Social Media | 22+ | Instagram, X/Twitter, Facebook, TikTok, Reddit, LinkedIn, Mastodon |
| Developer | 22+ | GitHub, GitLab, Stack Overflow, LeetCode, HackerRank, npm, PyPI |
| Gaming | 11+ | Steam, Twitch, Chess.com, Roblox, Epic Games |
| Creative | 14+ | Behance, Dribbble, DeviantArt, ArtStation, Figma |
| Media | 8+ | YouTube, Vimeo, Dailymotion, Imgur |
| Music | 7+ | Spotify, SoundCloud, Bandcamp, Last.fm |
| Business | 12+ | LinkedIn, ProductHunt, Fiverr, Patreon, Linktree |
| Finance | 4+ | TradingView, CoinMarketCap |
| Education | 9+ | Duolingo, Coursera, Khan Academy, ResearchGate |
| Forum | 10+ | Hacker News, Wikipedia, XDA Developers |
| Other | 40+ | TryHackMe, Hack The Box, MyAnimeList, OpenSea |

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- pip
- (Optional) Tor service for anonymous scanning

### Setup

```bash
# Clone repository
git clone https://github.com/your-org/blindseeker.git
cd blindseeker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

---

## 💻 Usage

### Web Interface

```bash
# Start the web server
python app.py

# Or via CLI
python cli.py web --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000` in your browser.

**Web UI Features:**
- **Dashboard** — Scan stats, quick scan widget, platform overview, system status
- **New Scan** — Advanced search with category filters, timeout, and worker configuration
- **Results** — Tabular view with filtering, sorting, and multi-format export
- **History** — Browse all past scans with rescan capabilities
- **Settings** — Tor toggle, proxy management, rate limit tuning

### Command-Line Interface

```bash
# Basic scan
python cli.py search johndoe

# Scan with Tor anonymization
python cli.py search johndoe --tor

# Scan specific categories
python cli.py search johndoe -c social -c developer

# Custom timeout and workers
python cli.py search johndoe --timeout 20 --workers 100

# Export as PDF forensics report
python cli.py search johndoe --format pdf --investigator "Agent Smith" --case-id "CASE-2026-0042"

# Use proxy
python cli.py search johndoe --proxy socks5://127.0.0.1:9050

# Use proxy file
python cli.py search johndoe --proxy-file proxies.txt

# Export to specific file
python cli.py search johndoe -o reports/target_report.json

# List supported platforms
python cli.py platforms

# Show help
python cli.py --help
python cli.py search --help
```

### REST API

```bash
# Start scan
curl -X POST http://127.0.0.1:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "timeout": 15}'

# Get scan status
curl http://127.0.0.1:5000/api/scan/<scan_id>/status

# Export results
curl http://127.0.0.1:5000/api/export/<scan_id>/pdf \
  -o report.pdf

# Get platform list
curl http://127.0.0.1:5000/api/platforms

# Get engine stats
curl http://127.0.0.1:5000/api/stats
```

---

## 🔐 Security Features

| Feature | Description |
|---------|-------------|
| **Tor Integration** | Route all traffic through Tor SOCKS5 proxy with circuit renewal |
| **Proxy Rotation** | Round-robin or random rotation across multiple proxies |
| **Rate Limiting** | Adaptive per-domain throttling prevents ban/block |
| **UA Rotation** | Randomized User-Agent headers per request |
| **SSL Flexibility** | Handles non-standard SSL configurations |
| **Health Checks** | Automatic proxy health monitoring with dead proxy removal |
| **Adaptive Backoff** | Automatic rate reduction on 429 responses |
| **Session Isolation** | Independent scan sessions with no cross-contamination |

---

## 📊 Export Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| **JSON** | `.json` | API integration, programmatic processing |
| **CSV** | `.csv` | Spreadsheet analysis, database import |
| **PDF** | `.pdf` | Formal forensics reports with metadata, tables, branding |
| **XML** | `.xml` | System interoperability, structured data exchange |
| **HTML** | `.html` | Web-viewable reports, email attachments |
| **XLSX** | `.xlsx` | Multi-sheet Excel reports (Summary + Found + All Results) |

### PDF Report Contents
- Branded header with Blindseeker logo
- Scan metadata (target, timestamps, duration)
- Investigator and case ID fields
- Found profiles table with URLs and response times
- Investigator notes section
- Legal footer

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```ini
# Server
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
SECRET_KEY=your-secret-key

# Tor
TOR_ENABLED=false
TOR_SOCKS_HOST=127.0.0.1
TOR_SOCKS_PORT=9050

# Proxy
PROXY_ENABLED=false
PROXY_FILE=proxies.txt

# Scan
MAX_WORKERS=50
REQUEST_TIMEOUT=15
RATE_LIMIT_PER_SECOND=10
MAX_RETRIES=2

# Export
DEFAULT_EXPORT_FORMAT=json
EXPORT_DIR=exports
```

### Proxy File Format (`proxies.txt`)

```
http://proxy1.example.com:8080
https://proxy2.example.com:443
socks4://proxy3.example.com:1080
socks5://proxy4.example.com:9050
```

---

## 🏗️ Architecture

```
blindseeker/
├── app.py                 # Flask application + SocketIO
├── cli.py                 # Click CLI interface
├── config.py              # Configuration management
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── core/
│   ├── __init__.py
│   ├── engine.py          # Main enumeration orchestrator
│   ├── scanner.py         # Platform scanner (async)
│   ├── platforms.py       # 200+ platform definitions
│   ├── proxy.py           # Proxy manager
│   ├── tor.py             # Tor integration
│   ├── rate_limiter.py    # Token bucket rate limiter
│   └── exporter.py        # Multi-format exporter
├── templates/
│   ├── base.html          # Base layout
│   ├── dashboard.html     # Command center
│   ├── search.html        # Scan interface
│   ├── results.html       # Results viewer
│   ├── history.html       # Scan history
│   └── settings.html      # Configuration
└── static/
    ├── css/style.css       # Dark cybersecurity theme
    └── js/main.js          # SocketIO client
```

---

## 🔧 Detection Methods

Blindseeker uses multiple detection strategies:

| Method | Description |
|--------|-------------|
| **Status Code** | HTTP 200 = found, 404 = not found |
| **Response Body** | Search for "not found" indicators in page content |
| **Redirect** | Profile exists if no redirect occurs |
| **JSON Field** | Check API JSON responses for existence fields |

---

## 📄 Legal & Compliance

> **This tool is strictly intended for:**
> - Authorized law enforcement investigations
> - Licensed digital forensics operations
> - Court-ordered surveillance activities
> - Authorized penetration testing engagements
> - Missing person investigations by authorized agencies
> - Counter-terrorism intelligence operations

**The developers assume no liability for misuse.** All users must comply with applicable local, national, and international laws regarding digital investigations.

---

## 🙋 Support

For operational support, technical issues, or feature requests:
- Open an issue on the repository
- Contact the development team through authorized channels

---

<p align="center">
  <sub>Built with ◉ by <strong>MintFire</strong></sub><br>
  <sub><code>v1.0.0</code> • FOR AUTHORIZED USE ONLY</sub>
</p>
