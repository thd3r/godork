#!/usr/bin/env python3

import os
import re
import sys
import time
import json
import random
import urllib
import argparse
import subprocess

from datetime import datetime
from tempfile import gettempdir
from urllib.parse import urlparse, unquote, parse_qs

try:
    import pydub
    import asyncio
    import speech_recognition

    from bs4 import BeautifulSoup
    from rich.progress import Progress
    from aiohttp import TCPConnector, ClientSession

    from selenium import webdriver
    from selenium.webdriver import ChromeService
    from selenium.webdriver import ChromeOptions
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
except ImportError:
    print(f"[\033[34mINF\033[0m] Downloading the required dependencies...")

    required_packages = {
        "bs4": "0.0.2",
        "rich": "13.9.4",
        "pydub": "0.25.1",
        "aiohttp": "3.10.10",
        "asyncio": "3.4.3",
        "selenium": "4.26.1",
        "SpeechRecognition": "3.11.0",
        "webdriver-manager": "4.0.2"
    }
    
    for package, version in required_packages.items():
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
    
    exit(0)

class Bgcolors:

    DEFAULT  = '\033[0m'
    WARNING  = '\033[33m'
    PURPLE   = '\033[35m'
    GREEN    = '\033[32m'
    BLUE     = '\033[34m'
    CYAN     = '\033[36m'
    RED      = '\033[31m'

class GodorkBase:

    def __init__(self):
        self.current_version = "v2.0.5"

        self.response_dict = {}
        self.log_time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    def print_banner(self, status):
        banner = f"""
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/  {self.current_version}
 \_, /\___/\_,_/\___/_/ /_/\_\    {status}
/___/                                                                                                            
        thd3r & societyprojects
"""
        print(banner)

    def log_print(self, status:str, msg:str):
        print(self.log_format(status, msg))

    def log_format(self, status:str, msg:str):
        if status.lower() == "info":
            detailed_info = f"{Bgcolors.CYAN}{self.log_time}{Bgcolors.DEFAULT}  [{Bgcolors.BLUE}INF{Bgcolors.DEFAULT}]  {msg}"
            return detailed_info

        if status.lower() == "error":
            detailed_error = f"{Bgcolors.CYAN}{self.log_time}{Bgcolors.DEFAULT}  [{Bgcolors.RED}ERR{Bgcolors.DEFAULT}]  {msg}"
            return detailed_error

        if status.lower() == "debug":
            detailed_debug = f"{Bgcolors.CYAN}{self.log_time}{Bgcolors.DEFAULT}  [{Bgcolors.PURPLE}DBG{Bgcolors.DEFAULT}]  {msg}"
            return detailed_debug

        if status.lower() == "warning":
            detailed_warning = f"{Bgcolors.CYAN}{self.log_time}{Bgcolors.DEFAULT}  [{Bgcolors.WARNING}WRN{Bgcolors.DEFAULT}]  {msg}"
            return detailed_warning

        if status.lower() not in ["info", "debug", "error", "warning"]:
            self.log_print(status="error", msg="status=REQUIRED args required with msg:{}".format(msg))
            exit(1)

    async def release_version(self):
        async with ClientSession() as session:
            try:
                _ = await self.aiorequester(session, method="GET", url="https://api.github.com/repos/thd3r/godork/releases/latest", timeout=10, headers={"User-Agent": f"godork{self.current_version}"})
                datajson = json.loads(self.response_dict["body"])
                return datajson["tag_name"], datajson["body"]
            except:
                return self.current_version, None

    async def check_for_updates(self):
        release_version, _ = await self.release_version()
        if release_version is not None and self.current_version < release_version:
            self.print_banner(status=f"{Bgcolors.RED}outdated{Bgcolors.DEFAULT}")
        if release_version is not None and self.current_version == release_version:
            self.print_banner(status=f"{Bgcolors.GREEN}latest{Bgcolors.DEFAULT}")
        if release_version is None:
            self.print_banner(status=f"{Bgcolors.RED}outdated{Bgcolors.DEFAULT}")

    async def download_file_updates(self, **kwargs):
        try:
           async with ClientSession() as session:
                async with session.request(method="GET", url="https://raw.githubusercontent.com/thd3r/godork/refs/heads/main/v2/godork.py", timeout=10, headers={"User-Agent": f"godork{self.current_version}"}) as response:
                    if response.status != 200:
                        print(f"[{Bgcolors.RED}ERR{Bgcolors.DEFAULT}] Cannot find package with version {kwargs.get('release_version')}")
                        return
                    
                    total_size = int(response.headers.get('content-length', 0))
                    
                    with Progress() as progress:
                        task = progress.add_task("[cyan]Downloading...", total=total_size)
                        
                        with open(__file__, "wb") as f:
                            async for chunk in response.content.iter_chunked(1024):
                                f.write(chunk)
                                progress.update(task, advance=len(chunk))
                                await asyncio.sleep(0.3)
                    print(f"[{Bgcolors.BLUE}INF{Bgcolors.DEFAULT}] godork sucessfully updated {self.current_version} -> {kwargs.get('release_version')} ({Bgcolors.GREEN}latest{Bgcolors.DEFAULT})")
        except Exception as err:
            print(f"[{Bgcolors.RED}ERR{Bgcolors.DEFAULT}] Failed to download update... reason:{err}")
    
    def update_tools(self):
        release_version, body = asyncio.run(self.release_version())
        
        if release_version is not None and self.current_version < release_version:
            print(f"[{Bgcolors.BLUE}INF{Bgcolors.DEFAULT}] Release version available {release_version}")
            print(f"[{Bgcolors.BLUE}INF{Bgcolors.DEFAULT}] Updating tools...")

            asyncio.run(self.download_file_updates(release_version=release_version))
            print(f"{Bgcolors.PURPLE}{body}{Bgcolors.DEFAULT}")
        if release_version is not None and self.current_version == release_version:
            print(f"[{Bgcolors.BLUE}INF{Bgcolors.DEFAULT}] godork {self.current_version} is up to date")
        if release_version is None:
            print(f"[{Bgcolors.RED}ERR{Bgcolors.DEFAULT}] Cant find the latest version of godork")

    def write_file(self, filename, data):
        self.log_print(status="info", msg=f"Saving results to file {filename}")
        with open(filename, "wt") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False) + os.linesep)

    def reports(self, data):
        dirs = f"{gettempdir()}/godork/reports"
        try:
            os.makedirs(dirs)
        except FileExistsError:
            dirs = dirs

        filename = f"{dirs}/{str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))}_godork.json"
        self.write_file(filename, data=data)

    async def aiorequester(self, session, method, url, **kwargs):
        async with session.request(
            method=method,
            url=url,
            proxy=kwargs.get("proxy"),
            params=kwargs.get("params"),
            timeout=kwargs.get("timeout"),
            cookies=kwargs.get("cookies"),
            headers=kwargs.get("headers"),
            allow_redirects=kwargs.get("redirects")
        ) as response:
            self.response_dict.update({"body": await response.text()})
            return response

