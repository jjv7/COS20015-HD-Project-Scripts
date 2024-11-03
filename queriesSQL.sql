--------------------------------------------------------------
-- This file contains some useful queries for the orders db --
--------------------------------------------------------------


# Total sales per product
# Useful if you want to tell which products are successful

SELECT 
    p.product_SKU, 
    p.product_Name, 
    SUM(oi.orderItem_Quantity) AS `Quantity Sold`, 
    SUM(oi.orderItem_Quantity * oi.orderItem_SalePrice) AS Revenue
FROM OrderItem oi
JOIN Product p ON oi.product_SKU = p.product_SKU
GROUP BY p.product_SKU, p.product_Name
ORDER BY Revenue DESC;


# Orders due in the next 7 days
# Useful to tell which orders are urgent. 
# CURDATE() has been replaced by '2024-10-07' for consistency from the creation of this query

SELECT co.clientOrder_ID, c.client_Name, a.address_StreetAddress, a.address_State, a.address_Postcode, co.clientOrder_DueDate, co.clientOrder_Status
FROM ClientOrder co
JOIN ClientAddress ca ON co.client_ID = ca.client_ID AND co.address_ID = ca.address_ID
JOIN Client c ON ca.client_ID = c.client_ID
JOIN Address a ON ca.address_ID = a.address_ID
# WHERE co.clientOrder_DueDate BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY
WHERE co.clientOrder_DueDate BETWEEN '2024-10-07' AND '2024-10-07' + INTERVAL 7 DAY
AND co.clientOrder_Status IN ('Processing')
ORDER BY co.clientOrder_DueDate DESC;


# Order items which are shipped by Allied Express
# Useful for knowing which items should be grouped up for pickup

SELECT oi.product_SKU, SUM(oi.orderItem_Quantity) AS `quantity`, s.shippingCourier_Name
FROM OrderItem oi
JOIN ClientOrder o ON oi.clientOrder_ID = o.clientOrder_ID
JOIN Delivery d ON o.delivery_ID = d.delivery_ID
JOIN ShippingCourier s on d.shippingCourier_ID = s.shippingCourier_ID
WHERE s.shippingCourier_Name = 'Allied Express'
GROUP BY oi.product_SKU;


# Discount calculation on orders

SELECT 
    co.clientOrder_ID,
    c.client_Name,
    SUM(oi.orderItem_Quantity * p.product_Price) AS `Original Total`,
    SUM(oi.orderItem_Quantity * oi.orderItem_SalePrice) AS `Sales Total`,
    (SUM(oi.orderItem_Quantity * (p.product_Price - oi.orderItem_SalePrice)) / SUM(oi.orderItem_Quantity * p.product_Price)) * 100 AS `Discount (%)`
FROM ClientOrder co
JOIN Client c ON co.client_ID = c.client_ID
JOIN OrderItem oi ON co.clientOrder_ID = oi.clientOrder_ID
JOIN Product p ON oi.product_SKU = p.product_SKU
GROUP BY co.clientOrder_ID
ORDER BY co.clientOrder_ID;


# Complete information on orders
# This information is useful for keeping track of company orders
# The delivery information is useful for keeping track of which shipping company sent the product in case of any issues

SELECT
    co.clientOrder_ID,
    c.client_Name,
    c.client_Phone,
    c.client_Email,
    a.address_StreetAddress,
    a.address_State,
    a.address_Postcode,
    co.clientOrder_Date,
    co.clientOrder_DueDate,
    co.clientOrder_Status,
    sc.shippingCourier_Name,
    d.delivery_TrackingNumber,
    d.delivery_ShippingDate
FROM clientOrder co
JOIN Client c on co.client_ID = c.client_ID
JOIN Address a on co.address_ID = a.address_ID
LEFT JOIN Delivery d ON co.delivery_ID = d.delivery_ID
LEFT JOIN ShippingCourier sc ON d.shippingCourier_ID = sc.shippingCourier_ID
ORDER BY co.clientOrder_ID;