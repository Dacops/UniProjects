#!/usr/bin/python3 
import psycopg2, cgi
import login

form = cgi.FieldStorage()
#getvalue uses the names from the form in previous page
deleteClient = form.getvalue('number')

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Remove Page</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()

    # Making queries'
    sql_get_order_no = 'SELECT order_no FROM order_ WHERE cust_no = %s;'
    cursor.execute(sql_get_order_no, (deleteClient,))

    result = cursor.fetchall()

    for row in result:

        sql_delete_contains = 'DELETE FROM contains WHERE order_no = %s;'
        cursor.execute(sql_delete_contains, (row[0],))

        sql_delete_process = 'DELETE FROM process WHERE order_no = %s;'
        cursor.execute(sql_delete_process, (row[0],))

        sql_delete_pay = 'DELETE FROM pay WHERE order_no = %s;'
        cursor.execute(sql_delete_pay, (row[0],))

    sql_delete_pay = 'DELETE FROM pay WHERE cust_no = %s;'
    cursor.execute(sql_delete_pay, (deleteClient,))

    sql_delete_order = 'DELETE FROM order_ WHERE cust_no = %s;'
    cursor.execute(sql_delete_order, (deleteClient,))

    sql_delete_customer = 'DELETE FROM customer WHERE cust_no = %s;'
    cursor.execute(sql_delete_customer, (deleteClient,))

    connection.commit()
    cursor.close()

    print('<h1>Client deleted with sucess.</h1>')
    print('<a href="customers.cgi">go back</a>>')
    print('</body>')

except Exception as e:

       print('<h1>An error occurred.</h1>')
       print('<p>{}</p>'.format(e))
finally:
    if connection is not None:
        connection.close()
print('</body>')
print('</html>')