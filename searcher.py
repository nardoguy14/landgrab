import time
import json
from ListingRepository import ListingRepository
from RentoMeter import RentoMeter
from Zillow import Zillow
from NeighborhoodRatings import NeigborhoodRatings


rentoMeter = RentoMeter()
zillow = Zillow()
neighborHoodRatings = NeigborhoodRatings()
listingRepo = ListingRepository()

zillow.loadZillow()
rentoMeter.loginToRentoMeter()
neighborHoodRatings.loadRatingsSite()


time.sleep(10)


resultObjs = []
profitsAbove = []
page = 1
listingsVisited = 0

def cashOnCashCalculate(rentometer_rent_avg, monthly_cost, listing_price):
    cashOnCashReturn = ((float(rentometer_rent_avg) - float(monthly_cost)) * 11) / (listing_price * 0.25 + 35000.0) * 100.0
    cashOnCashReturn = round(cashOnCashReturn, 2)
    cashOnCashReturn = str(cashOnCashReturn) + "%"
    return cashOnCashReturn

def percentageReturnCalculate(rentoMeterAvg, listing_cost):
    wesCalc = (float(rentoMeterAvg) * 11) / (listing_cost + 35000.0) * 100.0
    wesCalc = round(wesCalc, 2)
    wesCalc = str(wesCalc) + "%"
    return wesCalc

def cashFlowCalculate(rentometer_rent_avg, monthlyCost):
    return float(rentometer_rent_avg) - float(monthlyCost)

#yolo
while True:
    try:
        listings = zillow.listingsCalculate(page)

        for listing in listings:
            try:
                print("===================")

                zillow.loadListing(listing)

                address = zillow.addressCalculate()
                numberOfBeds, numberOfBaths = zillow.bedAndBathCalculate()
                monthlyCost = zillow.monthlyCostCalculate()
                listing_cost = zillow.listingCostCalculate()
                listingurl = zillow.getListingUrl()

                neighborHoodRatings.searchRating(address)
                rating = neighborHoodRatings.ratingCalculate()
                ratingurl = neighborHoodRatings.getRatingUrl

                rentoMeter.searchRentoMeter(address, numberOfBeds, numberOfBaths)
                rentometer_rent_avg = rentoMeter.rentoMeterAvgCalculate()
                rentometerurl = rentoMeter.getRentoMeterUrl()

                wesCalc = percentageReturnCalculate(rentometer_rent_avg, listing_cost)
                cashOnCashReturn = cashOnCashCalculate(rentometer_rent_avg, monthlyCost, listing_cost)
                cashFlow = cashFlowCalculate(rentometer_rent_avg, monthlyCost)

                result = {
                    "info": {
                        "address": address,
                        "cost": listing_cost,
                        "numberOfBeds": numberOfBeds,
                        "numberOfBaths": numberOfBaths,
                    },
                    "stats": {
                        "%": {
                            "percentageReturn": wesCalc,
                            "cashOnCashReturn": cashOnCashReturn,
                        },
                        "raw":{
                            "rentalValue": rentometer_rent_avg,
                            "monthlyCost": monthlyCost,
                            "cashflow": cashFlow,
                        },
                        "rating": rating
                    },
                    "links": {
                        "rentometer": rentometerurl,
                        "zillow": listingurl,
                        "rating": ratingurl
                    }
                }

                if cashFlow >= 500.0:
                    profitsAbove.append(result)
                    if len(listingRepo.get_listing(address)) == 0:
                        listingRepo.create_listing(result)

                print(json.dumps(profitsAbove, indent=4, sort_keys=True))
                listingsVisited += 1
                print("results searched: " + str(len(resultObjs)) + f" % that arent worthless: {len(profitsAbove)/listingsVisited}")
                zillow.close()
            except Exception as e:
                print(e)
                zillow.close()
                print("error for item")

        zillow.getNextSetOfListings()
        page += 1

    except Exception as e:
        print(e)
        print("try again")
