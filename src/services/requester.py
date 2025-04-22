from src.utils.user_agents import random_agent

class Requester:

    """
    The Requester class is a Python utility designed for making HTTP requests with customizable options for both synchronous and asynchronous operations. 
    It simplifies sending requests with custom headers, proxies, cookies, and additional parameters, while also handling both standard and asynchronous HTTP methods.

    Key Features:

        1. Initialization (__init__):

            * The class initializes a default set of HTTP headers, including a User-Agent string (which is randomly chosen), Accept, Accept-Language, and Referer. 
              These headers are typically used to simulate real user traffic, helping to avoid detection by web servers or bot protection mechanisms.
            * It also initializes an empty dictionary, response_dict, to store response content asynchronously.

        2. HTTP Request (Synchronous) - reqwest:

            * This method sends a synchronous HTTP request using the session.request() function from the requests library.
            * It takes various arguments:

                - method: The HTTP method (e.g., GET, POST).
                - url: The target URL for the request.
                - Additional keyword arguments (kwargs) include optional parameters such as proxies, request parameters (params), timeouts, cookies, custom headers, and the ability to allow redirects.

            * The method sends the request and returns the response object.
            * This method is ideal for situations where blocking operations (synchronous requests) are acceptable.

        3. HTTP Request (Asynchronous) - aioreqwest:

            * This method allows for asynchronous HTTP requests using aiohttp, making it more suitable for high-performance web scraping or API interactions that require non-blocking calls.
            * The function accepts similar parameters as the synchronous version, with the main difference being the use of async with to handle the asynchronous nature of the request.
            * Upon receiving the response, it updates response_dict with the body content of the response, allowing asynchronous access to the data. 
              The function then returns the response object, providing an efficient way to handle multiple requests concurrently.
            * This method is ideal for situations requiring non-blocking I/O operations, such as when dealing with large-scale web scraping or API calls.
    
    The class leverages both requests for traditional synchronous requests and aiohttp for asynchronous tasks, offering flexibility depending on the needs of the application.

    """

    def __init__(self):
        self.headers = {
            "User-Agent": str(random_agent),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
        }
        self.response_dict = {}

    def reqwest(self, session, method, url, **kwargs):
        response = session.request(
            method=method,
            url=url,
            proxies=kwargs.get("proxy"),
            params=kwargs.get("params"),
            timeout=kwargs.get("timeout"),
            cookies=kwargs.get("cookies"),
            headers=self.headers if not kwargs.get("headers") else kwargs.get("headers"),
            allow_redirects=kwargs.get("redirects")
        )
        return response

    async def aioreqwest(self, session, method, url, **kwargs):
        async with session.request(
            method=method,
            url=url,
            proxy=kwargs.get("proxy"),
            params=kwargs.get("params"),
            timeout=kwargs.get("timeout"),
            cookies=kwargs.get("cookies"),
            headers=self.headers if not kwargs.get("headers") else kwargs.get("headers"),
            allow_redirects=kwargs.get("redirects")
        ) as response:
            self.response_dict.update({"body": await response.text()})
            return response