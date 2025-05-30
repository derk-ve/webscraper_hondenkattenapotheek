from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ...scraping.configs.xpath_configs import category_xpath
import logging

class Mover:

    def __init__(self,
                 driver,
                 website,
                 waiter):

        self.driver = driver
        self.website = website
        self.waiter = waiter


    def scroll_element_into_view(self,
                                 element):

        self.driver.execute_script("arguments[0].scrollIntoView();", element)


    def check_and_click_coockie(self):

        try:
            cookie_button = self.driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonDecline")
            logging.info("Found a cookie pop-up")
            self.waiter.wait(min=2, max=4)
            cookie_button.click()
            logging.info("Cookie pop-up closed.")
        except Exception:
            pass


    def get_next_button(self):

        try:
            next_button = self.driver.find_element(By.XPATH, "//" + category_xpath[self.website]["next_button"])
            logging.info("Found Next button")
            return next_button
        except Exception:
            logging.info("Could not find next button")
            raise


    def go_to_next_page(self,
                        next_button=None):

        logging.info("Trying to go to next page...")
        if not next_button:
            next_button = self.get_next_button()
        if not next_button:
            logging.info("No next button found")
            raise
        logging.info("Scrolling down to next button...")
        self.scroll_element_into_view(next_button)
        self.waiter.wait(min=2, max=4)
        next_button.click()
        logging.info("Clicked next page button")
        logging.info(self.driver.current_url)
        self.waiter.wait(min=2, max=4)

