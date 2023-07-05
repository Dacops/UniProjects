#!/usr/bin/python3
import psycopg2
import login
import cgi

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Add Product Page</title>')
print('</head>')
print('<body>')
    
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    form = cgi.FieldStorage()
    
    sql = """
            UPDATE product
            SET price = %(price)s,
                description = %(description)s
            WHERE sku = %(sku)s
          """

    cursor.execute(sql, {'price': form.getvalue('price'), 'description': form.getvalue('description'), 'sku': form.getvalue('sku')})
    connection.commit()
    cursor.close()
    
    print('<h1>Product Updated Sucessfully</h1>')
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