class GodorkService(GodorkBase):

    def __init__(self, headless):
        GodorkBase.__init__(self)
        self.headless = headless

    def chromedriver_service(self):
        """Initialize the ChromeDriverService which will return a driver object."""
        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chromeoptions(headless=self.headless))
            driver.set_page_load_timeout(10)
            return driver
        except Exception as err:
            raise Exception(err)

    def chromeoptions(self, headless):
        options = ChromeOptions()
        if not headless:
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
        else:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")

        return options

    def recaptcha_service(self, driver):
        # Switch to the iframe containing the recaptcha
        iframe_inner = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        driver.switch_to.frame(iframe_inner)

        time.sleep(1)

        # Click on the recaptcha
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".rc-anchor-content"))
            ).click()
        except TimeoutException:
            raise TimeoutError("Failed to click recaptcha")

        # Switch back to the default frame
        driver.switch_to.default_content()

        time.sleep(1)

        # Get the new iframe for audio
        iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'recaptcha')]")
        driver.switch_to.frame(iframe)

        # Click on the audio button
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recaptcha-audio-button"))
            ).click()
        except TimeoutException:
            raise TimeoutError("Failed to click audio button")

        time.sleep(1)

        # Wait for the audio source to load
        try:
            audio_source = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-source"))
            )
            src = audio_source.get_attribute("src")
        except TimeoutException:
            raise TimeoutError("Failed to load audio source")

        # Download the audio to the temp folder
        path_to_mp3 = f"{gettempdir()}/{str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))}.mp3"
        path_to_wav = f"{gettempdir()}/{str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))}.wav"
        
        urllib.request.urlretrieve(src, path_to_mp3)

        # Convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")

        sample_audio = speech_recognition.AudioFile(path_to_wav)
        r = speech_recognition.Recognizer()

        try:
            with sample_audio as source:
                audio = r.record(source)
            # Recognize the audio
            key = r.recognize_google(audio)
        except (speech_recognition.exceptions.UnknownValueError, speech_recognition.exceptions.RequestError):
            raise Exception("Failed to recognize")

        # Input the key
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(key.lower())
        except TimeoutException:
            raise TimeoutError("Failed to input key")

        # Submit the key
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(Keys.RETURN)
        except TimeoutException:
            raise TimeoutError("Failed to submit key")

        # Wait for a short period to allow the recaptcha to process the input
        time.sleep(2)
        
        self.log_print(status="info", msg="Successfully bypassed recaptcha protection")
        
        # Delete temporary files
        try:
            os.remove(path_to_mp3)
            os.remove(path_to_wav)
        except Exception:
            raise Exception("Failed to delete temporary files")
    
    def solve_captcha(self, url):
        try:
            driver = self.chromedriver_service()
            driver.get(url)
            self.recaptcha_service(driver)
            return driver
        except (Exception, TimeoutError) as err:
            self.log_print(status="error", msg=f"Failed to bypass recaptcha protection reason:{err}")
            driver.quit()
            return None

