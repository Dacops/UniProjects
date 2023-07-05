#!/usr/bin/python3
import psycopg2
import login


def handle_exception(exception_message):
    print('<head>')
    print('<link rel="stylesheet" href="error-style.css">') 
    print('<title>Error</title>')
    print('</head>')
    print('<body>')
    print('<div class="error-container">')
    print('<img src="error-image.jpeg" alt="Error Image" class="error-image">')
    print('<p class="error-message">{}</p>'.format(exception_message))
    print('</div>')

def viewTable(sql,tableName,removeScript,addForm):
    print('Content-type:text/html\n\n')
    print('<html>')
    print('<link rel="stylesheet" href="main-style.css">')
    print('<head>')
    print('<title>Project {}</title>'.format(addForm))
    print('</head>')
    print('<h1 style="color: #000000" >{}</h1>'.format(tableName))
    print('<body>')
    connection = None

    try:
        #creating connection
        connection = psycopg2.connect(login.credentials)
        cursor = connection.cursor()

        cursor.execute(sql)
        result = cursor.fetchall()
        
        len_row = len(result[0])

        if tableName == "Orders":
            names = ["Order", "Customer", "Date"]
        elif tableName == "Suppliers":
            names = ["TIN", "Name", "Address", "Product"]
        elif tableName == "Customers":
            names = ["Customer", "Name", "E-MAIL" ,"Phone", "Address"]
        elif tableName == "Products":
            names = ["Product", "Name", "Description", "Price", "EAN"]

        #Dislpaying results
        print('<table border="1" cellspacing="20" align="center">')
        print('<tr>')
        for i in range(len_row):
            print('<td align="center">{}</td>'.format(names[i]))
        print('<td align="center"><a href="{}" class="button" >Add</a></td>'.format(addForm))
        print('</tr>')
        for row in result:
            print('<tr>')
            for value in row:
                print('<td align="center">{}</td>'.format(value))
            if tableName != "Orders":
                print('<td align="center"><a href="{}?number={}" class="button">remove</a></td>'.format(removeScript,row[0]))
            if tableName == "Products":
                print('<td align="center"><a href="form_update_product.cgi?sku={}" class="button">update</a></td>'.format(row[0]))
            elif tableName == "Orders":
                print('<td align="center"><a href="add_payment.cgi?order_no={}" class="button">pay</a></td>'.format(row[0]))
            print('<tr>')
        print('</table>')
        
        #print lastStrip div
        print('<div id="lastStripe">')
        print('<p>')
        print('<a align="center" href="customers.cgi">Customers</a></td>')
        print('<a align="center" href="suppliers.cgi">Suppliers</a></td>')
        print('<a align="center" href="orders.cgi">Orders</a></td>')
        print('<a align="center" href="products.cgi">Products</a></td>')
        print('</p>')

        #closing connection
        cursor.close()
        connection.close()
    except Exception as e:
        handle_exception(e)
    finally:
        if connection is not None:
            connection.close()

    print('</body>')
    print('</html>')