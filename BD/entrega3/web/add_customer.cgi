#!/usr/bin/python3
import psycopg2
import login
import cgi
import view

try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    form = cgi.FieldStorage()

    sql_get_max = "SELECT MAX(cust_no) FROM customer"
    cursor.execute(sql_get_max)
    result = cursor.fetchall()

    cust_no = result[0][0] + 1
    
    sql = "INSERT INTO customer VALUES(%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s)"
    cursor.execute(sql, {'cust_no': cust_no, 'name': form.getvalue('name'), 'email': form.getvalue('email'), 'phone': form.getvalue('phone'), 'address': form.getvalue('address')})
    connection.commit()
    cursor.close()

    print('Content-type:text/html\n\n')
    print('<html>')
    print('<head>')
    print('<title>Add Page</title>')
    print('</head>')
    print('<body>')
    print('<h1>Client added with sucess.</h1>')
    print('<a href="customers.cgi">go back</a>>')
    print('</body>')
    
except Exception as e:
    view.handle_exception(e)
    
finally:
    if connection is not None:
        connection.close()

print('</body>')
print('</html>')