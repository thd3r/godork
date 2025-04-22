#!/usr/bin/env python3

import asyncio

from pathlib import Path

from utils.colors import Bgcolor
from helpers.console import Console
from helpers.options import OptionParser
from services.update import UpdateTool
from services.scrape import Scraper

def main():
    BASE_DIR = Path(__file__).resolve().parent
    
    updater = UpdateTool()
    updater.check_version()

    args = OptionParser.argument_parser()
    scrape = Scraper(dorks=args.dorks, debug=args.debug, proxy=args.proxy, retries=args.retries, max_retries=args.max_retries, headless_mode=args.no_headless)

    if args.update_tool:
        updater.update_tool(BASE_DIR)
        return

    if len(args.dorks) < 1:
        print(f"""{Bgcolor.RED}error{Bgcolor.DEFAULT}: the following required arguments were not provided:
  --dorks <DORKS>
              
usage: godork --dorks <DORKS>

For more information, try 'godork --help'""")
        return
    
    try:
        asyncio.run(scrape.run_with_async())
    except KeyboardInterrupt:
        print(f"\r{Console().text_format('info', msg='We appreciate your use of our tool ;) Goodbye!')}")

if __name__ == '__main__':
    main()