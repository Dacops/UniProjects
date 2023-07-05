DROP TABLE IF EXISTS workplace CASCADE;
DROP TABLE IF EXISTS office CASCADE;
DROP TABLE IF EXISTS warehouse CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS works CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS EAN_product CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS delivery CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS order_ CASCADE;
DROP TABLE IF EXISTS sale CASCADE;
DROP TABLE IF EXISTS pay CASCADE;
DROP TABLE IF EXISTS process CASCADE;
DROP TABLE IF EXISTS contains CASCADE;

CREATE TABLE workplace (
    address VARCHAR(255) NOT NULL,
    lat FLOAT NOT NULL,
    long FLOAT NOT NULL,
    PRIMARY KEY (address),
    UNIQUE (lat, long)
);

CREATE TABLE office (
    address VARCHAR(255) NOT NULL,
    FOREIGN KEY (address) REFERENCES workplace(address)
);

CREATE TABLE warehouse (
    address VARCHAR(255) NOT NULL,
    FOREIGN KEY (address) REFERENCES workplace(address)
);

CREATE TABLE department (
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE employee (
    ssn NUMERIC(20,0) NOT NULL,
    TIN NUMERIC(20,0) NOT NULL,
    bdate DATE NOT NULL,
    name VARCHAR(80) NOT NULL,
    PRIMARY KEY (ssn),
    UNIQUE (TIN)
);

CREATE TABLE works (
    ssn NUMERIC(20,0) NOT NULL,
    address VARCHAR(255) NOT NULL,
    name VARCHAR(80) NOT NULL,
    PRIMARY KEY (ssn, address, name),
    FOREIGN KEY (ssn) REFERENCES employee(ssn),
    FOREIGN KEY (address) REFERENCES workplace(address),
    FOREIGN KEY (name) REFERENCES department(name)
);

CREATE TABLE product (
    sku VARCHAR(50) NOT NULL,
    name VARCHAR(80) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    PRIMARY KEY (sku)
);

CREATE TABLE EAN_product (
    sku VARCHAR(50) NOT NULL,
    ean VARCHAR(50) NOT NULL,
    PRIMARY KEY (sku, ean),
    FOREIGN KEY (sku) REFERENCES product(sku)
);

CREATE TABLE supplier (
    TIN NUMERIC(20,0) NOT NULL,
    name VARCHAR(80) NOT NULL,
    address VARCHAR(255) NOT NULL,
    sku VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (TIN),
    FOREIGN KEY (sku) REFERENCES product(sku)
);

CREATE TABLE delivery (
    address VARCHAR(255) NOT NULL,
    TIN NUMERIC(20,0) NOT NULL,
    sku VARCHAR(50) NOT NULL,
    PRIMARY KEY (address, TIN, sku),
    FOREIGN KEY (address) REFERENCES workplace(address),
    FOREIGN KEY (TIN) REFERENCES supplier(TIN),
    FOREIGN KEY (sku) REFERENCES product(sku)
);

CREATE TABLE customer (
    cust_no NUMERIC(20,0) NOT NULL,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL,
    phone NUMERIC(20,0) NOT NULL,
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY (cust_no),
    UNIQUE (email)
);

 -- added underscore to avoid using reserved word
CREATE TABLE order_ (
    order_no NUMERIC(20,0) NOT NULL,
    date DATE NOT NULL,
    cust_no NUMERIC(20,0) NOT NULL,
    PRIMARY KEY (order_no),
    FOREIGN KEY (cust_no) REFERENCES customer(cust_no)
);

CREATE TABLE sale (
    order_no NUMERIC(20,0) NOT NULL,
    PRIMARY KEY (order_no),
    FOREIGN KEY (order_no) REFERENCES order_( order_no)
);

CREATE TABLE pay (
    cust_no NUMERIC(20,0) NOT NULL,
    order_no NUMERIC(20,0) NOT NULL,
    PRIMARY KEY (cust_no, order_no),
    FOREIGN KEY (cust_no) REFERENCES customer(cust_no),
    FOREIGN KEY (order_no) REFERENCES order_( order_no)
);

CREATE TABLE process (
    ssn NUMERIC(20,0) NOT NULL,
    order_no NUMERIC(20,0) NOT NULL,
    PRIMARY KEY (ssn, order_no),
    FOREIGN KEY (ssn) REFERENCES employee(ssn),
    FOREIGN KEY (order_no) REFERENCES order_( order_no)
);

CREATE TABLE contains (
    sku VARCHAR(50) NOT NULL,
    order_no NUMERIC(20,0) NOT NULL,
    qty INTEGER NOT NULL,
    PRIMARY KEY (sku, order_no),
    FOREIGN KEY (sku) REFERENCES product(sku),
    FOREIGN KEY (order_no) REFERENCES order_( order_no)
);

