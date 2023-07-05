num_entries = 1000000  # Specify the number of entries you want to generate

def generate_insert_queries(n):
    for i in range(n):
        address = f"'{i} Example St'"
        lat = round(0.0000 + i * 0.0001, 4)
        lon = round(0.0000 - i * 0.0001, 4)
        entry = f"    ({address}, {lat}, {lon})"
        if i < n - 1:
            entry += ","
        print(entry)


print(""" -- workplace and offices/warehouse need to be populated in a transaction due to RI-2
START	TRANSACTION;
SET	CONSTRAINTS	ALL	DEFERRED;
        
INSERT INTO workplace (address, lat, long) \nVALUES"""
      )
generate_insert_queries(num_entries)
print(";")

def generate_street_names(start, end):
    for i in range(start, end + 1):
        street_name = f"    ('{i} Example St')"
        if i < end:
            street_name += ","
        print(street_name)

print("INSERT INTO office (address) \nVALUES")
start_index = 1  # Specify the start index of the street names
end_index = int(num_entries/2)  # Specify the end index of the street names
street_names = generate_street_names(start_index, end_index)
print(";")

print("INSERT INTO warehouse (address) \nVALUES")
start_index = int(num_entries/2)  # Specify the start index of the street names
end_index = num_entries-1  # Specify the end index of the street names
street_names = generate_street_names(start_index, end_index)
print(";")

print("\nCOMMIT;\n")


#------------------------------------------------------------------------------------------------------------------------


departments = [
    'Sales',
    'Marketing',
    'Finance',
    'Human Resources',
    'Operations',
    'Information Technology',
    'Research and Development',
    'Customer Service',
    'Product Management',
    'Quality Assurance',
    'Supply Chain',
    'Legal',
    'Administration',
    'Business Development',
    'Training and Development',
    'Public Relations',
    'Accounting',
    'Engineering',
    'Design',
    'Purchasing',
    'Project Management',
    'Data Analytics',
    'Logistics',
    'Corporate Communications',
    'Risk Management',
    'Strategic Planning',
    'Internal Audit',
    'Facilities Management',
    'Consulting',
    'Compliance',
    'Event Management',
    'Employee Relations',
    'Investor Relations',
    'Health and Safety',
    'Procurement',
    'Software Development',
    'Graphic Design',
    'Sales Operations',
    'Training',
    'Operations Management'
]

def print_departments(departments):
    print("INSERT INTO department (name)")
    print("VALUES")

    for department in departments:
        if department != departments[-1]: print(f"    ('{department}'),")
        else: print(f"    ('{department}')")

    print(";")

# Call the function
print_departments(departments)



