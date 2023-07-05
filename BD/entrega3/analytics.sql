 -- 1. As quantidade e valores totais de venda de cada produto em 2022, globalmente, por cidade, por
 -- mês, dia do mês e dia da semana

SELECT city, month, day_of_month, day_of_week, sku, SUM(qty) AS qty, SUM(total_price) AS total_price
FROM product_sales
WHERE year = 2022

GROUP BY GROUPING SETS ( (city, sku), (month, sku), (day_of_month, sku), (day_of_week, sku) )


 -- 2. O valor médio diário das vendas de todos os produtos em 2022, globalmente, por mês e dia da
 -- semana

SELECT month, day_of_week, AVG(total_price) AS daily_avg
FROM product_sales
WHERE year = 2022

GROUP BY GROUPING SETS ( (), (month), (day_of_week) )