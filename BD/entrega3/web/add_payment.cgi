#!/usr/bin/python3
import psycopg2
import login
import cgi
import view

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Pay Page</title>')
print('</head>')
print('<body>')
    
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    form = cgi.FieldStorage()
    
    sql_get_order = "SELECT order_no, cust_no FROM order_ WHERE order_no = %(order_no)s"
    cursor.execute(sql_get_order, {'order_no': form.getvalue('order_no')})
    result = cursor.fetchall()
    
    order_no = result[0][0]
    cust_no = result[0][1]
    sql_insert = "INSERT INTO pay VALUES(%(order_no)s, %(cust_no)s)"
    cursor.execute(sql_insert, {'cust_no': cust_no, 'order_no': order_no})

    print('<h1>Order Payed with Sucess.</h1>')
    print('<a href="orders.cgi">go back</a>>')
        
    connection.commit()
    cursor.close()

    print('</body>')
    
except Exception as e:
    view.handle_exception(e)    
finally:
    if connection is not None:
        connection.close()

print('</body>')
print('</html>')