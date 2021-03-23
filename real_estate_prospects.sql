create table listings (
    id               INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(256),
    cost    DOUBLE,
    beds    INTEGER,
    baths   INTEGER,
    rating_url   VARCHAR(500),
    rentometer_url  VARCHAR(500),
    zillow_url   VARCHAR(500),
    cashOnCashReturn VARCHAR(20),
    percentageReturn VARCHAR(20),
    rating INTEGER,
    cashflow DOUBLE,
    monthly_cost DOUBLE,
    rent    DOUBLE

);

 {
        "info": {
            "address": "327 E Maynard Ave, Columbus, OH 43202",
            "cost": 249900.0,
            "numberOfBaths": "2",
            "numberOfBeds": "4",
            "pricePerSquareFootage": "192",
            "rentoMeterAvg": "2045 "
        },
        "links": {
            "rating": "https://www.areavibes.com/search-results/?st=OH&ct=Columbus&hd=Somerset&zip=&addr=&ll=40.0272+-82.9187",
            "rentometer": "https://www.rentometer.com/analysis/4-bed/327-east-maynard-avenue-columbus-ohio-43202/6YLN3L2pMRQ/quickview",
            "zillow": "https://www.zillow.com/homedetails/327-E-Maynard-Ave-Columbus-OH-43202/33831299_zpid/"
        },
        "stats": {
            "%": {
                "cashOnCashReturn": "6.95%",
                "percentageReturn": "7.9%"
            },
            "rating": 69,
            "raw": {
                "cashflow": 616.0,
                "monthlyCost": "1429",
                "rentalValue": "2045 "
            }
        }
    }