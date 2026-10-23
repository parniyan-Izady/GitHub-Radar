<div align="center">

# 🛰️ GitHub Relationship Radar

**A fast, elegant, zero-dependency tool to uncover unfollowers, admirers, and mutual connections on GitHub.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Ready-brightgreen)](https://pages.github.com/)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-0-orange.svg)](#-zero-dependencies)

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-cli-usage">CLI</a> •
  <a href="#-github-pages-hosting">GitHub Pages</a> •
  <a href="#-license">License</a>
</p>

</div>

---

## ✨ Features

- **❌ Unfollowers Detection**: Discover users you follow who do not follow you back.
- **⭐ Fan / Admirer Discovery**: Spot people who follow you, but you haven't followed back.
- **🤝 Mutual Connections**: Easily identify friends who follow each other.
- **🎨 Modern Dark Dashboard**: Built with glassmorphism, responsive cards, micro-interactions, and real-time live search.
- **📥 One-Click Export**: Save results anytime to CSV or JSON formats.
- **⚡ Zero Dependencies**: Powered entirely by the Python standard library (`http.server`, `urllib`) and vanilla web technologies.
- **🌐 Dual Mode**: Works either via local Python backend or as a 100% client-side web application (compatible with GitHub Pages).

---

## 🚀 Quick Start

### 1. Web Application (Recommended)

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

## 🌐 Deploy to GitHub Pages (1-Click Free Hosting)

Because `index.html` is 100% self-contained and communicates directly with the public GitHub REST API:

1. Push this repository to GitHub.
2. Go to **Settings > Pages**.
3. Under **Branch**, select `main` (or `master`) and folder `/ (root)`.
4. Click **Save**.
5. Your analyzer will be live online on `https://<your-username>.github.io/<repo-name>/`!

---

## 🔑 GitHub API Rate Limits

GitHub provides public access with the following allowances:
- **Unauthenticated**: 60 requests/hour (~6,000 accounts per hour).
- **With Personal Access Token**: 5,000 requests/hour (~500,000 accounts per hour).

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
