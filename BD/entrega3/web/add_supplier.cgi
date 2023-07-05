#!/usr/bin/python3
import psycopg2
import login
import cgi
import view

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Add Supplier Page</title>')
print('</head>')
print('<body>')

try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    form = cgi.FieldStorage()

    sql_get_product = "SELECT sku FROM product WHERE sku = %(sku)s;"
    cursor.execute(sql_get_product, {'sku': form.getvalue('sku')})
    result = cursor.fetchall() 

    if len(result) == 0: raise Exception('Product Does Not Exist')
    
    sql_get_sup = "SELECT tin FROM supplier WHERE tin = %(tin)s AND sku = %(sku)s;"
    cursor.execute(sql_get_sup, {'tin': form.getvalue('tin'), 'sku': form.getvalue('sku')})
    result = cursor.fetchall()

    if len(result) > 0: raise Exception('Tin Already Exists for that product')

    sql = "INSERT INTO supplier VALUES(%(tin)s, %(name)s, %(address)s, %(sku)s)"
    cursor.execute(sql, {'tin': form.getvalue('tin'), 'name': form.getvalue('name'), 'address': form.getvalue('address'), 'sku': form.getvalue('sku')})
    connection.commit()
    cursor.close()

    print('<h1>Supplier added with sucess.</h1>')
    print('<a href="suppliers.cgi">go back</a>>')
    print('</body>') 

except Exception as e:
    print('<a href="form_supplier.cgi">Please try again</a>')
    view.handle_exception(e)    
finally:
    if connection is not None:
        connection.close()
        
print('</body>')
print('</html>')