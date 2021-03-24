**Install**

1. python3 -m venv .venv
2. . .venv/bin/activate
3. pip install -r requirements.txt
4. python main.py
5. run sql create table script on real_estate_prospects.sql

**Dependencies**

1. Chrome
2. You need a selenium driver that can be found here.
https://chromedriver.chromium.org/downloads
Download the appropriate one for your version of chrome.
3. mysql database to store results


**Downside**
Needs a login into rentometer. You can create a free account that lasts for 7 days.

**Layout of Project**
main.py is a script that goes to zillow grabs all the listings on a page, grabs data from each listing, then goes and checks the rent
at rentometer, and lastly grabs the rating score from areavibes. If the cashflow is over a certain amount defined as a constant and the
listing hasnt been saved to a local database, then it saves it to a mysql database. It keeps doing that.