class GodorkRunner(GodorkService):

    def __init__(self, dorks, proxy, headless):
        GodorkService.__init__(self, headless)
        self.basename = "godork"
        self.base_url = "https://www.google.com/search"
    
        self.dorks = dorks.strip().splitlines() if not os.path.isfile(dorks) else open(dorks, 'r').read().strip().splitlines()
        self.proxy = proxy
        self.headless = headless

        self.data_output = []
    
    def set_qwerys(self, qwerys):
        filtered_qwerys = [qwery.split(":") if ":" in qwery else qwery.strip() for qwery in qwerys]
        result = {}
        
        for newqwery in filtered_qwerys:
            if isinstance(newqwery, list):
                result[newqwery[0]] = newqwery[1]
            else:
                result[newqwery] = None
        
        return result if result else None

    def get_page_num(self, url):
        parsed = urlparse(unquote(url))
        query_params = parse_qs(parsed.query)

        return query_params["start"][0]
    
    def set_page_num(self, num):
        num = num // 10
        num += 1
        return num

    def params(self, qwery, page):
        return {
            "q": qwery,
            "client": random.choice(["chrome", "firefox", "ubuntu", "gws", "godork"]),
            "start": page,
        }
    
    def get_title(self, html):
        datatitle = []
        soup = BeautifulSoup(html, "html.parser")

        for title in soup.find_all("h3"):
            if "Google Search Console" not in title.getText():
                datatitle.append(title.getText().strip())
        
        return datatitle
    
    def get_links(self, html):
        datalinks = []
        links = re.findall(r'\"><a href=\"\/url\?q=(.*?)&amp', html)

        for link in links:
            if link.startswith(("http", "https")):
                datalinks.append(unquote(link.strip()))
            if not link.startswith(("http", "https")):
                continue
    
        return datalinks
    
    def get_links_from_driver(self, html):
        soup = BeautifulSoup(html, "html.parser")
        datalinks = []

        for tag in soup.find_all("a", href=True):
                link = tag.get("href")
                if not link.startswith(("http", "https")):
                    continue
                if link.startswith(("http", "https")):
                    for qwery in self.dorks:
                        qwerys_dict = self.set_qwerys(qwery.split(" "))

                        if qwerys_dict is not None and isinstance(qwerys_dict, dict):
                            for key, val in qwerys_dict.items():
                                if isinstance(key, str) and isinstance(val, str):
                                    val = val.replace("*", "") if "*" in val else val
                                    if key.lower() == "site" and val in urlparse(unquote(link)).netloc:
                                        datalinks.append(link)
                                    
        return datalinks

    def collect_data(self, html, **kwargs):
        numpage = kwargs.get("numpage")

        titles = self.get_title(html)
        links = self.get_links(html)
            
        if len(titles) > 0 and len(links) > 0:
            self.log_print(status="info", msg=f"Found {len(titles)} titles and {len(links)} links on page {self.set_page_num(numpage)}")

            self.data_output.append({
                "title": titles,
                "links": links
            })

            for i, title in enumerate(titles):
                try:
                    print(f"{title} [{Bgcolors.GREEN}{links[i]}{Bgcolors.DEFAULT}]")
                except IndexError:
                    pass

    def collect_data_from_driver(self, html, **kwargs):
        numpage = kwargs.get("numpage")

        titles = self.get_title(html)
        links = self.get_links_from_driver(html)

        if len(titles) > 0 and len(links) > 0:
            self.log_print(status="info", msg=f"Found {len(titles)} titles and {len(links)} links on page {self.set_page_num(numpage)}")

            self.data_output.append({
                "title": titles,
                "links": links
            })

            for i, title in enumerate(titles):
                try:
                    print(f"{title} [{Bgcolors.GREEN}{links[i]}{Bgcolors.DEFAULT}]")
                except IndexError:
                    pass

    def no_data(self, html):
        try:
            return len(self.get_title(html)) < 1
        except:
            return False
        
    async def reuse_connection(self, session, url, **kwargs):
        self.log_print(status="info", msg="Trying to bypass recaptcha protection")

        response = self.solve_captcha(url)

        if response is not None:
            target_url = response.current_url
            datahtml = response.page_source

            numpage = kwargs.get("numpage")

            if self.no_data(datahtml) == True:
                raise Exception(f"No data can be collected on page {self.set_page_num(numpage)}")
            else:
                self.collect_data_from_driver(datahtml, numpage=numpage)

            response.quit()

            await self.fetch_urls(session, url=target_url, params=None)
            
    async def fetch_urls(self, session, url, **kwargs):
        response = await self.aiorequester(
            session=session,
            method="GET",
            url=url,
            proxy=self.proxy,
            params=kwargs.get("params"),
            timeout=10,
            headers={"User-Agent": f"godork/{self.current_version}", "Referer": "https://www.google.com/"},
            redirects=False
        )

        numpage = kwargs.get("params")["start"] if kwargs.get("params") is not None else self.get_page_num(url)

        if response.status == 200:
            if self.no_data(self.response_dict["body"]) == True:
                raise Exception(f"No data can be collected on page {self.set_page_num(numpage)}")
            else: self.collect_data(self.response_dict["body"], numpage=numpage)

        if response.status != 200 and "https://www.google.com/sorry/index" in response.headers["Location"]:
            url_redirection = response.headers["Location"]
            self.log_print(status="warning", msg="The provider has set protections to block our requests")
            self.log_print(status="warning", msg="Recaptcha has been detected!")
            await self.reuse_connection(session, url=url_redirection, numpage=numpage)
            
    async def fetch_links(self, session, url):
        for qwery in self.dorks:
            self.log_print(status="info", msg=f"{Bgcolors.PURPLE}Enumerating now for {qwery}{Bgcolors.DEFAULT}")
            for i in range(0, 501, 10):
                try:
                    await self.fetch_urls(session, url=url, params=self.params(qwery=qwery, page=i))
                except Exception as err:
                    self.log_print(status="error", msg=err)
                    break

        if len(self.data_output) > 0:
            self.reports(data={
                "godork": {
                    "data": {
                        "title": [self.data_output[i]["title"] for i in range(len(self.data_output))],
                        "links": [self.data_output[i]["links"] for i in range(len(self.data_output))]
                    }
                }
            })

    async def run_with_async(self):
        await self.check_for_updates()
        
        print(f"[{Bgcolors.BLUE}INF{Bgcolors.DEFAULT}] A fast tool to scrape every link and title from google search results")
        print(f"[{Bgcolors.WARNING}WRN{Bgcolors.DEFAULT}] Use with caution. You are responsible for your actions")
        print(f"[{Bgcolors.WARNING}WRN{Bgcolors.DEFAULT}] Developers assume no liability and are not responsible for any issue or damage.")

        async with ClientSession(connector=TCPConnector(ssl=False if self.proxy else True)) as session:
            await self.fetch_links(session, url=self.base_url)

def main():
    parser = argparse.ArgumentParser(
        prog="godork",
        usage="%(prog)s [OPTIONS] "
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s 2.0.5",
    )
    parser.add_argument(
        "-d",
        "--dorks",
        action="store",
        default="",
        help="single dork or file containing dorks"
    )
    parser.add_argument(
        "-p",
        "--proxy",
        action="store",
        help="http proxy to use with godork (eg http://127.0.0.1:8080)"
    )
    parser.add_argument(
        "--no-headless",
        action="store_false",
        default=True,
        help="run in graphical mode when bypassing"
    )
    parser.add_argument(
        "--update-tools",
        action="store_true",
        default=False,
        help="update godork to the latest version"
    )

    args = parser.parse_args()

    godork = GodorkRunner(dorks=args.dorks, proxy=args.proxy, headless=args.no_headless)

    if args.update_tools:
        godork.update_tools()
        return
    
    if len(godork.dorks) < 1:
        print(f"""error: the following required arguments were not provided:
  --dorks <DORKS>
              
usage: godork --dorks <DORKS>

For more information, try 'godork --help'""")
        return
    
    asyncio.run(godork.run_with_async())

if __name__ == '__main__':
    main()
