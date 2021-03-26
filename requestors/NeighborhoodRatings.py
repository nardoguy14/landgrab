from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class NeigborhoodRatings:
    ratingsDriver = webdriver.Chrome()

    def closeWindow(self):
        self.ratingsDriver.close()

    def getRatingUrl(self):
        return self.ratingsDriver.current_url

    def loadRatingsSite(self):
        self.ratingsDriver.get("https://www.areavibes.com/search-results/")

    def searchRating(self, address):
        self.ratingsDriver.get("https://www.areavibes.com/search-results/")
        time.sleep(3)
        addressRatingsInput = self.ratingsDriver.find_element_by_xpath("/html/body/div[1]/div/div/div/header/form/input")
        addressRatingsInput.send_keys(address)
        addressRatingsInput.send_keys(Keys.ENTER)
        time.sleep(2)
        addressRatingsInput.send_keys(Keys.DOWN)
        time.sleep(2)
        addressRatingsInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def ratingCalculate(self):
        rating = int(self.ratingsDriver.find_element_by_xpath("/html/body/div[3]/div[3]/div/a[1]/i[2]").text)
        return rating