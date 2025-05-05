from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time
import logging

logger = logging.getLogger(__name__)


class Waiter:

    def __init__(self,
                 driver):

        self.driver = driver


    def wait_for_webelement_to_load(self,
                                     webelement_xpath,
                                     timeout=15):

        """Wait until the page loads by checking for the presence of product items."""
        try:
            logger.debug("Waiting for page to load...")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, webelement_xpath))
            )
            logger.debug("Page has fully loaded.")
        except Exception as e:
            logger.debug(f"Timeout waiting for page to load: {e}")
            raise


    def wait(self,
             min,
             max,
             webelement_xpath=None,
             timeout=15,
             print_waittime=True):

        if webelement_xpath:
            self.wait_for_webelement_to_load(webelement_xpath, timeout)

        wait_time = random.uniform(min, max)
        time.sleep(wait_time)

        if print_waittime:
            logger.debug(f"Waiting {round(wait_time, 2)} seconds...")

        return wait_time
