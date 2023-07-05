#!/usr/bin/python3
import psycopg2
import login
import cgi

form = cgi.FieldStorage()
delete = form.getvalue('number')

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Remove Product Page</title>')
print('</head>')
print('<body>')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()

    sql_get_contains = 'SELECT order_no FROM contains WHERE sku = %s;'
    cursor.execute(sql_get_contains, (delete,))
    result = cursor.fetchall()
    
    for row in result:
        sql_delete_pay = 'DELETE FROM pay WHERE order_no = %s;'
        cursor.execute(sql_delete_pay, (row[0],))
        sql_delete_contains = 'DELETE FROM contains WHERE order_no = %s;'
        cursor.execute(sql_delete_contains, (row[0],))
        sql_delete_process = 'DELETE FROM process WHERE order_no = %s;'
        cursor.execute(sql_delete_process, (row[0],))
        sql_delete_order = 'DELETE FROM order_ WHERE order_no = %s;'
        cursor.execute(sql_delete_order, (row[0],))

    
    sql_get_suppliers = 'SELECT tin FROM supplier WHERE sku = %s;'
    cursor.execute(sql_get_suppliers, (delete,))
    result = cursor.fetchall()

    if len(result) > 0:
        for row in result:
            sql_delete_deliveries = 'DELETE FROM delivery WHERE tin = %s;'
            cursor.execute(sql_delete_deliveries, (row[0],))

            sql_delete_supplier = 'DELETE FROM supplier WHERE tin = %s;'
            cursor.execute(sql_delete_supplier, (row[0],))

    sql_delete_product = 'DELETE FROM product WHERE sku = %s;'
    cursor.execute(sql_delete_product, (delete,))
    
    connection.commit()
    cursor.close()
    
    print('<h1>Product deleted with sucess.</h1>')
    print('<a href="products.cgi">go back</a>>')
    print('</body>')
    
except Exception as e:
    print('<h1>OOPSI DUPSIIE.</h1>')
    print('<p>{}</p>'.format(e))
    
finally:
    if connection is not None:
        connection.close()

print('</body>')
print('</html>')