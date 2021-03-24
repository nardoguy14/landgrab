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
    rent    DOUBLE,
    yay_or_nay BOOLEAN,
    needs_renno BOOLEAN
);

alter table listings add column yay_or_nay BOOL;
