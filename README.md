<h1 align="left">
  Godork - Advanced & Fast Google Dorking Tool
</h1>

<div align="left">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/releases"><img src="https://img.shields.io/github/release/thd3r/godork.svg"></a>
  <a href="https://pypi.python.org/pypi/godork/"><img src="https://img.shields.io/pypi/v/godork.svg"></a>
  <a href="https://github.com/thd3r/godork/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/thd3r/godork?color=dark-green&label=issues%20fixed"></a>
</div>

```sh
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/  v2.5.4
 \_, /\___/\_,_/\___/_/ /_/\_\    latest
/___/                                                                                                            
           thd3r & societyprojects
```

**Godork** is a high-performance tool designed to scrape links and titles from Google search results using the [asyncio](https://docs.python.org/3/library/asyncio.html) library, which enables efficient cooperative multitasking. Combined with [aiohttp](https://docs.aiohttp.org), this tool allows you to quickly and reliably extract URLs along with their corresponding titles. Additionally, Godork is capable of bypassing restrictions imposed by network providers, ensuring uninterrupted access to search data

## ✨ Why Godork?

* ⚡ Blazing-fast performance using asynchronous HTTP requests (aiohttp)

* 🔍 Automated dork execution with support for lists, batches, and single queries

* 🌐 Proxy-ready: Bypass restrictions and stay anonymous with HTTP proxy integration

* 🕶️ Headless browser mode with Selenium to defeat CAPTCHAs and JS-based blocks

* 🔄 Self-updating via --update-tool flag and never run outdated tools again

* 🐳 Docker-compatible: Seamlessly containerize and deploy in any environment

## Resources
- [Requirements](#requirements)
- [Installation](#installation)
	- [Install with pip](#install-with-pip)
	- [Or clone from GitHub](#or-clone-from-github)
- [Options](#options)
- [Example Usage](#example-usage)
  - [Basic dorking](#basic-dorking)
  - [Batch mode](#batch-mode)
- [Help & Bugs](#help--bugs)
- [Contributors](#contributors-heart)
- [License](#license)
- [Support](#support)


## Requirements

```sh
# This is required for the pydub library
$ sudo apt install ffmpeg

# Check the version of the google-chrome browser
$ google-chrome --version

# If the browser version does not exist run this command
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt -f install
$ sudo dpkg -i google-chrome-stable_current_amd64.deb

# After that, take the version from your google-chrome browser and place it here
$ wget https://storage.googleapis.com/chrome-for-testing-public/{PUT_THAT_VERSION_HERE}/linux64/chromedriver-linux64.zip
$ unzip chromedriver-linux64.zip
$ cd chromedriver-linux64 
$ sudo mv chromedriver /usr/bin
```

## Installation

**Godork** requires **python 3.8** or higher to install successfully

### Install with pip:

```sh
pip install godork
```

### Or clone from GitHub:

```sh
git clone https://github.com/thd3r/godork.git
cd godork
pip install -r requirements.txt
python3 setup.py install
```

## Options

| Option            | Type         | Description                             	      |
|-------------------|--------------|------------------------------------------------|
| -v, --version     | Flag         | displays the current version of godork |
| -d, --dorks       | String       | single dork or file containing multiple dorks            |
| -p, --proxy       | String       | http proxy to use with godork (e.g. http://127.0.0.1:8080) |
| --debug           | Boolean      | show detailed logs and error for debugging |
| --retries         | Integer      | retries when request is blocked (default: 40) |
| --max-retries     | Integer      | max attempts to bypass protection mechanisms (default: 2) |
| --no-headless     | Boolean      | run in graphical mode when bypassing |
| --update-tool     | Boolean      | update godork to the latest version  |

## Example Usage

### Basic dorking:

```sh
godork --dorks "intitle:index.of site:example.com"
```

> [!WARNING]
> Developers assume no liability and are not responsible for any issue or damage.

### Batch mode:

```sh
godork --dorks dorks.txt --proxy http://127.0.0.1:8080 --no-headless
```

## Help & Bugs

If you are still confused or found a bug, please [open the issue](https://github.com/thd3r/godork/issues). All bug reports are appreciated, some features have not been tested yet due to lack of free time.

## Contributors :heart:

<p align="left">
<a href="https://github.com/societyprojects"><img src="https://avatars.githubusercontent.com/u/181974230?s=400&v=4" width="50" height="50" alt="" style="max-width: 100%;"></a>
</p>

## License

Licensed under the [MIT License](https://github.com/thd3r/godork/blob/main/LICENSE.md).

Contributions are welcome :) feel free to fork, suggest improvements, or submit pull requests.

## Support

<a href="https://www.buymeacoffee.com/thd3r" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
