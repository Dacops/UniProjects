--Qual o número e nome do(s) cliente(s) com maior valor total de encomendas pagas?

WITH customer_spending AS (
    SELECT name AS customer_name, SUM(price * qty) AS total_spent
    FROM customer
    NATURAL JOIN pay
    NATURAL JOIN order_
    NATURAL JOIN contains
    NATURAL JOIN (
        SELECT sku, price
        FROM product
    ) p
    GROUP BY customer.name
)
SELECT customer_name, total_spent
FROM customer_spending
JOIN (
    SELECT MAX(total_spent) AS max_spent
    FROM customer_spending
) max_spent_table ON customer_spending.total_spent = max_spent_table.max_spent;


--Qual o nome dos empregados que processaram encomendas em todos os dias de 2022 em que 
--houve encomendas?

SELECT DISTINCT name
FROM employee e
WHERE NOT EXISTS (
    SELECT DISTINCT date
    FROM order_
    WHERE EXTRACT(YEAR FROM date) = 2022
    EXCEPT
    SELECT DISTINCT date
    FROM ( order_ NATURAL JOIN process NATURAL JOIN employee ) x
    WHERE e.name = x.name
);

--Quantas encomendas foram realizadas mas não pagas em cada mês de 2022?

SELECT EXTRACT(MONTH FROM date) AS month, COUNT(order_no)
FROM order_
WHERE EXTRACT(YEAR FROM date) = 2022 AND order_no NOT IN (
    SELECT order_no FROM pay
)
GROUP BY EXTRACT(MONTH FROM date)
ORDER BY month;




