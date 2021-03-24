

def cashOnCashCalculate(rentometer_rent_avg, monthly_cost, listing_price,
                        downpaymentPercentage, amountInvestedForRennovation, propertyManagementPercentageFeeOfRent):
    rentometer_rent_avg = float(rentometer_rent_avg)
    monthly_cost = float(monthly_cost)

    monthlyPropertyManangementFee = propertyManagementPercentageFeeOfRent * rentometer_rent_avg
    cashOnCashReturn = ((rentometer_rent_avg - monthly_cost - monthlyPropertyManangementFee) * 12) / \
                       (listing_price * downpaymentPercentage  + amountInvestedForRennovation) * 100.0

    cashOnCashReturn = round(cashOnCashReturn, 2)
    cashOnCashReturn = str(cashOnCashReturn) + "%"
    return cashOnCashReturn

def percentageReturnCalculate(rentoMeterAvg, listing_cost, amountInvestedForRennovation):
    wesCalc = (float(rentoMeterAvg) * 12) / (listing_cost + amountInvestedForRennovation) * 100.0

    wesCalc = round(wesCalc, 2)
    wesCalc = str(wesCalc) + "%"
    return wesCalc

def cashFlowCalculate(rentometer_rent_avg, monthlyCost):
    rentometer_rent_avg = float(rentometer_rent_avg)
    monthlyPropertyManangementFee = 0.07 * rentometer_rent_avg
    return rentometer_rent_avg - float(monthlyCost) - monthlyPropertyManangementFee