#!/usr/bin/python3
import psycopg2
import login
import cgi

form = cgi.FieldStorage()
deleteCustomer = form.getvalue('number')

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Remove Page</title>')
print('</head>')
print('<body>')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    
    sql_delete_deliveries = 'DELETE FROM delivery WHERE tin = %s;'
    cursor.execute(sql_delete_deliveries, (deleteCustomer,))
    
    
    sql_delete_supplier = 'DELETE FROM supplier WHERE tin = %s;'
    cursor.execute(sql_delete_supplier, (deleteCustomer,))
    
    connection.commit()
    cursor.close()
    
    print('<h1>Supplier deleted with sucess.</h1>')
    print('<a href="suppliers.cgi">go back</a>>')
    print('</body>')
    
except Exception as e:
    print('<h1>OOPSI DUPSIIE.</h1>')
    print('<p>{}</p>'.format(e))
    
finally:
    if connection is not None:
        connection.close()

print('</body>')
print('</html>')