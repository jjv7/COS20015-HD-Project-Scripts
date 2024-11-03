from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from datetime import datetime, timedelta
from pytz import timezone, utc
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()

melTZ = timezone("Australia/Melbourne")

# Aggregation pipeline, so we can calculate the sum of sold items and the revenue
revenueQuery = [
    # The embedded items document in each order is unwinded so we can work with each one individually
    # This contains the order items and some product info
    # The embedded info means we don't need to reference any other collection
    {"$unwind": "$items"},

    # GROUP BY product SKU and Name
    # This is to calculate the quantity sold and the revenue
    {
        "$group":  {
            "_id": {
                "product_SKU": "$items.sku",
                "product_Name": "$items.name"
            },
            "Quantity_Sold": {"$sum": "$items.quantity"},
            "Revenue": {"$sum": {"$multiply": ["$items.quantity", "$items.salePrice"]}}
        }
    },

    # ORDER BY Revenue in descending order
    {"$sort": {"Revenue": -1}}
]

# Python dictionary to store the query with the projection
urgentOrdersQuery = {
    # Basically the WHERE clause
    "query": {
        "dueDate": {
            "$gte": melTZ.localize(datetime(2024, 10, 7, 0, 0, 0)).astimezone(utc),
            "$lt": melTZ.localize(datetime(2024, 10, 14, 0, 0, 0)).astimezone(utc)
        },
        "status": "Processing"
    },
    # Basically the SELECT clause
    "projection": {
        "_id": 1,
        "client.name": 1,
        "client.address.streetAddress": 1,
        "client.address.postcode": 1,
        "dueDate": 1,
        "status": 1
    }
}


alliedScQuery = [
    # Match orders shipped by Allied Express
    {"$match": {"delivery.shippingCourierName": "Allied Express"}},

    # Unwind the embedded items document
    {"$unwind": "$items"},

    # Group by the SKU and sum up the quantities sold
    {
        "$group": {
            "_id": "$items.sku",
            "quantity": {"$sum":  "$items.quantity"},
            "shippingCourierName": {"$first": "$delivery.shippingCourierName"}  # Use first to retain the shipping courier name for each grouped document
        }                                                                       # This is safe, since all documents will have "Allied Express"
    }
]

discountQuery = [
    # Expand embedded items document
    {"$unwind": "$items"},
    # This is equivalent to a JOIN
    # Get product document associated with item
    {
        "$lookup": {
            "from": "Product",
            "localField": "items.sku",
            "foreignField": "_id",
            "as": "productDetails"
        }
    },
    # Expand obtained product document
    {"$unwind": "$productDetails"},
    # Group together values according to the order ID
    {
        "$group": {
            "_id": "$_id",
            "clientName": {"$first": "$client.name"},
            "originalTotal": {"$sum": {"$multiply": [{"$toDecimal": "$items.quantity"}, {"$toDecimal": "$productDetails.price"}]}},
            "salesTotal": {"$sum": {"$multiply": [{"$toDecimal": "$items.quantity"}, {"$toDecimal": "$items.salePrice"}]}},
            "totalDiscountAmount": {
                "$sum": {
                    "$multiply": [
                        {"$toDecimal": "$items.quantity"},
                        {"$subtract": [{"$toDecimal": "$productDetails.price"}, {"$toDecimal": "$items.salePrice"}]}
                    ]
                }
            }
        }
    },
    # Fields to display
    # Calculate discount percent
    {
        "$project": {
            "clientName": 1,
            "originalTotal": 1,
            "salesTotal": 1,
            "discountPercentage": {
                "$round": [
                    {
                        "$cond": {
                            "if": {"$gt": ["$originalTotal", Decimal128("0.0")]},
                            "then": {"$multiply": [{"$divide": ["$totalDiscountAmount", "$originalTotal"]}, 100]},
                            "else": Decimal128("0.0")
                        }
                    },
                    2           # Round to 2 decimal places for readability
                ]
            }
        }
    },
    # Order results by their ID
    {"$sort": {"_id": 1}}
]

ordersInfoQuery = {
    # Basically the WHERE clause
    "query": {},
    # Basically the SELECT clause
    "projection": {
        "_id": 1,
        "client.name": 1,
        "client.phone": 1,
        "client.email": 1,
        "client.address.streetAddress": 1,
        "client.address.state": 1,
        "client.address.postcode": 1,
        "orderDate": 1,
        "dueDate": 1,
        "status": 1,
        "delivery.shippingCourierName": 1,
        "delivery.trackingNumber": 1,
        "delivery.shippingDate": 1
    }
}


def displayQueryResults(df):
    resultString = df.to_string(index=False)
    separatorLength = max(len(resultString.split('\n')[0]), len(resultString.split('\n')[1]))  # Find the longest line in the resultString
    separator = "-" * separatorLength

    print(separator)
    print(df.to_string(index=False))
    print(separator)


