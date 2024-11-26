<h1 align="left">
  Godork - Scrape Google search quickly
</h1>

<div align="left">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/releases"><img src="https://img.shields.io/github/release/thd3r/godork.svg"></a>
  <a href="https://pypi.python.org/pypi/godork/"><img src="https://img.shields.io/pypi/v/godork.svg"></a>
  <a href="https://github.com/thd3r/godork/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/thd3r/godork?color=dark-green&label=issues%20fixed"></a>
</div>

```
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/  v2.0.0
 \_, /\___/\_,_/\___/_/ /_/\_\    latest
/___/                                                                                                            
        thd3r & societyprojects
```

**Godork** is a fast tool to scrape links and titles from google search results using [asyncio](https://docs.python.org/3/library/asyncio.html) library which uses cooperative multitasking combined with [aiohttp](https://docs.aiohttp.org)  and with this tool you can extract links including their titles. This tool is also able to bypass restrictions imposed by providers

## Resources
- [Requirements](#requirements)
- [Installation](#installation)
	- [from Pypi](#from-pypi)
	- [from GitHub](#from-github)
- [Options](#options)
- [Usage](#usage)
	- [Basic Usage](#basic-usage)
- [Help & Bugs](#help--bugs)
- [Contributors](#contributors-heart)
- [License](#license)
- [Support](#support)


## Requirements

```
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

### from Pypi

```sh
pip install godork
```

### from Github

```sh
git clone https://github.com/thd3r/godork.git
cd codork
python3 setup.py install
```

## Options

Here are all the options it supports.

| Options             	| Description                                    	|
|------------------	|------------------------------------------------	|
| -d, --dorks       | single dork or file containing dorks            |
| -p, --proxy       | http proxy to use with godork (eg http://127.0.0.1:8080) |
| --no-headless     | run in graphical mode when bypassing |
| --update-tools    | update godork to the latest version  |

# Usage

### Basic Usage

```sh
godork --dorks site:*.com
```

> [!WARNING]
> Developers assume no liability and are not responsible for any issue or damage.

## Help & Bugs

If you are still confused or found a bug, please [open the issue](https://github.com/thd3r/godork/issues). All bug reports are appreciated, some features have not been tested yet due to lack of free time.

## Contributors :heart:

<p align="left">
<a href="https://github.com/societyprojects"><img src="https://avatars.githubusercontent.com/u/181974230?s=400&v=4" width="50" height="50" alt="" style="max-width: 100%;"></a>
</p>

## License

Godork is distributed under [MIT License](https://github.com/thd3r/godork/blob/main/LICENSE.md).

<img src="https://img.shields.io/badge/license-MIT-000000.svg?style=for-the-badge">

## Support

<a href="https://www.buymeacoffee.com/thd3r" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>