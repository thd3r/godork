#!/usr/bin/env python3

from __future__ import print_function

from aiohttp import ClientSession, TCPConnector # v3.9.3
from argparse import ArgumentParser 
from bs4 import BeautifulSoup # v0.0.2
from tempfile import gettempdir
from datetime import datetime
from re import findall

import asyncio # v3.4.3
import random
import time
import json
import os

__version__ = "1.2.1"

class OptionsArgs(object):
    
    def __init__(self):
        self.parser = ArgumentParser(
            prog="godork",
            add_help=False,
            usage="%(prog)s [ -query [default arguments] ] [ arguments ] "
        )
        self.parser._optionals.title = "Options"
        self.parser.add_argument(
            "-help",
            action="help",
            help="show this help message and exit"
        )
        self.parser.add_argument(
            "-version",
            action="version",
            version=f"%(prog)s {__version__}"
        )
        self.parser.add_argument(
            "-query",
            type=str,
            required=True,
            help="search query"
        )
        self.parser.add_argument(
            "-sleep",
            action="store_true",
            default=False,
            help="use this option to prevent banning"
        )
        self.parser.add_argument(
            "-proxy",
            default=None,
            help="http proxy to use with godork (eg http://127.0.0.1:8080)"
        )

    def _options(self):
        args = self.parser.parse_args()
        return args

class Output(object):

    def __init__(self):
        try:
            self.dirs = os.makedirs(f"{gettempdir()}/godork/output/")
        except FileExistsError:
            self.dirs = f"{gettempdir()}/godork/output/"

    def write_json(self, data):
        filename = f"{self.dirs}{str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))}_godork.json"
        if len(data) > 1:
            print(f"[\033[94mINF\033[0m] Saving results to file %s" % str(filename))
            with open(str(filename), "wt") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False) + os.linesep)
        else: pass

class Dorks(Output):

    def __init__(self, query, sleep, proxy):
        super().__init__()
        self.base_url = "https://www.google.com/search" # Initialize base URL
        self.query = query
        self.sleep = sleep
        self.proxy = proxy

        self.nums = random.randint(8,12)
        self.data = []

    def random_words(self):
        words = [
            "supergodork",
            "godork",
            "awesomegodork",
            "batman",
            "spiderman",
            "superhero",
            "ironman",
            "powergodork",
            "superpowergodork",
            "iloveyou",
            "mygodork",
            "yourgodork",
            "anonymous",
            "python",
            "aiorequest",
        ]
        return random.choice(words).strip()

    def regexp(self, html):
        return findall('"><a href="\/url\?q=(.*?)&amp;sa=U&amp;', html)

    def params(self, q, p):
        return {
            "q": q,                 
            "start": p, # parameter defines the maximum number of results to return
        }
    
    def get_title(self, html):
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find_all("h3")
        if len(title) > 1 and len(html) > 40000:
            return title
        print(f"[\033[91mERR\033[0m] Could not find many matches for query: {self.query}")
    
    def get_links(self, i, html):
        links = self.regexp(html)
        if len(links) > i and len(html) > 40000:
            return links[i]
        
    def get_data(self, response):
        for i, html in enumerate(response):
            titles, links = self.get_title(html), self.get_links(i, html)
            if titles and links:
                for title in titles:
                    self.data.append({
                        "title": title.getText(),
                        "links": links
                    })
                    print(f"{title.getText()} [\033[92m{links}\033[0m]")
            else:
                break

    def banned(self, html):
        ban = False
        if len(html) < 40000 and "CAPTCHA" in html:
            ban = True
        return ban
    
    def should_sleep(self):
        if self.sleep:
            time.sleep(self.nums)
        else: pass
    
    async def aiorequest(self, url, params):
        async with ClientSession(connector=TCPConnector(ssl=False if self.proxy else True)) as session:
            self.should_sleep() # Sleep to prevent banning
            async with session.get(
                url=url,
                params=params,
                proxy=self.proxy,
                allow_redirects=False,
                headers={
                    "User-Agent": f"{self.random_words()}/1.2.0",
                    "Referer": "https://www.google.com/"
                },
                ) as resp:
                html = await resp.text()
                if self.banned(html):
                    raise RuntimeError("[\033[91mERR\033[0m] Your IP address has been blocked by a search engine provider")
                if resp.status != 200:
                    raise Exception("[\033[91mERR\033[0m] Your IP address has been blocked by a search engine provider")
                return html
    
    async def run(self):
        start_time = time.time()
        tasks =  [self.aiorequest(url=self.base_url, params=self.params(q=self.query, p=i)) for i in range(0, 71, 10)]
        response = await asyncio.gather(*tasks)

        self.get_data(response)
        self.write_json(self.data)

        link = [x['links'] for x in self.data]
        total_time = time.time() - start_time
        print(f"[\033[94mINF\033[0m] Found {len(link)} links in {total_time:.3f} seconds")

class Godork(OptionsArgs):

    def __init__(self):
        super().__init__()

    def print_banner(self):
        banner = f"""
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v{__version__} - @thd3r
"""
        print(banner)

    def run(self):
        self.print_banner()
        args = self._options()
        print(f"[\033[94mINF\033[0m] Enumerating now for {args.query} querys")
        godork = Dorks(args.query, args.sleep, args.proxy)
        try:
            asyncio.run(godork.run())
        except (Exception, RuntimeError) as err:
            print(err)

def main():
    godork = Godork()
    godork.run()

if __name__== '__main__':
    main()