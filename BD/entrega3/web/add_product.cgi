#!/usr/bin/python3
import psycopg2
import login
import cgi
import view

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Add Product Page</title>')
print('</head>')
print('<body>')
print('<h1>Product added with sucess.</h1>')
print('<a href="products.cgi">go back</a>>')
    
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    form = cgi.FieldStorage()
    
    sql = "INSERT INTO product VALUES(%(sku)s, %(name)s, %(description)s, %(price)s, %(ean)s)"
    cursor.execute(sql, {'sku': form.getvalue('sku'), 'name': form.getvalue('name'), 'description': form.getvalue('description'), 'price': form.getvalue('price'), 'ean': form.getvalue('ean')})
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