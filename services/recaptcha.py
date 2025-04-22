import os
import time
import pydub
import urllib
import asyncio
import speech_recognition

from tempfile import gettempdir
from datetime import datetime

from services.driver import SeleniumDriver
from helpers.console import Console
from helpers.reports import Reports
from utils.colors import Bgcolor
from utils.exceptions import GodorkException, GodorkTimeout

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RecaptchaBypass:

    """
    The RecaptchaBypass class is an advanced solution for bypassing reCAPTCHA v2 challenges, specifically designed for handling audio-based CAPTCHAs. 
    Using Selenium, undetected-chromedriver, and various media-processing libraries, it automates the process of solving the CAPTCHA by downloading, converting, and transcribing audio challenges. 
    The class also incorporates detailed logging, debugging, and error handling to ensure smooth and efficient operation, even in environments with strict bot protection.

    Key Features:
    
        1. Initialization (__init__):

            * The class is initialized with debug and headless_mode flags, allowing control over the debugging output and 
              whether the browser runs in headless mode (without a visible UI).
            * It also initializes instances of Console and Reports to handle logging and reporting during execution.

        2. reCAPTCHA Handling (recaptcha_service):

            * This asynchronous method automates the process of solving a reCAPTCHA by interacting with the CAPTCHA iframe, clicking the checkbox, and navigating through the audio challenge.
            * The method performs several actions in sequence:

                - Switching to the reCAPTCHA iframe.
                - Clicking the reCAPTCHA checkbox and waiting for it to become clickable.
                - Switching back to the default frame.
                - Locating the audio challenge iframe and clicking the audio button.
                - Retrieving the audio source URL.
                - Downloading, converting, and decoding the audio to extract the CAPTCHA key.
                - Entering the transcribed key and submitting the response.

        3. Audio CAPTCHA Processing:

            * The handle_audio_captcha method is responsible for downloading the audio file, converting it from MP3 to WAV format, and 
              decoding it to extract the text. The transcription is handled using the speech_recognition library.
            * Temporary files (MP3 and WAV) are cleaned up after processing to ensure no unnecessary files remain on the system.

        4. Audio Download and Conversion:

            * The download_audio method downloads the audio file to a temporary directory.
            * The convert_mp3_to_wav method converts the downloaded MP3 audio to WAV format using the pydub library.

        5. Transcription and Cleanup:

            * The audio is transcribed using the Google Speech Recognition API. If transcription fails, appropriate exceptions are raised.
            * Temporary audio files are cleaned up after the process, ensuring proper resource management.

        6. Error Handling:

            * If any CAPTCHA challenge cannot be completed, or if the IP address is blocked, relevant error messages are logged and displayed. 
              The system gracefully handles exceptions like NoSuchElementException and TimeoutException, ensuring robust operation.

        7. IP Blocking Detection (is_blocked):

            * This method checks if the IP address has been blocked by detecting the "captcha body text" indicating a block. 
              It helps in identifying if reCAPTCHA protection is preventing further attempts.

        8. Solve CAPTCHA (solve_captcha):

            * This asynchronous method accepts a URL, launches a Selenium WebDriver, and 
              attempts to solve the CAPTCHA on the page using the previously mentioned methods.
            * The process is wrapped in a try-except block to handle errors gracefully, with reports and console logs to provide real-time feedback.

    """

    def __init__(self, debug:bool, headless_mode:bool):
        self.console = Console()
        self.reports = Reports()

        self.debug = debug
        self.headless = headless_mode

        self.wait = None
    
    async def recaptcha_service(self, driver):
        # Switching to iframe containing reCAPTCHA
        self.reports.logs_report("debug", data="Switching to iframe containing reCAPTCHA")
        self.console.debugging(self.debug, msg="Switching to iframe containing reCAPTCHA")

        try:
            iframe_inner = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
            driver.switch_to.frame(iframe_inner)
        except NoSuchElementException:
            raise GodorkException("Failed to locate reCAPTCHA iframe element")

        time.sleep(1)

        # Click on the recaptcha
        self.reports.logs_report("debug", data="Clicking the reCAPTCHA checkbox")
        self.console.debugging(self.debug, msg="Clicking the reCAPTCHA checkbox")

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".rc-anchor-content"))
            ).click()
        except TimeoutException:
            raise GodorkTimeout("Failed to click reCAPTCHA checkbox")

        # Switch back to the default frame
        driver.switch_to.default_content()

        time.sleep(1)

        # Locating audio challenge iframe
        self.reports.logs_report("debug", data="Locating audio challenge iframe")
        self.console.debugging(self.debug, msg="Locating audio challenge iframe")

        try:
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'recaptcha')]")
            driver.switch_to.frame(iframe)
        except NoSuchElementException:
            raise GodorkException("Failed to locate reCAPTCHA iframe element")

        # Click on the audio button
        self.reports.logs_report("debug", data="Clicking the audio button")
        self.console.debugging(self.debug, msg="Clicking the audio button")

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recaptcha-audio-button"))
            ).click()
        except TimeoutException:
            raise GodorkTimeout("Failed to click audio button")

        time.sleep(1)

        # Wait for the audio source to load
        self.reports.logs_report("debug", data="Waiting for the audio source to load completely")
        self.console.debugging(self.debug, msg="Waiting for the audio source to load completely")

        try:
            audio_source = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-source"))
            )
            src = audio_source.get_attribute("src")
            self.reports.logs_report("debug", data=f"Getting the audio URL {src}")
            self.console.debugging(self.debug, msg=f"Getting the audio URL {src}")
        except TimeoutException:
            raise GodorkTimeout("Failed to load audio source")

        # Download, convert, and decode audio reCAPTCHA
        try:
            key = await self.handle_audio_captcha(src)
        except (speech_recognition.exceptions.UnknownValueError, speech_recognition.exceptions.RequestError):
            raise GodorkException("Failed to recognize")

        # Input the key
        self.reports.logs_report("debug", data="Entering the transcribed phrase")
        self.console.debugging(self.debug, msg="Entering the transcribed phrase")

        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(key.lower())
        except TimeoutException:
            raise GodorkTimeout("Failed to input key")

        # Submit the key
        self.reports.logs_report("debug", data="Submitting the phrase")
        self.console.debugging(self.debug, msg="Submitting the phrase")

        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(Keys.RETURN)
        except TimeoutException:
            raise GodorkTimeout("Failed to submit key")

        # Waiting briefly for reCAPTCHA to process the input
        self.reports.logs_report("debug", data="Waiting briefly for reCAPTCHA to process the input")
        self.console.debugging(self.debug, msg="Waiting briefly for reCAPTCHA to process the input")

        time.sleep(4)

        if self.is_blocked(driver):
            return

        self.console.log_print("info", msg="Successfully bypassed v2 protection")
    
    async def handle_audio_captcha(self, src_url):
        """Main handler to download, convert and decode audio CAPTCHA"""
        mp3_path, wav_path = self.get_temp_audio_paths()

        self.download_audio(src_url, mp3_path)
        self.convert_mp3_to_wav(mp3_path, wav_path)

        try:
            phrase = await self.async_decode_audio(wav_path)
        finally:
            # Delete temporary files
            self.reports.logs_report("debug", data="Deleting temporary audio files")
            self.console.debugging(self.debug, msg="Deleting temporary audio files")
            self.cleanup_temp_files(mp3_path, wav_path)

        return phrase
    
    def download_audio(self, src, save_path):
        self.reports.logs_report("debug", data="Downloading the audio to the temp folder")
        self.console.debugging(self.debug, msg="Downloading the audio to the temp folder")
        
        urllib.request.urlretrieve(src, save_path)

    def convert_mp3_to_wav(self, mp3_path, wav_path):
        self.reports.logs_report("debug", data="Converting MP3 to WAV format")
        self.console.debugging(self.debug, msg="Converting MP3 to WAV format")

        sound = pydub.AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")

    async def async_decode_audio(self, wav_path):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.decode_audio, wav_path)
    
    def decode_audio(self, wav_path):
        self.reports.logs_report("debug", data="Transcribing the audio content")
        self.console.debugging(self.debug, msg="Transcribing the audio content")

        recognizer = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)

    def cleanup_temp_files(self, *paths):
        for path in paths:
            try:
                os.remove(path)
            except Exception as e:
                self.reports.logs_report("warning", data=f"Failed to delete {path}: {e}")
                self.console.log_print("warning", f"Failed to delete {path}: {e}")

    def get_temp_audio_paths(self):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        mp3 = os.path.join(gettempdir(), f"{timestamp}.mp3")
        wav = os.path.join(gettempdir(), f"{timestamp}.wav")

        return mp3, wav

    def get_text_blocked(self, driver):
        try:
            recaptcha_header = driver.find_element(By.CLASS_NAME, "rc-doscaptcha-body-text")
            return recaptcha_header
        except NoSuchElementException:
            return None

    def is_blocked(self, driver):
        blocked = self.get_text_blocked(driver)
        if blocked is not None:
            self.reports.logs_report("error", data=f"Failed to bypass v2 protection. IP has been blocked! {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{blocked.text}")
            self.console.log_print("error", msg=f"Failed to bypass v2 protection. IP has been blocked! {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{blocked.text}")

        if driver.current_url == "https://www.google.com/sorry/index":
            self.reports.logs_report("error", data="Unexpected response comes from search engines")
            self.console.log_print("error", msg="Unexpected response comes from search engines")
    
    async def solve_captcha(self, url):
        self.reports.logs_report("debug", data=f"Bad URL {url}")
        self.console.debugging(self.debug, msg=f"Bad URL {url}")

        with SeleniumDriver(headless_mode=self.headless) as driver:
            self.wait = WebDriverWait(driver, 5)

            try:
                driver.get(url)
                await self.recaptcha_service(driver)
                return driver
            except KeyboardInterrupt:
                driver.quit()
            except (GodorkException, GodorkTimeout) as err:
                self.reports.logs_report("error", data=f"Failed to bypass v2 protection. {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{err}")
                self.console.log_print("error", msg=f"Failed to bypass v2 protection. {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{err}")