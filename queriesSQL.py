import mysql.connector
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()


def execute_query(db, query, params=None):
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SET profiling = 1;")
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    cursor.execute("SHOW PROFILES;")
    profiles = cursor.fetchall()

     # Get the last executed query's profiling info
    if profiles:
        lastQueryProfile = profiles[-1] # Get the last query profile
        execTime = lastQueryProfile["Duration"]  # Execution time of the last query
    
    cursor.execute("SET profiling = 0;")
    cursor.close()
    
    return results, execTime


def displayResults(df):
    resultString = df.to_string(index=False)
    separatorLength = max(len(resultString.split('\n')[0]), len(resultString.split('\n')[1]))
    separator = "-" * separatorLength
    print(separator)
    print(resultString)
    print(separator)

def executeRevenueQuery(db):
    revenueQuery = """
    SELECT 
        p.product_SKU, 
        p.product_Name, 
        SUM(oi.orderItem_Quantity) AS Quantity_Sold, 
        SUM(oi.orderItem_Quantity * oi.orderItem_SalePrice) AS Revenue
    FROM OrderItem oi
    JOIN Product p ON oi.product_SKU = p.product_SKU
    GROUP BY p.product_SKU, p.product_Name
    ORDER BY Revenue DESC;
    """
    results, execTime = execute_query(db, revenueQuery)
    df = pd.DataFrame(results)
    displayResults(df)
    print(f"Execution Time: {execTime:.6f} seconds")

def executeUrgentOrdersQuery(db):
    urgentOrdersQuery = """
    SELECT co.clientOrder_ID, c.client_Name, a.address_StreetAddress, a.address_Postcode, co.clientOrder_DueDate, co.clientOrder_Status
    FROM ClientOrder co
    JOIN ClientAddress ca ON co.client_ID = ca.client_ID AND co.address_ID = ca.address_ID
    JOIN Client c ON ca.client_ID = c.client_ID
    JOIN Address a ON ca.address_ID = a.address_ID
    WHERE co.clientOrder_DueDate BETWEEN '2024-10-07' AND '2024-10-07' + INTERVAL 7 DAY
    AND co.clientOrder_Status = 'Processing'
    ORDER BY co.clientOrder_DueDate DESC;
    """
    results, execTime = execute_query(db, urgentOrdersQuery)
    df = pd.DataFrame(results)
    displayResults(df)
    print(f"Execution Time: {execTime:.6f} seconds")

def executeAlliedScQuery(db):
    alliedScQuery = """
    SELECT oi.product_SKU, SUM(oi.orderItem_Quantity) AS quantity, s.shippingCourier_Name
    FROM OrderItem oi
    JOIN ClientOrder o ON oi.clientOrder_ID = o.clientOrder_ID
    JOIN Delivery d ON o.delivery_ID = d.delivery_ID
    JOIN ShippingCourier s on d.shippingCourier_ID = s.shippingCourier_ID
    WHERE s.shippingCourier_Name = 'Allied Express'
    GROUP BY oi.product_SKU;
    """
    results, execTime = execute_query(db, alliedScQuery)
    df = pd.DataFrame(results)
    displayResults(df)
    print(f"Execution Time: {execTime:.6f} seconds")

def executeDiscountQuery(db):
    discountQuery = """
    SELECT 
        co.clientOrder_ID,
        c.client_Name,
        SUM(oi.orderItem_Quantity * p.product_Price) AS Original_Total,
        SUM(oi.orderItem_Quantity * oi.orderItem_SalePrice) AS Sales_Total,
        (SUM(oi.orderItem_Quantity * (p.product_Price - oi.orderItem_SalePrice)) / 
        NULLIF(SUM(oi.orderItem_Quantity * p.product_Price), 0)) * 100 AS Discount_Percentage
    FROM ClientOrder co
    JOIN Client c ON co.client_ID = c.client_ID
    JOIN OrderItem oi ON co.clientOrder_ID = oi.clientOrder_ID
    JOIN Product p ON oi.product_SKU = p.product_SKU
    GROUP BY co.clientOrder_ID
    ORDER BY co.clientOrder_ID;
    """
    results, execTime = execute_query(db, discountQuery)
    df = pd.DataFrame(results)
    displayResults(df)
    print(f"Execution Time: {execTime:.6f} seconds")

def executeOrdersInfoQuery(db):
    ordersInfoQuery = """
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
    FROM ClientOrder co
    JOIN Client c on co.client_ID = c.client_ID
    JOIN Address a on co.address_ID = a.address_ID
    LEFT JOIN Delivery d ON co.delivery_ID = d.delivery_ID
    LEFT JOIN ShippingCourier sc ON d.shippingCourier_ID = sc.shippingCourier_ID
    ORDER BY co.clientOrder_ID;
    """
    results, execTime = execute_query(db, ordersInfoQuery)
    df = pd.DataFrame(results)
    displayResults(df)
    print(f"Execution Time: {execTime:.6f} seconds")

def queryMenu(db):
    finished = False
    
    while not finished:
        print("\nQueries menu:")
        print("1. Total revenue per product")
        print("2. Urgent orders")
        print("3. Order items shipped by Allied Express")
        print("4. Discount on all orders")
        print("5. Order information")
        print("6. Exit program")

        choice = input("Please enter your choice (1-6): ")

        match choice:
            case "1":
                executeRevenueQuery(db)
            case "2":
                executeUrgentOrdersQuery(db)
            case "3":
                executeAlliedScQuery(db)
            case "4":
                executeDiscountQuery(db)
            case "5":
                executeOrdersInfoQuery(db)
            case "6":
                print("Exiting program")
                finished = True
            case _:
                print("Please input an integer (1-6)")

def main():
    # Connect to MySQL
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    print("Connected to database")
    
    queryMenu(db)

    db.close()

if __name__ == "__main__":
    main()
