<h1 align="center">
  Godork - Scrape Google search quickly
</h1>

<h1 align="center">
  <img src="static/godork-logo.png" alt="godork" width="200px">
  <br>
</h1>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation-instructions">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#running-godork">Running godork</a> •
  <a href="#notes">Notes</a> • 
  <a href="https://github.com/thd3r">Follow me</a>
</p>

`godork` can scrape results from google searches quickly by using the [asyncio](https://docs.python.org/3/library/asyncio.html) library which uses **cooperative multitasking** in combination with [aiohttp](https://docs.aiohttp.org)

# Features

<h1 align="center">
  <img src="https://raw.githubusercontent.com/thd3r/godork/main/static/godork-run.png" alt="godork" width="700px">
  <br>
</h1>

 - Simple and modular code base making it easy to contribute.
 - Fast scanner
 - Scrape Google search titles and links quickly

# Installation Instructions

`godork` requires **python 3.8** or higher to install successfully. Run the following command to get the repo:

```sh
git clone https://github.com/thd3r/godork.git && python3 -m pip install -r requirements.txt
```

# Usage

```sh
python godork.py -h
```

This will display help for the tool. Here are all the switches it supports.

```console
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r


usage: godork.py [ --query [default arguments] ] [ arguments ]

scrape Google search quickly

Options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        search query
  -p PAGE, --page PAGE  specify number of pages
  --hl HL               language
  --gl GL               country of the search
  -o OUTPUT, --output OUTPUT
                        write output in JSONL(ines) format  
```

# Running godork

### Scrape

It will run its tool to scrape titles and links from google search

```console
comming soon
```

# Notes
