
DROP TABLE IF EXISTS products;
CREATE TABLE products(
    productID INTEGER PRIMARY KEY,
    productName VARCHAR(100),
    supplierID SMALLINT,
    categoryID SMALLINT,
    quantityPerUnit VARCHAR(100),
    unitPrice REAL,
    unitsInStock INTEGER,
    unitsOnOrder INTEGER,
    reorderLevel INTEGER,
    discontinued BOOLEAN
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
 orderID BIGINT PRIMARY KEY,
 customerID VARCHAR(10),
 employeeID SMALLINT,
 orderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 requiredDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 shippedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 shipVia SMALLINT,
 freight REAL,
 shipName VARCHAR(100),
 shipAddress VARCHAR(300),
 shipCity VARCHAR(50),
 shipRegion VARCHAR(50),
 shipPostalCode VARCHAR(50),
 shipCountry VARCHAR(100)
 );

DROP TABLE IF EXISTS order_details;
 CREATE TABLE order_details (
 orderID BIGINT,
 productID SMALLINT,
 unitPrice REAL,
 quantity SMALLINT,
 discount REAL
);

COPY products (productID, productName, supplierID, categoryID, quantityPerUnit, unitPrice, unitsInStock, unitsOnOrder, reorderLevel, discontinued)
FROM '/Users/Flo/Documents/GitHub/projects/week_6/data/products.csv' 
DELIMITER ','
CSV HEADER;

COPY orders (orderID,customerID,employeeID,orderDate,requiredDate,shippedDate,shipVia,freight,shipName,shipAddress,shipCity,shipRegion,shipPostalCode,shipCountry) 
FROM '/Users/Flo/Documents/GitHub/projects/week_6/data/orders.csv'
DELIMITER ','
CSV HEADER;

COPY order_details (orderID,productID,unitPrice,quantity,discount) 
FROM '/Users/Flo/Documents/GitHub/projects/week_6/data/order_details.csv'
DELIMITER ','
CSV HEADER;

--psql -U postgres -f northwind.sql -d northwind
