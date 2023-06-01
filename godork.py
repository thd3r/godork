#!/usr/bin/env python3

from __future__ import print_function

from aiohttp import ClientSession, ClientTimeout
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from datetime import datetime
from sys import argv
from re import findall

import requests
import asyncio
import time
import json
import os

def write_json(filename, data):
    try:
        if filename:
            filename = filename

        if '.' not in filename:
            filename = f"{filename}-{str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))}.json"
        
        if not filename:
            filename = f"{filename}-{str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))}.json"

        print(f"\n[\033[94mINF\033[0m] Saving results to file %s" % str(filename))
        with open(str(filename), "wt") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False) + os.linesep)
    except:
        print(f"[\033[91mERR\033[0m] Cannot save result to file: %s" % str(filename))

class OptionsArgs:
    
    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog="godork",
            usage=f"{argv[0]} [ --query [default arguments] ] [ arguments ]"
        )
        self.parser._optionals.title = "Options"
        self.parser.add_argument(
            "-q",
            "--query",
            type=str,
            action="store",
            required=True,
            help="search query"
        )
        self.parser.add_argument(
            "-p",
            "--page",
            type=int,
            action="store",
            default=1,
            help="specify number of pages"
        )
        self.parser.add_argument(
            "--hl",
            action="store",
            help="language"
        )
        self.parser.add_argument(
            "--gl",
            action="store",
            help="country of the search",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            action="store",
            default="godork",
            help="write output in JSONL(ines) format"
        )

        return
    
    def _options(self):
        args = self.parser.parse_args()
        return args

class Googledork:

    def __init__(self, query: str, page: int, hl, gl, output) -> None:
        self.base_url = "https://www.google.com/search"     # Base url for google dorks
        self.query = query
        self.page = page
        self.hl = hl
        self.gl = gl
        self.output = output
        
        self.data = []
        self.start_time = time.time()

        return 

    def params(self, q, p, hl, gl) -> dict:
        return {
            "q": q,          # query
            "hl": hl,        # language
            "gl": gl,        # country of the search
            "start": p       # parameter defines the maximum number of results to return
        }
    
    def regexp(self, text) -> list:
        return findall('"><a href="\/url\?q=(.*?)&amp;sa=U&amp;', text)
    
    async def aiorequest(self, url, params, headers):
        timeout = ClientTimeout(total=0)    # '0' value to disable timeout
        async with ClientSession() as session:
            async with session.get(url=url, params=params, headers=headers, timeout=timeout) as r:
                return await r.text()
            
    def isocode(self):
        html = requests.get("https://www.google.com", headers={"User-Agent": "godork/1.0.0"})
        soup = BeautifulSoup(html.text, "html.parser")

        return soup.html['lang']

    def title(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("h3")
        
    def links(self, i, html):
        link = self.regexp(html)
        return link[i]

    async def run(self):
        isocode = self.isocode()
        for i in range(self.page):
            html = await self.aiorequest(self.base_url, params=self.params(self.query, str(i*10), hl=isocode if not self.hl else self.hl, gl=isocode if not self.gl else self.gl), headers={"User-Agent": "godork/1.0.0"})
            for i, tag in enumerate(self.title(html)):
                self.data.append({
                    "title": tag.getText(),
                    "links": self.links(i, html)
                })
        
        for data in self.data:
            print(f"{data['title']} [\033[92m{data['links']}\033[0m]")
        
        if self.output:
            write_json(self.output, self.data)
        
        link = [x['links'] for x in self.data]
        print(f"[\033[94mINF\033[0m] Found {len(link)} links for {self.query} querys in {round(time.time() - self.start_time)} seconds")

class Godork(object):

    def __init__(self) -> None:
        self.engine = "Google"
        self.OptionsArgs = OptionsArgs()

        return

    def print_banner(self):
        banner = """\033[1m\033[92m
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r

\033[0m"""
        print(banner)

    def info(self, q, p):
        print(f"[\033[94mINF\033[0m] Engine  : {self.engine}")
        print(f"[\033[94mINF\033[0m] Query   : {q}")
        print(f"[\033[94mINF\033[0m] Page    : {p}\n")

        print("[\033[93mWRN\033[0m] Returns None if your IP address has been blocked by a search engine provider or some other reason.")
        print(f"[\033[94mINF\033[0m] Enumerating now for {q} querys\n")

    def run(self):
        self.print_banner()
        args = self.OptionsArgs._options()
        self.info(args.query, args.page)
        godork = Googledork(args.query, args.page, args.hl, args.gl, args.output)
        asyncio.run(godork.run())

if __name__ == '__main__':
    godork = Godork()
    godork.run()
