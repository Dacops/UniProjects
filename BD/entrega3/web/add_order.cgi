#!/usr/bin/python3
import psycopg2
import login
import cgi
import view

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Add Order Page</title>')
print('</head>')
print('<body>')
    
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    form = cgi.FieldStorage()
    
    sql_get_max = "SELECT MAX(order_no) FROM order_"
    cursor.execute(sql_get_max)
    result = cursor.fetchall()
    
    order_no = result[0][0]+1
    
    sql_get_ssn = "SELECT ssn FROM employee WHERE ssn = %(ssn)s"
    cursor.execute(sql_get_ssn, {'ssn': form.getvalue('ssn')})
    result = cursor.fetchall()
    
    if len(result) == 0: raise Exception('Employee does not exist.')
    
    sql_get_cust_no = "SELECT cust_no FROM customer WHERE cust_no = %(cust_no)s"
    cursor.execute(sql_get_cust_no, {'cust_no': form.getvalue('cust_no')})
    result = cursor.fetchall() 
    
    if len(result) == 0: raise Exception('Customer does not exist.')
    
    sql_get_product = "SELECT sku FROM product WHERE sku = %(sku)s"
    cursor.execute(sql_get_product, {'sku': form.getvalue('sku')})
    result = cursor.fetchall()
    
    if len(result) == 0: raise Exception('Product does not exist.')
    
    
    sql_order = "INSERT INTO order_ VALUES(%(order_no)s, %(cust_no)s, %(date)s)"
    cursor.execute(sql_order, {'order_no': order_no, 'cust_no': form.getvalue('cust_no'), 'date': form.getvalue('date')})
    
    sql_contains = "INSERT INTO contains VALUES(%(order_no)s, %(sku)s, %(quantity)s)"
    cursor.execute(sql_contains, {'order_no': order_no, 'sku': form.getvalue('sku'), 'quantity': form.getvalue('quantity')})
    
    sql_process = "INSERT INTO process VALUES(%(ssn)s, %(order_no)s)"
    cursor.execute(sql_process, {'ssn': form.getvalue('ssn'), 'order_no': order_no})
    
    connection.commit()
    cursor.close()
    
    print('<h1>Order added with sucess.</h1>')
    print('<a href="orders.cgi">go back</a>>')

    print('</body>')
    
except Exception as e:
    print('<a href="form_order.cgi">please come back</a>')
    view.handle_exception(e)
    
finally:
    if connection is not None:
        connection.close()

print('</body>')
print('</html>')