#!/usr/bin/python3 
import cgi

form = cgi.FieldStorage()
sku = form.getvalue('sku')

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Remove Customer Page</title>')
print('</head>')
print('<body>')
print('<link rel="stylesheet" href="form-style.css">')
print('<form action="update_product.cgi" method="post">')
print('<h2 align="center">Update Product {}</h2>'.format(sku))
print('<p><input type="hidden" name="sku" value="{}"/></p>'.format(sku))
print('<p>New description: <input type="text" name="description"/></p>')
print('<p>New price: <input type="text" name="price"/></p>')
print('<p><input type="submit" value="Submit"/></p>')
print('</body>')
print('</html>')