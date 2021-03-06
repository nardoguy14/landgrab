import time
from repositories.ListingRepository import ListingRepository
from requestors.RentoMeter import RentoMeter
from requestors.Zillow import Zillow
from requestors.NeighborhoodRatings import NeigborhoodRatings
import traceback
from utils import financial_stats

amountInvestedForRennovation = 35000.0
downpaymentPercentage = 0.25
downpaymentPercentageStr = "25"
propertyManagementPercentageFeeOfRent = 0.07
#needs to go over this or match it to consider it
cashFlowCutOff = 400.0
city = "cincinnati"

rentoMeter = RentoMeter()
zillow = Zillow()
neighborHoodRatings = NeigborhoodRatings()
listingRepo = ListingRepository()

#yolo
while True:
    zillow.loadZillow(city)
    rentoMeter.loginToRentoMeter()
    neighborHoodRatings.loadRatingsSite()

    time.sleep(10)

    resultObjs = []
    profitsAbove = []
    page = 1
    listingsVisited = 0
    pageLimit = zillow.getAmountOfPages()
    while page <= pageLimit:
        try:
            listings = zillow.listingsCalculate(page)
            for listing in listings:
                try:
                    print("===================")

                    zillow.loadListing(listing)

                    address = zillow.addressCalculate()
                    numberOfBeds, numberOfBaths = zillow.bedAndBathCalculate()
                    monthlyCost = zillow.monthlyCostCalculate(downpaymentPercentageStr)
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

                    if cashFlow >= cashFlowCutOff:
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

    zillow.closeWindow()
    rentoMeter.closeWindow()
    neighborHoodRatings.closeWindow()