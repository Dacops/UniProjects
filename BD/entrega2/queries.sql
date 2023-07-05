 -- 1. Liste o nome de todos os clientes que fizeram encomendas contendo produtos de preço superior 
 -- a €50 no ano de 2023;

SELECT DISTINCT(c.name)
FROM customer c
    JOIN order_ o ON c.cust_no = o.cust_no
    JOIN contains co ON o.order_no = co.order_no
    JOIN (
        SELECT sku, name AS product_name, description, price
        FROM product
    ) p ON p.sku = co.sku
WHERE p.price > 50 AND o.date BETWEEN '2023-01-01' AND '2023-12-31';



 -- 2. Liste o nome de todos os empregados que trabalham em armazéns e não em escritórios e
 -- processaram encomendas em Janeiro de 2023;

SELECT e.name
FROM employee e
    JOIN process p ON e.ssn = p.ssn
    JOIN order_ o ON o.order_no = p.order_no
    JOIN (
        SELECT ssn, address, name AS department_name
        FROM works
    ) w ON w.ssn = e.ssn
    JOIN workplace wp ON wp.address = w.address
    JOIN warehouse wh ON wh.address = wp.address
WHERE o.date BETWEEN '2023-01-01' AND '2023-01-31';



 -- 3. Indique o nome do produto mais vendido;

SELECT p.name
FROM (
    SELECT name, SUM(c.qty) AS total_sold
    FROM product p
        JOIN contains c ON p.sku = c.sku
        JOIN order_ o ON o.order_no = c.order_no
        JOIN sale s ON s.order_no = o.order_no
    GROUP BY name
) p
WHERE p.total_sold = (
    SELECT MAX(total_sold)
    FROM (
        SELECT SUM(c.qty) AS total_sold
        FROM product p
            JOIN contains c ON p.sku = c.sku
            JOIN order_ o ON o.order_no = c.order_no
            JOIN sale s ON s.order_no = o.order_no
        GROUP BY p.name
    ) subquery
);


 -- 4. Indique o valor total de cada venda realizada.

SELECT o.order_no, p.price * c.qty AS total
FROM product p
    JOIN contains c ON p.sku = c.sku
    JOIN order_ o ON o.order_no = c.order_no
    JOIN sale s ON s.order_no = o.order_no

 