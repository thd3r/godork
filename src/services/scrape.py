import re
import os
import time
import random

from aiohttp import ClientSession, TCPConnector

from src.utils.colors import Bgcolor
from src.utils.exceptions import GodorkNoData, GodorkMaxRetries
from src.utils.parse import get_query, get_page_num, set_page_num
from src.helpers.console import Console
from src.helpers.reports import Reports
from src.helpers.extractor import extract_pages, extract_data
from src.services.requester import Requester
from src.services.recaptcha import RecaptchaBypass

class Scraper:

    """
    The Scraper class is a sophisticated tool designed for scraping Google search results, efficiently managing retries, handling CAPTCHAs, and extracting valuable data like links and titles. 
    It provides both synchronous and asynchronous scraping capabilities, ensuring flexibility and robustness while interacting with Google's search engine.
    
    Key Features:

        1. Initialization (__init__):

            * The class initializes a number of key parameters like:

                - Dorks: A list of search queries (either from a file or input string).
                - Debugging and Proxy Settings: Configuration for debugging and using proxies.
                - Retries: Mechanism to retry failed requests with a configurable retry count and maximum retry limit.
                - Headless Mode: Configuration to run the scraper in headless mode for browser interactions.

            * The scraper utilizes several components for functionality:

                - Console: For logging and output management.
                - Reports: For generating detailed reports about the scraping process.
                - Requester: For handling the HTTP requests (both synchronous and asynchronous).
                - RecaptchaBypass: A service for bypassing CAPTCHA protections encountered during scraping.

        2. Parameter Construction (params):

            * This method generates the request parameters for querying Google search results, including:

                - q: The search query.
                - client: Randomly selecting a user agent string (chrome, firefox, ubuntu, etc.)
                - start: The page number for pagination.

        3. Asynchronous Connection Handling (reuse_connection):

            * This function manages retries when CAPTCHA protection is triggered on Google search results pages.
            * It calls the RecaptchaBypass.solve_captcha method to handle CAPTCHA challenges.
            * If CAPTCHA is detected, the method tries to bypass it by interacting with the page's reCAPTCHA service and retries the process for a set number of attempts.

        4. Fetching URLs (fetch_urls):

            * This method initiates an HTTP GET request to retrieve search result pages.
            * It handles various HTTP response codes:

                - 200 OK: Processes valid search results and extracts data.
                - 3xx Redirects: Detects CAPTCHA challenges and attempts to bypass them.
                - 4xx and 5xx Errors: Logs client and server errors.

            * It attempts to bypass reCAPTCHA challenges automatically when detected.
            * If the request fails, it retries a set number of times before throwing an error.

        5. Fetching Links (fetch_links):

            * This method handles the core logic of iterating through search queries (dorks) and fetching search result pages.
            * For each query, it sends requests to multiple pages (using the params method to adjust the page number) and attempts to extract links and titles from the result.
            * It also gracefully handles exceptions such as timeouts and CAPTCHA protection issues, retrying requests when necessary.

        6. Running the Scraper (run_with_async):

            * This method serves as the entry point for running the asynchronous scraper.
            * It starts by printing introductory messages, including warnings about using the scraper responsibly.
            * Using async with ClientSession, it establishes a session to interact with Google search, managing retries and exceptions along the way.
            * Once the scraping process completes, the session is closed, and the final report is saved.

    """

    def __init__(self, dorks, debug, proxy, retries, max_retries, headless_mode):
        self.base_url = "https://www.google.com/search"
    
        self.dorks = dorks.strip().splitlines() if not os.path.isfile(dorks) else open(dorks, 'r').read().strip().splitlines()
        self.debug = debug
        self.proxy = proxy
        self.retries = retries
        self.max_retries = max_retries
        self.headless = headless_mode

        self.console = Console()
        self.reports = Reports()
        self.requester = Requester()
        self.recaptcha_service = RecaptchaBypass(debug, headless_mode=headless_mode)

    def params(self, query, page):
        return {
            "q": query,
            "channel": "fs",
            "client": random.choice(["chrome", "firefox", "ubuntu", "gws"]),
            "start": page,
        }
    
    async def reuse_connection(self, session, url, retry_count=0, **kwargs):
        num_page = kwargs.get("num_page")

        if retry_count >= self.max_retries:
            raise GodorkMaxRetries("Maximum retries attempts reached for solving v2 protection")

        self.reports.logs_report("info", data="Initiating v2 bypass...")
        self.console.log_print("info", msg="Initiating v2 bypass...")

        response = await self.recaptcha_service.solve_captcha(url)

        if response is not None:
            target_url = response.current_url
            data_html = response.page_source

            try:
                last_page = extract_pages(data_html)
                self.reports.logs_report("info", data=f"Total known pages: {last_page}")
                self.console.log_print("info", msg=f"Total known pages: {last_page}")
            except IndexError:
                pass
            
            extract_data(data_html, reports=self.reports, metadata={"query": get_query(url), "num_page": set_page_num(num_page)})

            await self.fetch_urls(session, url=target_url, params=None)

            response.quit()
        else:
            self.reports.logs_report("info", data=f"Retrying bypass of v2 protection (attempt: {retry_count+1}) on page {set_page_num(num_page)}")
            self.console.log_print("info", msg=f"Retrying bypass of v2 protection (attempt: {retry_count+1}) on page {set_page_num(num_page)}")

            await self.reuse_connection(session, url, num_page=num_page, retry_count=retry_count + 1)

    async def fetch_urls(self, session, url, **kwargs):
        num_page = kwargs.get("params")["start"] if kwargs.get("params") is not None else get_page_num(url)
        i = 0

        while True:
            i += 1
            response = await self.requester.aioreqwest(
                session,
                method="GET",
                url=url,
                proxy=self.proxy,
                params=kwargs.get("params"),
                timeout=10,
                redirects=False
            )

            self.reports.logs_report("debug", data=f"Initiating request to {str(response.url)}")
            self.console.debugging(self.debug, msg=f"Initiating request to {str(response.url)}")

            self.reports.logs_report("debug", data=f"Getting response status {response.status}")
            self.console.debugging(self.debug, msg=f"Getting response status {response.status}")

            if "Google Search" not in re.findall("<title>(.*?)</title>", self.requester.response_dict["body"]):

                if response.status == 200:
                    try:
                        last_page = extract_pages(self.requester.response_dict["body"])
                        self.reports.logs_report("info", data=f"Total known pages: {last_page}")
                        self.console.log_print("info", msg=f"Total known pages: {last_page}")
                    except IndexError:
                        pass

                    extract_data(self.requester.response_dict["body"], reports=self.reports, metadata={"query": get_query(response.url), "num_page": set_page_num(num_page)})

                if 300 <= response.status <= 399 and "https://www.google.com/sorry/index" in response.headers["Location"]:
                    url_redirection = response.headers["Location"]

                    self.reports.logs_report("debug", data=f"Getting the redirect URL {url_redirection}")
                    self.console.debugging(self.debug, msg=f"Getting the redirect URL {url_redirection}")

                    self.reports.logs_report("warning", data="Requests were blocked due to provider-side protection")
                    self.console.log_print("warning", msg="Requests were blocked due to provider-side protection    ")
                    
                    self.reports.logs_report("warning", data=f"reCAPTCHA detected on the page {set_page_num(num_page)}")
                    self.console.debugging(self.debug, msg=f"reCAPTCHA detected on the page {set_page_num(num_page)}")

                    await self.reuse_connection(session, url=url_redirection, num_page=num_page, retry_count=0)

                if 400 <= response.status <= 499:
                    self.reports.logs_report("error", data=f"Failed to fetch request on page {set_page_num(num_page)} {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:Client error occurred")
                    self.console.log_print("error", msg=f"Failed to fetch request on page {set_page_num(num_page)} {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:Client error occurred")

                if 500 <= response.status <= 599:
                    self.reports.logs_report("error", data=f"Failed to fetch request on page {set_page_num(num_page)} {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:Server error occurred")
                    self.console.log_print("error", msg=f"Failed to fetch request on page {set_page_num(num_page)} {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:Server error occurred")

                break

            if i >= self.retries:
                raise GodorkMaxRetries("The request failed after reaching the maximum number of retries attempts")

            else:
                print(f"\r{self.console.out_log_format('warning', msg=f'Unexpected provider response. Retrying (request: {i})')}", flush=True, end="\r")
                    
    async def fetch_links(self, session, url):
        for query in self.dorks:
            self.reports.logs_report("info", data=f"{Bgcolor.BOLD}Starting enumeration for {query}{Bgcolor.DEFAULT}")
            self.console.log_print("info", msg=f"{Bgcolor.BOLD}Starting enumeration for {query}{Bgcolor.DEFAULT}")

            for i in range(0, 501, 10):
                self.console.debugging(self.debug, msg=f"Performing an HTTP GET request on page {set_page_num(i)}")
                self.reports.logs_report("info", data=f"Performing an HTTP GET request on page {set_page_num(i)}")

                try:
                    await self.fetch_urls(session, url=url, params=self.params(query=query, page=i))
                except GodorkMaxRetries as err:
                    self.reports.logs_report("warning", data=err)
                    self.console.log_print("warning", msg=err)
                    break
                except GodorkNoData as err:
                    self.reports.logs_report("info", data=err)
                    self.console.log_print("info", msg=err)
                    break
                except Exception as err:
                    self.reports.logs_report("error", data=err)
                    self.console.log_print("error", msg=err)
                    break

    async def run_with_async(self):
        print(self.console.text_format("info", msg="A high-speed scraper for collecting links and titles from Google search results"))
        print(self.console.text_format("warning", msg="Use with caution. You are responsible for your actions"))
        print(self.console.text_format("warning", msg="Developers assume no liability and are not responsible for any issue or damage"))

        time.sleep(1)

        async with ClientSession(connector=TCPConnector(ssl=False if self.proxy else True)) as session:
            try:
                await self.fetch_links(session, url=self.base_url)
            finally:
                await session.close()

        self.console.log_print("info", msg="Check the report in {}".format(self.reports.base_dir))