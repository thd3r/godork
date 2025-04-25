#!/usr/bin/env python3

import asyncio

from .utils.colors import Bgcolor
from .helpers.console import Console
from .helpers.options import OptionParser
from .services.version import check_version
from .services.scrape import Scraper

def main():
    check_version()

    args = OptionParser.argument_parser()

    if len(args.dorks) < 1:
        print(f"""{Bgcolor.RED}error{Bgcolor.DEFAULT}: the following required arguments were not provided:
  --dorks <DORKS>
              
usage: godork --dorks <DORKS>

For more information, try 'godork --help'""")
        return
    
    scrape = Scraper(
        dorks=args.dorks,  
        proxy=args.proxy,
        debug=args.debug,
        retries=args.retries,
        max_retries=args.max_retries, 
        headless_mode=args.no_headless
    )
    
    try:
        asyncio.run(scrape.run_with_async())
    except KeyboardInterrupt:
        print(f"\r{Console().text_format('info', msg='We appreciate your use of our tool ;) Goodbye!')}")

if __name__ == '__main__':
    main()