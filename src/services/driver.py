import undetected_chromedriver as uc

from src.utils.user_agents import random_agent

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeService

class SeleniumDriver:

    """
    The SeleniumDriver class is designed to manage the creation and configuration of a Selenium WebDriver instance for automated web browsing. 
    It utilizes undetected-chromedriver (uc) to handle interactions with Chrome in a way that minimizes the chance of detection by websites using anti-bot mechanisms.

    Key Features:

        1. Initialization (__init__):

            * The class accepts a headless_mode argument that determines whether the browser will run in headless mode (without a visible UI).
            * Initializes a driver attribute set to None at the start.

        2. Context Manager (__enter__):

            * When entering the context (via a with statement), the class configures the Chrome browser by setting up ChromeService with an automatically downloaded driver using ChromeDriverManager.
            * Configures the Chrome options for the WebDriver:

                - Disables automation flags to avoid detection (--disable-blink-features=AutomationControlled).
                - Disables unnecessary features like extensions and GPU usage for better performance.
                - Sets a custom user-agent string (likely to simulate a real browser environment).
                - Optionally enables headless mode based on the headless_mode flag.
                - Creates a Chrome WebDriver instance (uc.Chrome), applies the configurations, and sets a page load timeout of 10 seconds.
                - Returns the WebDriver instance for use within the with block.

        3. Exit (__exit__):

            * The __exit__ method is a placeholder that ensures proper cleanup and exit behavior when leaving the context. 
              Currently, it does nothing but could be expanded for proper resource management (e.g. closing the driver).
              
    """

    def __init__(self, headless_mode:bool):
        self.headless = headless_mode
        self.driver = None

    def __enter__(self):
        chrome_service = ChromeService(ChromeDriverManager().install())

        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--user-agent={random_agent}")

        if self.headless:
            options.add_argument("--headless=new")

        self.driver = uc.Chrome(service=chrome_service, options=options)
        self.driver.set_page_load_timeout(10)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
