<h1 align="center">
  Godork - Scrape Google search quickly
</h1>

<div align="center">
  <img src="https://raw.githubusercontent.com/thd3r/godork/master/assets/images/godork-logo.png" alt="godork" width="300px">
</div>

<div align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/releases"><img src="https://img.shields.io/github/release/thd3r/godork.svg"></a>
  <a href="https://pypi.python.org/pypi/godork/"><img src="https://img.shields.io/pypi/v/godork.svg"></a>
  <a href="https://github.com/thd3r/godork/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/thd3r/godork?color=dark-green&label=issues%20fixed"></a>
  <a href="https://github.com/thd3r/godork/tree/master?tab=readme-ov-file#contributing"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</div>

# About

**godork** can scrape results from google searches quickly by using the [asyncio](https://docs.python.org/3/library/asyncio.html) library which uses **cooperative multitasking** in combination with [aiohttp](https://docs.aiohttp.org) and with this tool you can extract links including their titles. This tool is also able to bypass prohibitions made by providers

# Installation

### **godork** requires **python 3.8** or higher to install successfully. Run the following command to get the repo:

```sh
git clone https://github.com/thd3r/godork.git && python3 setup.py install
```

### Using pip

```sh
pip3 install godork
```

# Usage

```sh
python3 godork.py -help
```

### This will display help for the tool. Here are all the switches it supports.


```console
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.2.0 - @thd3r

usage: godork [ -query [default arguments] ] [ arguments ] 

Options:
  -help         show this help message and exit
  -version      show program's version number and exit
  -query QUERY  search query
  -sleep        use this option to prevent banning
  -proxy PROXY  http proxy to use with godork (eg http://127.0.0.1:8080) 
```

# Documentation

Documentation is available at https://thd3r.github.io

# Contributing

Contributions are welcome! If you want to contribute to **godork** don't forget to Fork the repository

# Support

### Support me on 

<a href="https://coindrop.to/thd3r" target="_blank">
  <img src="https://coindrop.to/embed-button.png" style="border-radius: 10px; height: 57px !important;width: 200px !important;" alt="Coindrop.to me"></img>
</a>