from datetime import datetime, timedelta
def generate_employee_entries(n):
    ssn = 1000000000
    tin = 2000000000
    bdate_start = '1990-01-01'
    name_start = 'Employee'
    print("INSERT INTO employee (ssn, TIN, bdate, name)\nVALUES\n")
    
    for i in range(n):
        ssn += 1
        tin += 1
        if (i%1000==0): bdate = (datetime.strptime(bdate_start, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        name = f'{name_start} {i+1}'
        entry = f"({ssn}, {tin}, '{bdate}', '{name}')"
        if i < n - 1:
            entry += ","
        print(entry)

    print(";")


generate_employee_entries(num_entries)



def print_works(entries, departments):
    print("INSERT INTO works (ssn, address, name)")
    print("VALUES")
    ssn = 1000000000

    for i in range(entries):
        ssn += 1
        address = "{i} Example St".format(i=i)
        department = departments[i % len(departments)]
        if i<entries-1: print(f"    ({ssn}, '{address}', '{department}'),")
        else: print(f"    ({ssn}, '{address}', '{department}')")

    print(";")

print_works(num_entries, departments)


import random

start_sku = 1
end_sku = num_entries
base_ean = 1000000000000

print("INSERT INTO product (sku, name, description, price, ean)")
print("VALUES")

for sku in range(start_sku, end_sku + 1):
    product_name = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}Product{sku}"
    description = "Product description"
    price = round(random.uniform(0, 100), 2)
    ean = base_ean + sku

    if sku < end_sku: print(f"    ('SKU{sku:03}', '{product_name}', '{description}', {price}, '{ean}'),")
    else: print(f"    ('SKU{sku:03}', '{product_name}', '{description}', {price}, '{ean}');")


print("INSERT INTO supplier (TIN, name, address, sku)")
print("VALUES")
print("    (1234567890, 'Supplier A', '123 Example St', 'SKU001'),")
print("    (2345678901, 'Supplier B', '456 Example St', 'SKU002'),")
print("    (3456789012, 'Supplier C', '789 Example St', 'SKU003'),")
print("    (4567890123, 'Supplier D', '123 Example St', 'SKU004'),")
print("    (5678901234, 'Supplier E', '456 Example St', 'SKU005'),")
print("    (6789012345, 'Supplier F', '789 Example St', 'SKU006'),")
print("    (7890123456, 'Supplier G', '123 Example St', 'SKU007'),")
print("    (8901234567, 'Supplier H', '456 Example St', 'SKU008'),")
print("    (9012345678, 'Supplier I', '789 Example St', 'SKU009'),")
print("    (1234567891, 'Supplier J', '123 Example St', 'SKU010'),")
print("    (2345678902, 'Supplier K', '456 Example St', 'SKU011'),")
print("    (3456789013, 'Supplier L', '789 Example St', 'SKU012'),")
print("    (4567890124, 'Supplier M', '123 Example St', 'SKU013'),")
print("    (5678901235, 'Supplier N', '456 Example St', 'SKU014'),")
print("    (6789012346, 'Supplier O', '789 Example St', 'SKU015'),")
print("    (7890123457, 'Supplier P', '123 Example St', 'SKU016'),")
print("    (8901234568, 'Supplier Q', '456 Example St', 'SKU017'),")
print("    (9012345679, 'Supplier R', '789 Example St', 'SKU018'),")
print("    (1234567892, 'Supplier S', '123 Example St', 'SKU019'),")
print("    (2345678903, 'Supplier T', '456 Example St', 'SKU020')")
print(";")


print("INSERT INTO delivery (address, TIN)")
print("VALUES")
print("    ('{i} Example St', 1234567890),".format(i=num_entries-1))
print("    ('{i} Example St', 2345678901),".format(i=num_entries-1))
print("    ('{i} Example St', 3456789012),".format(i=num_entries-1))
print("    ('{i} Example St', 4567890123),".format(i=num_entries-1))
print("    ('{i} Example St', 5678901234),".format(i=num_entries-1))
print("    ('{i} Example St', 6789012345),".format(i=num_entries-1))
print("    ('{i} Example St', 7890123456),".format(i=num_entries-1))
print("    ('{i} Example St', 8901234567),".format(i=num_entries-1))
print("    ('{i} Example St', 9012345678),".format(i=num_entries-1))
print("    ('{i} Example St', 1234567891),".format(i=num_entries-1))
print("    ('{i} Example St', 2345678902),".format(i=num_entries-1))
print("    ('{i} Example St', 3456789013),".format(i=num_entries-1))
print("    ('{i} Example St', 4567890124),".format(i=num_entries-1))
print("    ('{i} Example St', 5678901235),".format(i=num_entries-1))
print("    ('{i} Example St', 6789012346),".format(i=num_entries-1))
print("    ('{i} Example St', 7890123457),".format(i=num_entries-1))
print("    ('{i} Example St', 8901234568),".format(i=num_entries-1))
print("    ('{i} Example St', 9012345679),".format(i=num_entries-1))
print("    ('{i} Example St', 1234567892),".format(i=num_entries-1))
print("    ('{i} Example St', 2345678903)".format(i=num_entries-1))
print(";")


#-------------------------------------------------------------------------------------

import random

def generate_customers(n):
    for i in range(1, n + 1):
        cust_no = 1000 + i
        name = f"Customer {i}"
        email = f"customer{i}@example.com"
        phone = random.randint(1000000000, 9999999999)
        address = f"{i} Example St {random.randint(10000, 99999)} City{i}"
        entry = (cust_no, name, email, phone, address)
        if i < n: print(f"    {entry},")
        else: print(f"    {entry};\n")

print("INSERT INTO customer (cust_no, name, email, phone, address)\nVALUES\n")
generate_customers(num_entries)


def generate_order_entries(num_entries):
    order_no = 2000
    cust_no = 1000

    for i in range(num_entries):
        order_no += 1
        cust_no += 1
        date = random_date()
        entry = (order_no, date, cust_no)
        if i < num_entries - 1: print(f"    {entry},")
        else: print(f"    {entry}")

    print(";")

def random_date():
    year = 2022
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    date = f"{year:04d}-{month:02d}-{day:02d}"
    return date

print(""" -- orders need to be in contains due to RI-3
START	TRANSACTION;
SET	CONSTRAINTS	ALL	DEFERRED;""")
      
print("""INSERT INTO order_ (order_no, date, cust_no)
VALUES""")
generate_order_entries(num_entries)



def generate_contains_entries(num_entries):

    order_no = 2000
    for i in range(num_entries):
        sku = generate_sku()
        order_no += 1
        qty = random.randint(1, 10)

        entry = (sku, order_no, qty)
        if i < num_entries - 1: print(f"    {entry},")
        else: print(f"    {entry}")

    print(";")

def generate_sku():
    sku_number = random.randint(1, 20)
    sku = f"SKU{sku_number:03d}"
    return sku


print("""INSERT INTO contains (sku, order_no, qty)
VALUES""")
generate_contains_entries(num_entries)


print("COMMIT;")


print("""INSERT INTO pay (cust_no, order_no)
VALUES""")
def generate_pays(num_entries):
    cust_no = 1000
    order_no = 2000

    for i in range(int(num_entries/2)):
        cust_no += 1
        order_no += 1
        entry = (cust_no, order_no)
        if i < int(num_entries/2) - 1: print(f"    {entry},")
        else: print(f"    {entry}")

    print(";")

generate_pays(num_entries)



print("""INSERT INTO process (ssn, order_no)
VALUES""")
def generate_process(num_entries):
    ssn = 1000000000
    order_no = 2000

    for i in range(int(num_entries/2)):
        ssn += 1
        order_no += 1
        entry = (ssn, order_no)
        if i < int(num_entries/2) - 1: print(f"    {entry},")
        else: print(f"    {entry}")

    print(";")

generate_process(num_entries)