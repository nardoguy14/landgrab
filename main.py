import time
from repositories.ListingRepository import ListingRepository
from requestors.RentoMeter import RentoMeter
from requestors.Zillow import Zillow
from requestors.NeighborhoodRatings import NeigborhoodRatings
import traceback
from utils import financial_stats

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

amountInvestedForRennovation = 35000.0
downpaymentPercentage = 0.25
propertyManagementPercentageFeeOfRent = 0.07

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
                ratingurl = neighborHoodRatings.getRatingUrl()

                rentoMeter.searchRentoMeter(address, numberOfBeds, numberOfBaths)
                rentometer_rent_avg = rentoMeter.rentoMeterAvgCalculate()
                rentometerurl = rentoMeter.getRentoMeterUrl()

                wesCalc = financial_stats.percentageReturnCalculate(rentometer_rent_avg, listing_cost,
                                                                    amountInvestedForRennovation)
                cashOnCashReturn = financial_stats.cashOnCashCalculate(rentometer_rent_avg, monthlyCost, listing_cost,
                                                                       downpaymentPercentage, amountInvestedForRennovation,
                                                                       propertyManagementPercentageFeeOfRent)
                cashFlow = financial_stats.cashFlowCalculate(rentometer_rent_avg, monthlyCost)

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

                if cashFlow >= 400.0:
                    profitsAbove.append(result)
                    if len(listingRepo.get_listing(address)) == 0:
                        listingRepo.create_listing(result)

                listingsVisited += 1
                print("results searched: " + str(listingsVisited) +
                      f" % that arent worthless: {len(profitsAbove)/listingsVisited} page: {page}")
                zillow.close()
            except Exception as e:
                print(e)
                traceback.print_exc()
                zillow.close()

        zillow.getNextSetOfListings()
        page += 1

    except Exception as e:
        print(e)
        print("try again")
