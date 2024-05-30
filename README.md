<h1 align="center">
  Godork - Scrape Google search quickly
</h1>

<div align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/releases"><img src="https://img.shields.io/github/release/thd3r/godork.svg"></a>
  <a href="https://pypi.python.org/pypi/godork/"><img src="https://img.shields.io/pypi/v/godork.svg"></a>
  <a href="https://github.com/thd3r/godork/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/thd3r/godork?color=dark-green&label=issues%20fixed"></a>
</div>

# About

**Godork** is a tool that can quickly scrape Google search results using the [asyncio](https://docs.python.org/3/library/asyncio.html) library that uses cooperative multitasking combined with [aiohttp](https://docs.aiohttp.org) and with this tool you can extract links including their titles. This tool is also able to bypass the bans made by the provider

# Installation

**Godork** requires **python 3.8** or higher to install successfully

### Using Github repo

```sh
git clone https://github.com/thd3r/godork.git
cd codork
python3 setup.py install
```

### Using pip

```sh
pip install godork
```

# Usage

### This will display help for the tool. Here are all the switches it supports.

```sh
python godork.py -help
```

```console
Options:
  -help         show this help message and exit
  -version      show program's version number and exit
  -query QUERY  search query
  -sleep        use this option to prevent banning
  -proxy PROXY  http proxy to use with godork (eg http://127.0.0.1:8080) 
```

# Support

### Buy me a coffe

<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="thd3r" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff"></script>
