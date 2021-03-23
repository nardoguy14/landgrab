from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import json
from BaseRepository import BaseRepository

driver = webdriver.Chrome()
rentoMeterDriver = webdriver.Chrome()
ratingsDriver = webdriver.Chrome()

driver.get("https://www.zillow.com/homes/for_sale/colombus-ohio_rb/")

rentoMeterDriver.get("https://www.rentometer.com/")
rentoMeterDriver.find_element_by_xpath("/html/body/div[3]/nav/div[2]/ul[1]/li[2]/a").click()
time.sleep(2)
rentoMeterDriver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/form/div[1]/input").send_keys("nardoarevalo@me.com")
rentoMeterDriver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/form/div[3]/input").send_keys("CAMera14!")
rentoMeterDriver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/form/div[5]/input").click()


ratingsDriver.get("https://www.areavibes.com/search-results/")

time.sleep(10)


def close():
    try:
        for item in driver.find_elements_by_class_name("ds-close-lightbox-icon"):
            item.click()

        driver.find_element_by_class_name("hdp__zbe8gz-0").click()
    except:
        print("")


def create_listing(listing):
    with BaseRepository() as base_repo:
        sql = """
        INSERT INTO listings (
            address,
            cost,
            beds,
            baths,
            rating_url,
            rentometer_url,
            zillow_url,
            cashOnCashReturn,
            percentageReturn,
            rating,
            cashflow,
            monthly_cost,
            rent    
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (
            listing['info']['address'],
            listing['info']['cost'],
            int(listing['info']['numberOfBeds']),
            int(listing['info']['numberOfBaths']),
            listing['links']['rating'],
            listing['links']['rentometer'],
            listing['links']['zillow'],
            listing['stats']['%']['cashOnCashReturn'],
            listing['stats']['%']['percentageReturn'],
            listing['stats']['rating'],
            float(listing['stats']['raw']['cashflow']),
            float(listing['stats']['raw']['monthlyCost']),
            float(listing['stats']['raw']['rentalValue']),
        )

        base_repo.execute(sql, val)
        return base_repo.lastrowid


def get_listing(address):
    with BaseRepository() as base_repo:
        query = (f"""SELECT 
                        id
                    FROM listings 
                    WHERE address = %s
                """)
        params = [address]
        filtered_params = tuple(list(filter(lambda x: x != None, params)))
        base_repo.execute(query, filtered_params)

        results = []
        for (
                id,
        ) in base_repo:
            results.append(id)

        return results

resultObjs = []
profitsAbove = []

page = 1
while True:
    try:
        print(f"page {page}")
        results = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul")
        options = results.find_elements_by_tag_name("article")
        print(len(options))

        for option in options:
            try:
                print("===================")
                print(option.text)
                link = option.find_element_by_tag_name('a')
                link.click()
                print("sleeping...")
                time.sleep(4)

                listingurl = driver.current_url
                address = driver.find_element_by_id("ds-chip-property-address").text
                print(address)

                ratingsDriver.get("https://www.areavibes.com/search-results/")
                time.sleep(3)
                addressRatingsInput = ratingsDriver.find_element_by_xpath("/html/body/div[1]/div/div/div/header/form/input")
                addressRatingsInput.send_keys(address)
                addressRatingsInput.send_keys(Keys.ENTER)
                time.sleep(2)
                addressRatingsInput.send_keys(Keys.DOWN)
                time.sleep(2)
                addressRatingsInput.send_keys(Keys.ENTER)
                time.sleep(2)
                rating = int(ratingsDriver.find_element_by_xpath("/html/body/div[3]/div[3]/div/a[1]/i[2]").text)
                ratingurl =ratingsDriver.current_url

                bedAndBaths = driver.find_elements_by_class_name("ds-bed-bath-living-area")

                numberOfBeds = 0
                numberOfBaths = 0
                for item in bedAndBaths:
                    text = item.text
                    print(item.text)
                    if 'bd' in text:
                        numberOfBeds = text.split(" ")[0]
                    elif 'ba' in text:
                        numberOfBaths = text.split(" ")[0]

                monthlyCost = driver.find_element_by_class_name("sc-fzokOt").text
                monthlyCost = monthlyCost.split('\n')[1].replace("$", "").replace(",", "")
                print(monthlyCost)

                rentalValue = 0
                # rentalValue = driver.find_elements_by_class_name("bloUvX")[2].text.split("/")[0].replace("$", "").replace(",", "")
                # print(rentalValue)

                pricePerSquareFootage = driver.find_elements_by_class_name('iDaikS')[6].text
                pricePerSquareFootage = pricePerSquareFootage.replace("$", "").replace(",", "")
                print(pricePerSquareFootage)

                rentoMeterDriver.get("https://www.rentometer.com/")
                time.sleep(2)
                rentoMeterDriver.find_element_by_id("address_unified_search_address").send_keys(address)

                Select(rentoMeterDriver.find_element_by_id("address_unified_search_bed_style")).select_by_value(numberOfBeds)
                if int(numberOfBaths) > 1:
                    Select(rentoMeterDriver.find_element_by_id("address_unified_search_baths")).select_by_value("1.5")
                else:
                    Select(rentoMeterDriver.find_element_by_id("address_unified_search_baths")).select_by_value("1")

                rentoMeterDriver.find_element_by_name("commit").click()

                time.sleep(4)

                rentometerurl = rentoMeterDriver.current_url

                rentoMeterAvg = 0
                for stat in rentoMeterDriver.find_elements_by_class_name("box-stats"):
                    if "AVERAGE" in stat.text:
                        rentoMeterAvg = stat.text
                        rentoMeterAvg = rentoMeterAvg.split("\n")[1].split("±")[0].replace("$", "").replace(",", "")

                cost = driver.find_element_by_class_name("hdp__qf5kuj-3").text
                cost = cost.replace("$", "").replace(",", "")
                cost = float(cost)

                wesCalc = (float(rentoMeterAvg) * 11) / (cost + 35000.0) * 100.0
                wesCalc = round(wesCalc, 2)
                wesCalc = str(wesCalc) + "%"

                cashOnCashReturn = ((float(rentoMeterAvg) - float(monthlyCost)) * 11) / (cost * 0.25 + 35000.0) * 100.0
                cashOnCashReturn = round(cashOnCashReturn, 2)
                cashOnCashReturn = str(cashOnCashReturn) + "%"

                result = {
                    "info": {
                        "address": address,
                        "cost": cost,
                        "numberOfBeds": numberOfBeds,
                        "numberOfBaths": numberOfBaths,
                        "pricePerSquareFootage": pricePerSquareFootage,
                    },
                    "stats": {
                        "%": {
                            "percentageReturn": wesCalc,
                            "cashOnCashReturn": cashOnCashReturn,
                        },
                        "raw":{
                            "rentalValue": rentoMeterAvg,
                            "monthlyCost": monthlyCost,
                            "cashflow": float(rentoMeterAvg) - float(monthlyCost),
                        },
                        "rating": rating
                    },
                    "links": {
                        "rentometer": rentometerurl,
                        "zillow": listingurl,
                        "rating": ratingurl
                    }
                }

                resultObjs.append(result)

                if float(rentoMeterAvg) - float(monthlyCost) >= 500.0:
                   profitsAbove.append(result)
                   if len(get_listing(result['info']['address'])) == 0:
                       create_listing(result)

                print(json.dumps(profitsAbove, indent=4, sort_keys=True))
                print("results searched: " + str(len(resultObjs)) + f" %: {len(profitsAbove)/len(resultObjs)}")

                close()
                time.sleep(2)
            except Exception as e:
                print(e)
                close()
                print("error for item")

        driver.find_element_by_css_selector("[title*='Next page']").click()
        time.sleep(3)
        page += 1
        print(str(resultObjs))

    except Exception as e:
        print(e)
        print("try again")



