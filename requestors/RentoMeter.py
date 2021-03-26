from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

class RentoMeter:
    rentoMeterDriver = webdriver.Chrome()

    def closeWindow(self):
        self.rentoMeterDriver.close()

    def getRentoMeterUrl(self):
        return self.rentoMeterDriver.current_url

    def loginToRentoMeter(self):
        self.rentoMeterDriver.get("https://www.rentometer.com/")
        self.rentoMeterDriver.find_element_by_xpath("/html/body/div[3]/nav/div[2]/ul[1]/li[2]/a").click()
        time.sleep(2)
        self.rentoMeterDriver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/form/div[1]/input").send_keys(
            "nardoarevalo@me.com")
        self.rentoMeterDriver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/form/div[3]/input").send_keys(
            "CAMera14!")
        self.rentoMeterDriver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/form/div[5]/input").click()

    def searchRentoMeter(self, address, numberOfBeds, numberOfBaths):
        self.rentoMeterDriver.get("https://www.rentometer.com/")
        time.sleep(2)
        self.rentoMeterDriver.find_element_by_id("address_unified_search_address").send_keys(address)
        Select(self.rentoMeterDriver.find_element_by_id("address_unified_search_bed_style")).select_by_value(numberOfBeds)
        if int(numberOfBaths) > 1:
            Select(self.rentoMeterDriver.find_element_by_id("address_unified_search_baths")).select_by_value("1.5")
        else:
            Select(self.rentoMeterDriver.find_element_by_id("address_unified_search_baths")).select_by_value("1")

        self.rentoMeterDriver.find_element_by_name("commit").click()
        time.sleep(4)

    def rentoMeterAvgCalculate(self):
        rentoMeterAvg = 0
        for stat in self.rentoMeterDriver.find_elements_by_class_name("box-stats"):
            if "AVERAGE" in stat.text:
                rentoMeterAvg = stat.text
                rentoMeterAvg = rentoMeterAvg.split("\n")[1].split("±")[0].replace("$", "").replace(",", "")
        return rentoMeterAvg