def executeRevenueQuery(db):
    global revenueQuery

    startTime = time.time()
    results = list(db.Order.aggregate(revenueQuery))
    execTime = time.time() - startTime

    # Create a pandas DataFrame to display the results
    data = {
        "Product SKU:": [result["_id"]["product_SKU"] for result in results],
        "Product Name:": [result["_id"]["product_Name"] for result in results],
        "Quantity Sold:": [result["Quantity_Sold"] for result in results],
        "Revenue:": [result["Revenue"] for result in results],
    }

    df = pd.DataFrame(data)
    displayQueryResults(df)

    print(f"Execution Time: {execTime:.6f} seconds")
    

def executeUrgentOrdersQuery(db):
    global melTZ, urgentOrdersQuery

    startTime = time.time()
    results = list(db.Order.find(urgentOrdersQuery["query"], urgentOrdersQuery["projection"]).sort("dueDate", 1))
    execTime = time.time() - startTime

    # Create a pandas DataFrame to display the results
    data = {
        "Order ID:": [result["_id"] for result in results],
        "Client:": [result["client"]["name"] for result in results],
        "Street Address:": [result["client"]["address"]["streetAddress"] for result in results],
        "Postcode:": [result["client"]["address"]["postcode"] for result in results],
        "Due Date:": [result["dueDate"].replace(tzinfo=utc).astimezone(melTZ).strftime("%Y-%m-%d") for result in results],
        "Status:": [result["status"] for result in results]
    }

    df = pd.DataFrame(data)
    displayQueryResults(df)

    print(f"Execution Time: {execTime:.6f} seconds")


def executeAlliedScQuery(db):
    global alliedScQuery

    startTime = time.time()
    results = list(db.Order.aggregate(alliedScQuery))
    execTime = time.time() - startTime

    # Create a pandas DataFrame to display the results
    data = {
        "Product SKU:": [result["_id"] for result in results],
        "Quantity Sold:": [result["quantity"] for result in results],
        "Shipping Courier:": [result["shippingCourierName"] for result in results],
    }

    df = pd.DataFrame(data)
    displayQueryResults(df)

    print(f"Execution Time: {execTime:.6f} seconds")


def executeDiscountQuery(db):
    global discountQuery

    startTime = time.time()
    results = list(db.Order.aggregate(discountQuery))
    execTime = time.time() - startTime

    # Create a pandas DataFrame to display the results
    data = {
        "Order ID:": [result["_id"] for result in results],
        "Client:": [result["clientName"] for result in results],
        "Original Total:": [result["originalTotal"] for result in results],
        "Sales Total:": [result["salesTotal"] for result in results],
        "Discount (%):": [result["discountPercentage"] for result in results],
    }

    df = pd.DataFrame(data)
    displayQueryResults(df)

    print(f"Execution Time: {execTime:.6f} seconds")


def executeOrdersInfoQuery(db):
    global ordersInfoQuery

    startTime = time.time()
    results = list(db.Order.find(ordersInfoQuery["query"], ordersInfoQuery["projection"]))
    execTime = time.time() - startTime

    # Create a pandas DataFrame to display the results
    data = {
        "Order ID:": [result["_id"] for result in results],
        "Client:": [result["client"]["name"] for result in results],
        "Client Phone:": [result["client"]["phone"] for result in results],
        "Client Email:": [result["client"]["email"] for result in results],
        "Street Address:": [result["client"]["address"]["streetAddress"] for result in results],
        "State:": [result["client"]["address"]["state"] for result in results],
        "Postcode:": [result["client"]["address"]["postcode"] for result in results],
        "Order Date:": [result["orderDate"].replace(tzinfo=utc).astimezone(melTZ).strftime("%Y-%m-%d") for result in results],
        "Due Date:": [result["dueDate"].replace(tzinfo=utc).astimezone(melTZ).strftime("%Y-%m-%d") for result in results],
        "Status:": [result["status"] for result in results],
        "Shipping Courier:": [result.get("delivery", {}).get("shippingCourierName", "N/A") for result in results],
        "Tracking Number:": [result.get("delivery", {}).get("trackingNumber", "N/A") for result in results],
        "Shipping Date:": [
           (result.get("delivery", {}).get("shippingDate", "N/A"))
            if result.get("delivery", {}).get("shippingDate") is None
            else result ["delivery"]["shippingDate"].replace(tzinfo=utc).astimezone(melTZ).strftime("%Y-%m-%d")
            for result in results
        ]
    }

    df = pd.DataFrame(data)
    displayQueryResults(df)

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
    # Connect to MongoDB
    client = MongoClient(
        host=os.getenv("MONGODB_URI"),
        username=os.getenv("MONGODB_USER"),
        password=os.getenv("MONGODB_PASSWORD"),
        authSource=os.getenv("MONGODB_AUTHSERVER")
    )
    db = client[os.getenv("MONGODB_DB")]
    print("Connected to database")
    
    queryMenu(db)

    client.close()



if __name__ == "__main__":
    main()
