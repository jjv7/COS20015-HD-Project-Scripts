------------------------------------------------------------
-- Run thisSQL script to create/reset the orders database --
------------------------------------------------------------

DROP DATABASE IF EXISTS `orders`;

CREATE DATABASE `orders` DEFAULT CHARACTER SET utf8mb4;

USE `orders`;

DROP TABLE IF EXISTS `Factory`;
DROP TABLE IF EXISTS `Product`;
DROP TABLE IF EXISTS `Client`;
DROP TABLE IF EXISTS `Address`;
DROP TABLE IF EXISTS `ClientAddress`;
DROP TABLE IF EXISTS `ShippingCourier`;
DROP TABLE IF EXISTS `Delivery`;
DROP TABLE IF EXISTS `ClientOrder`;
DROP TABLE IF EXISTS `OrderItem`;

--
-- Create Factory table
--

CREATE TABLE `Factory` (
  factory_ID INT UNSIGNED AUTO_INCREMENT NOT NULL,
  factory_Name VARCHAR(100) NOT NULL,
  factory_Phone CHAR(12) NOT NULL,
  factory_Email VARCHAR(100) NOT NULL,
  PRIMARY KEY (factory_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

--
-- Create Product table
--

CREATE TABLE `Product` (
  product_SKU VARCHAR(20) NOT NULL,
  product_Name VARCHAR(50) NOT NULL,
  product_Description TEXT,
  product_Price DECIMAL(7, 2) NOT NULL,
  product_Stock INT UNSIGNED NOT NULL,
  factory_ID INT UNSIGNED NOT NULL,
  PRIMARY KEY (product_SKU),
  FOREIGN KEY (factory_ID) REFERENCES `Factory`(factory_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create Client table
--

CREATE TABLE `Client` (
  client_ID INT UNSIGNED AUTO_INCREMENT NOT NULL,
  client_Name VARCHAR(100) NOT NULL,
  client_Phone CHAR(12) NOT NULL,
  client_Email VARCHAR(100) NOT NULL,
  PRIMARY KEY (client_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create Address table
--

CREATE TABLE `Address` (
  address_ID INT UNSIGNED AUTO_INCREMENT NOT NULL,
  address_StreetAddress VARCHAR(150) NOT NULL,
  address_State CHAR(3) NOT NULL,
  address_Postcode CHAR(4) NOT NULL,
  PRIMARY KEY (address_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create ClientAddress table
--

CREATE TABLE `ClientAddress` (
  client_ID INT UNSIGNED NOT NULL,
  address_ID INT UNSIGNED NOT NULL,
  PRIMARY KEY (client_ID, address_ID),
  FOREIGN KEY (client_ID) REFERENCES `Client`(client_ID),
  FOREIGN KEY (address_ID) REFERENCES `Address`(address_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create ShippingCourier table
--

CREATE TABLE `ShippingCourier` (
  shippingCourier_ID INT UNSIGNED AUTO_INCREMENT NOT NULL,
  shippingCourier_Name VARCHAR(100) NOT NULL,
  shippingCourier_Phone CHAR(12) NOT NULL,
  shippingCourier_Email VARCHAR(100) NOT NULL,
  PRIMARY KEY (shippingCourier_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create Delivery table
--

CREATE TABLE `Delivery` (
  delivery_ID INT UNSIGNED AUTO_INCREMENT NOT NULL,
  shippingCourier_ID INT UNSIGNED NOT NULL,
  delivery_TrackingNumber VARCHAR(20) NOT NULL,
  delivery_ShippingDate DATE,
  PRIMARY KEY (delivery_ID),
  FOREIGN KEY (shippingCourier_ID) REFERENCES `ShippingCourier`(shippingCourier_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create ClientOrder table
--

CREATE TABLE `ClientOrder` (
  clientOrder_ID INT UNSIGNED AUTO_INCREMENT NOT NULL,
  client_ID INT UNSIGNED NOT NULL,
  address_ID INT UNSIGNED NOT NULL,
  clientOrder_Date DATE NOT NULL,
  clientOrder_Time TIME NOT NULL,
  clientOrder_DueDate DATE NOT NULL,
  clientOrder_Status VARCHAR(15) NOT NULL,
  delivery_ID INT UNSIGNED NULL,
  PRIMARY KEY (clientOrder_ID),
  FOREIGN KEY (client_ID, address_ID) REFERENCES `ClientAddress`(client_ID, address_ID),
  FOREIGN KEY (delivery_ID) REFERENCES `Delivery`(delivery_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Create OrderItem table
--

CREATE TABLE `OrderItem` (
  clientOrder_ID INT UNSIGNED NOT NULL,
  orderItem_Number INT UNSIGNED NOT NULL,
  product_SKU VARCHAR(20) NOT NULL,
  orderItem_Quantity INT UNSIGNED NOT NULL,
  orderItem_SalePrice DECIMAL(7, 2) NOT NULL,
  PRIMARY KEY (clientOrder_ID, orderItem_Number),
  FOREIGN KEY (clientOrder_ID) REFERENCES `ClientOrder`(clientOrder_ID),
  FOREIGN KEY (product_SKU) REFERENCES `Product`(product_SKU)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


--
-- Insert table data
--

# Factory table data

INSERT INTO `Factory` (`factory_Name`, `factory_Phone`, `factory_Email`)
VALUES
('Kid''s beds factory', '0321321321', 'factory1@kbfactory.com'),
('Modern furniture factory', '0123456789', 'factory2@mffactory.com'),
('Bunk bed factory', '0987654321', 'factory3@bbfactory.com');

# Product table data

INSERT INTO `Product` (`product_SKU`, `product_Name`, `product_Description`, `product_Price`, `product_Stock`, `factory_ID`) 
VALUES 
('KF1001-SBB', 'Single blue racing car bed', 'A stylish blue racing car bed for kids', 500.00, 100, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Kid''s beds factory')),
('KF1001-SBR', 'Single red racing car bed', 'A vibrant red racing car bed for kids', 500.00, 100, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Kid''s beds factory')),
('KF1001-SBY', 'Single yellow racing car bed', 'A cheerful yellow racing car bed for kids', 500.00, 20, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Kid''s beds factory')),
('KF1001-SBG', 'Single green racing car bed', 'A dynamic green racing car bed for kids', 500.00, 20, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Kid''s beds factory')),
('MF2001-KSOW', 'Oak white modern bed', 'King single oak white modern bed', 350.00, 75, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Modern furniture factory')),
('MF2001-KSG', 'Grey modern bed', 'King single grey modern bed', 350.00, 80, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Modern furniture factory')),
('BB3001-SW', 'Wooden bunk bed', 'Single over single wooden bunk bed', 700.00, 50, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Bunk bed factory')),
('BB3002-SODBL', 'Metal bunk bed frame', 'Single over double metal bunk bed', 900.00, 60, (SELECT `factory_ID` FROM `Factory` WHERE `factory_Name` = 'Bunk bed factory'));

# Client table data

INSERT INTO `Client` (`client_Name`, `client_Phone`, `client_Email`) 
VALUES 
('Temple & Webster', '0111111111', 'client1@tpw.com.au'),
('Fantastic Furniture', '0222222222', 'client2@fantastic.com.au'),
('Sleep Doctor', '0333333333', 'client3@sleepdoctor.com.au'),
('Going Bunks', '0444444444', 'client4@goingbunks.com.au'),
('Forty Winks', '0555555555', 'client5@fortywinks.com.au'),
('Bedshed', '0666666666', 'client6@bedshed.com.au');

# Address table data

INSERT INTO `Address` (`address_StreetAddress`, `address_State`, `address_Postcode`) 
VALUES 
('1 TPW Road', 'VIC', '3111'),
('2 TPW Avenue', 'VIC', '3145'),
('3 TPW Crescent', 'VIC', '3152'),
('1 Fantastic Street', 'VIC', '3222'),
('2 Furniture Avenue', 'VIC', '3249'),
('1 Sleepy Street', 'NSW', '2111'),
('1 Bunk Road', 'VIC', '3333'),
('40 Wink Street', 'VIC', '3444'),
('41 Dreamy Lane', 'VIC', '3450'),
('42 Pillow Crescent', 'VIC', '3465'),
('1 Bed Road', 'VIC', '3555'),
('2 Mattress Street', 'VIC', '3577');

# ClientAddress table data

INSERT INTO `ClientAddress` (`client_ID`, `address_ID`)
VALUES
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Temple & Webster'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '1 TPW Road' AND `address_Postcode` = '3111')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Temple & Webster'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '2 TPW Avenue' AND `address_Postcode` = '3145')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Temple & Webster'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '3 TPW Crescent' AND `address_Postcode` = '3152')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Fantastic Furniture'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '1 Fantastic Street' AND `address_Postcode` = '3222')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Fantastic Furniture'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '2 Furniture Avenue' AND `address_Postcode` = '3249')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Sleep Doctor'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '1 Sleepy Street' AND `address_Postcode` = '2111')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Sleep Doctor'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '1 Bunk Road' AND `address_Postcode` = '3333')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Going Bunks'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '1 Bunk Road' AND `address_Postcode` = '3333')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Forty Winks'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '40 Wink Street' AND `address_Postcode` = '3444')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Forty Winks'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '41 Dreamy Lane' AND `address_Postcode` = '3450')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Forty Winks'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '42 Pillow Crescent' AND `address_Postcode` = '3465')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Bedshed'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '1 Bed Road' AND `address_Postcode` = '3555')),
((SELECT `client_ID` FROM `Client` WHERE `client_Name` = 'Bedshed'), (SELECT `address_ID` FROM `Address` WHERE `address_StreetAddress` = '2 Mattress Street' AND `address_Postcode` = '3577'));

# ShippingCourier table data

INSERT INTO `ShippingCourier` (`shippingCourier_Name`, `shippingCourier_Phone`, `shippingCourier_Email`)
VALUES 
('Allied Express', '0543215432', 'shipping1@alliedexpress.com.au'),
('Hunter Express', '0678967896', 'shipping2@hunterexpress.com.au'),
('Toll IPEC', '0432143214', 'shipping3@tollgroup.com');

# Delivery table data

INSERT INTO `Delivery` (`shippingCourier_ID`, `delivery_TrackingNumber`, `delivery_ShippingDate`)
VALUES
((SELECT `shippingCourier_ID` FROM `ShippingCourier` WHERE `shippingCourier_Name` = 'Allied Express'), 'TNW111111111', NULL),
((SELECT `shippingCourier_ID` FROM `ShippingCourier` WHERE `shippingCourier_Name` = 'Hunter Express'), 'H222222', '2024-10-05'),
((SELECT `shippingCourier_ID` FROM `ShippingCourier` WHERE `shippingCourier_Name` = 'Allied Express'), 'AL333333333', NULL),
((SELECT `shippingCourier_ID` FROM `ShippingCourier` WHERE `shippingCourier_Name` = 'Hunter Express'), 'H444444', NULL);

# ClientOrder table data

INSERT INTO `ClientOrder` (client_ID, address_ID, clientOrder_Date, clientOrder_Time, clientOrder_DueDate, clientOrder_Status, delivery_ID) 
VALUES 
((SELECT client_ID FROM Client WHERE client_Name = 'Temple & Webster'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '1 TPW Road' AND address_Postcode = '3111'), '2024-10-01', '10:30', '2024-10-09', 'Processing', NULL),
((SELECT client_ID FROM Client WHERE client_Name = 'Temple & Webster'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '2 TPW Avenue' AND address_Postcode = '3145'), '2024-10-01', '10:33', '2024-10-08', 'Awaiting pickup', (SELECT delivery_ID FROM Delivery WHERE delivery_TrackingNumber = 'TNW111111111')),
((SELECT client_ID FROM Client WHERE client_Name = 'Fantastic Furniture'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '1 Fantastic Street' AND address_Postcode = '3222'), '2024-10-01', '11:30', '2024-10-11', 'Processing', NULL),
((SELECT client_ID FROM Client WHERE client_Name = 'Fantastic Furniture'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '2 Furniture Avenue' AND address_Postcode = '3249'), '2024-10-02', '11:59', '2024-10-07', 'Shipped', (SELECT delivery_ID FROM Delivery WHERE delivery_TrackingNumber = 'H222222')),
((SELECT client_ID FROM Client WHERE client_Name = 'Sleep Doctor'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '1 Sleepy Street' AND address_Postcode = '2111'), '2024-10-02', '11:59', '2024-10-07', 'Awaiting pickup', (SELECT delivery_ID FROM Delivery WHERE delivery_TrackingNumber = 'AL333333333')),
((SELECT client_ID FROM Client WHERE client_Name = 'Temple & Webster'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '1 TPW Road' AND address_Postcode = '3111'), '2024-10-07', '09:30', '2024-10-18', 'Processing', NULL),
((SELECT client_ID FROM Client WHERE client_Name = 'Forty Winks'), (SELECT address_ID FROM Address WHERE address_StreetAddress = '40 Wink Street' AND address_Postcode = '3444'), '2024-10-03', '10:45', '2024-10-10', 'Awaiting pickup', (SELECT delivery_ID FROM Delivery WHERE delivery_TrackingNumber = 'H444444'));

# OrderItem table data

INSERT INTO `OrderItem` (clientOrder_ID, orderItem_Number, product_SKU, orderItem_Quantity, orderItem_SalePrice) 
VALUES
(1, 1, 'KF1001-SBB', 10, 450.00),
(1, 2, 'KF1001-SBR', 10, 450.00),
(1, 3, 'MF2001-KSOW', 5, 332.50),
(1, 4, 'MF2001-KSG', 5, 332.50),
(1, 5, 'BB3001-SW', 5, 650.00),
(2, 1, 'KF1001-SBB', 10, 450.00),
(2, 2, 'KF1001-SBR', 5, 450.00),
(2, 3, 'MF2001-KSOW', 4, 332.50),
(2, 4, 'MF2001-KSG', 3, 332.50),
(3, 1, 'MF2001-KSOW', 10, 340.00),
(3, 2, 'MF2001-KSG', 10, 340.00),
(3, 3, 'BB3001-SW', 5, 680.00),
(4, 1, 'MF2001-KSOW', 5, 340.00),
(4, 2, 'MF2001-KSG', 5, 340.00),
(4, 3, 'BB3001-SW', 2, 680.00),
(5, 1, 'KF1001-SBB', 20, 450.00),
(5, 2, 'KF1001-SBR', 20, 450.00),
(5, 3, 'KF1001-SBY', 10, 450.00),
(5, 4, 'MF2001-KSOW', 5, 332.50),
(5, 5, 'MF2001-KSG', 5, 332.50),
(6, 1, 'MF2001-KSOW', 10, 332.50),
(6, 2, 'MF2001-KSG', 10, 332.50),
(6, 3, 'BB3001-SW', 5, 680.00),
(6, 4, 'BB3002-SODBL', 5, 810.00),
(7, 1, 'MF2001-KSOW', 10, 332.50),
(7, 2, 'MF2001-KSG', 10, 332.50);

# This sets the isolation level for handling concurrent users on a global level
SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;