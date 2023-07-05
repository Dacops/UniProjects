 <b>
 
 <br>
 workplace(<u>address</u>, lat, long)

 - UNIQUE (lat, long)

 <br>
 office(<u>address</u>)
 
 - address: FK(workplace.address)

 <br>
 warehouse(<u>address</u>)

 - address: FK(workplace.address)

 <br>

 department(<u>name</u>)

 <br>
 employee(<u>ssn</u>, TIN, bdate, name)

 - UNIQUE (TIN)
 - IC-6: Every employee (ssn) must participate in the works association

 <br>
 works(<u>ssn</u>, <u>address</u>, <u>name</u>)

 - ssn: FK(employee)
 - address: FK(workplace)
 - name: FK(department)


 <br>
 <br>
 product(<u>sku</u>, name, description, price)

 - IC-7: Every product (sku) must participate in the supply-contract association

 <br>
 EAN-product(<u>sku</u>, ean)

 - sku: FK(product.sku)

 <br>

 supplier(<u>TIN</u>, name, address, sku, date)

 <br>
 delivery(<u>address</u>, <u>TIN</u>, <u>sku</u>)

 - address: FK(workplace.address)
 - TIN: FK(supplier)
 - sku: FK(product)


 <br>
 <br>
 customer(<u>cust_no</u>, name, email, phone, address)

 - UNIQUE (email)
 - IC-1: Customers can only pay for the Sale of an Order they have placed themselves

 <br>
 order(<u>order_no</u>, date, cust_no)

 - IC-8: Every order (order_no) must participate in the contains association

 <br>
 sale(<u>order_no</u>)

 - order_no: FK(order.order_no)

 <br>
 pay(cust_no, <u>order_no</u>)

 - cust_no: FK(customer)
 - order_no: FK(order.order_no)

 <br>
 process(<u>ssn</u>, <u>order_no</u>)
 
 - ssn: FK(employee)
 - order_no: FK(order)

 <br>
 contains(<u>sku</u>, <u>order_no</u>, qty)

 - sku: FK(product)
 - order_no: FK(order)