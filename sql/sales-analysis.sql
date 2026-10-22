-- Online Retail Sales Analysis
USE ecommerce_analysis;

-- 1. Total Revenue
SELECT ROUND(SUM(Revenue), 2) AS Total_Revenue
FROM online_retail;

-- 2. Total Orders
SELECT COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM online_retail;

-- 3. Total Customers
SELECT COUNT(DISTINCT CustomerID) AS Total_Customers
FROM online_retail;

-- 4. Top 10 Countries by Revenue
SELECT Country, ROUND(SUM(Revenue), 2) AS Total_Revenue
FROM online_retail
GROUP BY Country
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 5. Top 10 Products by Revenue
SELECT Description, ROUND(SUM(Revenue), 2) AS Total_Revenue
FROM online_retail
GROUP BY Description
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 6. Monthly Revenue Trend
SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
ROUND(SUM(Revenue), 2) AS Monthly_Revenue
FROM online_retail
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY Month;
