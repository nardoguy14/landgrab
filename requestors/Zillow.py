from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class Zillow:
    driver = webdriver.Chrome()

    def closeWindow(self):
        self.driver.close()

    def getListingUrl(self):
        return self.driver.current_url

    def loadZillow(self, city):
        self.driver.get(f"https://www.zillow.com/homes/for_sale/{city}_rb/")

    def getAmountOfPages(self):
        pages = int(self.driver.find_element_by_class_name("PaginationReadoutItem-c11n-8-27-0__sc-18an4gi-0").text.split()[3])
        return pages

    def close(self):
        try:
            for item in self.driver.find_elements_by_class_name("ds-close-lightbox-icon"):
                item.click()

            self.driver.find_element_by_class_name("hdp__zbe8gz-0").click()
        except:
            print("")
        time.sleep(2)

    def getNextSetOfListings(self):
        self.driver.find_element_by_css_selector("[title*='Next page']").click()
        time.sleep(3)


    def bedAndBathCalculate(self):
        numberOfBeds = 0
        numberOfBaths = 0
        bedAndBaths = self.driver.find_elements_by_class_name("ds-bed-bath-living-area")
        for item in bedAndBaths:
            text = item.text
            print(item.text)
            if 'bd' in text:
                numberOfBeds = text.split(" ")[0]
            elif 'ba' in text:
                numberOfBaths = text.split(" ")[0]
        return numberOfBeds, numberOfBaths


    def monthlyCostCalculate(self, downPaymentPercent):
        self.driver.find_elements_by_xpath("//*[contains(text(), 'Principal')]")[0].find_element_by_xpath('..').click()
        self.driver.find_element_by_id("down-payment-percent").send_keys("lalala")
        while self.driver.find_element_by_id("down-payment-percent").get_attribute('value') != '':
            self.driver.find_element_by_id("down-payment-percent").clear()
        self.driver.find_element_by_id("down-payment-percent").send_keys(downPaymentPercent)
        self.driver.find_element_by_id("interest-rate").click()
        monthlyCost = self.driver.find_elements_by_xpath("//*[contains(text(), 'Estimated monthly')]")[0].find_element_by_xpath('..').text
        monthlyCost = monthlyCost.split('\n')[1].replace("$", "").replace(",", "")
        return monthlyCost

    def listingCostCalculate(self):
        cost = self.driver.find_element_by_class_name("hdp__qf5kuj-3").text
        cost = cost.replace("$", "").replace(",", "")
        cost = float(cost)
        return cost

    def addressCalculate(self):
        return self.driver.find_element_by_id("ds-chip-property-address").text

    def loadListing(self, listing):
        link = listing.find_element_by_tag_name('a')
        link.click()
        time.sleep(4)

    def listingsCalculate(self, page):
        print(f"page {page}")
        results = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul")
        listings = results.find_elements_by_tag_name("article")
        print(len(listings))
        return listings