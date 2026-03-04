create database mydatabse;
use mydatabse;

-- CREATE TABLE
CREATE TABLE MarketAnalysis (
    Order_ID INT primary key,
    Country VARCHAR(50),
    Category VARCHAR(50),
    Unit_Price Decimal(10,2),
    Quantity INT,
    Order_Date Date,
    Total_Amount Decimal(10,2)
);

-- Load Dataset 
-- SET GLOBAL local_infile = 1;
-- LOAD DATA LOCAL INFILE 'C:/Users/hp/Desktop/P.MIB/03_SQL_Analysis.sql/global_ecommerce_sales.csv'
-- INTO TABLE MarketAnalysis
-- FIELDS TERMINATED BY ','
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- Remove exixting data from table
TRUNCATE TABLE MarketAnalysis;

LOAD DATA LOCAL INFILE 'C:/Users/hp/Desktop/P.MIB/03_SQL_Analysis.sql/global_ecommerce_sales.csv'
INTO TABLE MarketAnalysis
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Order_ID, Country, Category, Unit_Price, Quantity, @Order_Date, Total_Amount)
SET Order_Date = STR_TO_DATE(TRIM(@Order_Date), '%m/%d/%Y');


SELECT * FROM MarketAnalysis;

				-- Query-1 : Product Demand
SELECT Category, SUM(Total_Amount) AS Revenue
FROM MarketAnalysis
GROUP BY Category
ORDER BY Revenue DESC;


				-- Analysis 2 — Country Revenue Comparison
				-- Show international purchasing patterns
SELECT Country, SUM(Total_Amount) AS Total_Revenue
FROM MarketAnalysis
GROUP BY Country
ORDER BY Total_Revenue DESC;


				-- Analysis 3 — Average Order Value (AOV)
                -- Understand consumer spending behavior
SELECT Country, AVG(Total_Amount) AS Avg_Order_Value
FROM MarketAnalysis
GROUP BY Country;


				-- Analysis 4 — Sales Trend Over Time
SELECT Order_Date, SUM(Total_Amount)
FROM MarketAnalysis
GROUP BY Order_Date
ORDER BY Order_Date;
