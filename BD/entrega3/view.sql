DROP VIEW IF EXISTS product_sales

CREATE VIEW product_sales(
    sku, order_no, qty, total_price, year, month, day_of_month, day_of_week, city
)
AS
SELECT sku, order_no, qty, qty*price, EXTRACT(YEAR FROM date),
        EXTRACT(MONTH FROM date), EXTRACT(DAY FROM date), EXTRACT(DOW FROM date),
        REVERSE(SUBSTRING(REVERSE(address), 1, POSITION(' ' IN REVERSE(address)) - 1))
FROM product NATURAL JOIN contains NATURAL JOIN order_
JOIN ( SELECT address, cust_no FROM customer ) customer on customer.cust_no = order_.cust_no
WHERE order_no IN ( SELECT order_no FROM pay )