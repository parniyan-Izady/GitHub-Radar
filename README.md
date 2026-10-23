<div align="center">

# 🛰️ GitHub Relationship Radar

**A fast, elegant, zero-dependency tool to uncover unfollowers, admirers, and mutual connections on GitHub.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Try%20Online-2ea44f?style=for-the-badge&logo=github)](https://parniyan-izady.github.io/GitHub-Radar/)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://parniyan-izady.github.io/GitHub-Radar/)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-0-orange.svg)](#-zero-dependencies)

<p align="center">
  <a href="https://parniyan-izady.github.io/GitHub-Radar/"><b>🚀 Try Live Web App</b></a> •
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-cli-usage">CLI</a> •
  <a href="#-license">License</a>
</p>

</div>

---

## 🌐 Live Web Application

No download or installation required! You can use the web version directly in your browser:

👉 **[https://parniyan-izady.github.io/GitHub-Radar/](https://parniyan-izady.github.io/GitHub-Radar/)**

---

## ✨ Features

- **❌ Unfollowers Detection**: Discover followed accounts that do not follow back.
- **⭐ Fan / Admirer Discovery**: Identify accounts following the user that are not followed back.
- **🤝 Mutual Connections**: Easily identify friends who follow each other.
- **🎨 Modern Dark Dashboard**: Built with glassmorphism, responsive cards, micro-interactions, and real-time live search.
- **📥 One-Click Export**: Save results anytime to CSV or JSON formats.
- **⚡ Zero Dependencies**: Powered entirely by the Python standard library (`http.server`, `urllib`) and vanilla web technologies.
- **🌐 Dual Mode**: Works either via local Python backend or as a 100% client-side web application (hosted on GitHub Pages).

---

## 🚀 Quick Start (Local Run)

### 1. Web Application via Local Server

#### On Windows:
Double-click `run.bat` or run:
```powershell
py server.py
```
Then open [http://localhost:8000](http://localhost:8000) in your browser.

#### On macOS / Linux:
```bash
python3 server.py
```
Then open [http://localhost:8000](http://localhost:8000).

---

### 💻 CLI Usage

You can also run analysis directly in your terminal:

```bash
# Basic scan
python cli.py torvalds

# With optional GitHub Token (increases rate limit to 5,000 req/hr)
python cli.py <username> --token ghp_xxxxxxxxxxxxxxxxxxxx

# Export non-followers directly to CSV
python cli.py <username> --csv unfollowers.csv
```

---

## 🔑 GitHub API Rate Limits

GitHub provides public access with the following allowances:
- **Unauthenticated**: 60 requests/hour (~6,000 accounts per hour).
- **With Personal Access Token**: 5,000 requests/hour (~500,000 accounts per hour).

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
