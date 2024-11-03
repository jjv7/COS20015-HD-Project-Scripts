from pymongo import MongoClient, WriteConcern
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from datetime import datetime
from pytz import timezone, utc
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
client = MongoClient(
    host=os.getenv("MONGODB_URI"),
    username=os.getenv("MONGODB_USER"),
    password=os.getenv("MONGODB_PASSWORD"),
    authSource=os.getenv("MONGODB_AUTHSERVER")
)
adminDb = client["admin"]
db = client[os.getenv("MONGODB_DB")]
print("Connected to database")


# Drop existing collections
db.Product.drop()
db.Factory.drop()
db.Client.drop()
db.Order.drop()
db.Delivery.drop()
db.ShippingCourier.drop()
print("Dropped existing collections")

# Insert factories
db.Factory.insert_many([
    {
        "name": "Kid's beds factory",
        "phone": "0321321321",
        "email": "factory1@kbfactory.com"
    },
    {
        "name": "Modern furniture factory",
        "phone": "0123456789",
        "email": "factory2@mffactory.com"
    },
    {
        "name": "Bunk bed factory",
        "phone": "0987654321",
        "email": "factory3@bbfactory.com"
    },
])

# Obtain factory object IDs
factory1ID = db.Factory.find_one({"name": "Kid's beds factory"})["_id"]
factory2ID = db.Factory.find_one({"name": "Modern furniture factory"})["_id"]
factory3ID = db.Factory.find_one({"name": "Bunk bed factory"})["_id"]

# Insert products
db.Product.insert_many([
    {
        "_id": "KF1001-SBB",
        "name": "Single blue racing car bed",
        "description": "A stylish blue racing car bed for kids",
        "price": Decimal128("500.00"),
        "stock": 100,
        "factory": {
            "id": factory1ID,
            "name": "Kid's beds factory"
        }
    },
    {
        "_id": "KF1001-SBR",
        "name": "Single red racing car bed",
        "description": "A vibrant red racing car bed for kids",
        "price": Decimal128("500.00"),
        "stock": 100,
        "factory": {
            "id": factory1ID,
            "name": "Kid's beds factory"
        }
    },
    {
        "_id": "KF1001-SBY",
        "name": "Single yellow racing car bed",
        "description": "A cheerful yellow racing car bed for kids",
        "price": Decimal128("500.00"),
        "stock": 20,
        "factory": {
            "id": factory1ID,
            "name": "Kid's beds factory"
        }
    },
    {
        "_id": "KF1001-SBG",
        "name": "Single green racing car bed",
        "description": "A dynamic green racing car bed for kids",
        "price": Decimal128("500.00"),
        "stock": 20,
        "factory": {
            "id": factory1ID,
            "name": "Kid's beds factory"
        }
    },
    {
        "_id": "MF2001-KSOW",
        "name": "Oak white modern bed",
        "description": "King single oak white modern bed",
        "price": Decimal128("350.00"),
        "stock": 75,
        "factory": {
            "id": factory2ID,
            "name": "Modern furniture factory"
        }
    },
    {
        "_id": "MF2001-KSG",
        "name": "Grey modern bed",
        "description": "King single grey modern bed",
        "price": Decimal128("350.00"),
        "stock": 80,
        "factory": {
            "id": factory2ID,
            "name": "Modern furniture factory"
        }
    },
    {
        "_id": "BB3001-SW",
        "name": "Wooden bunk bed",
        "description": "Single over single wooden bunk bed",
        "price": Decimal128("700.00"),
        "stock": 50,
        "factory": {
            "id": factory3ID,
            "name": "Bunk bed factory"
        }
    },
    {
        "_id": "BB3002-SODBL",
        "name": "Metal bunk bed frame",
        "description": "Single over double metal bunk bed",
        "price": Decimal128("900.00"),
        "stock": 60,
        "factory": {
            "id": factory3ID,
            "name": "Bunk bed factory"
        }
    }
])

# Insert clients
# Table for addresses and client addresses no longer required due to embedded documents
db.Client.insert_many([
    {
        "name": "Temple & Webster",
        "phone": "0111111111",
        "email": "client1@tpw.com.au",
        "addresses": [
            {
                "streetAddress": "1 TPW Road",
                "state": "VIC",
                "postcode": "3111"
            },
            {
                "streetAddress": "2 TPW Avenue",
                "state": "VIC",
                "postcode": "3145"
            },
            {
                "streetAddress": "3 TPW Crescent",
                "state": "VIC",
                "postcode": "3152"
            }
        ]
    },
    {
        "name": "Fantastic Furniture",
        "phone": "0222222222",
        "email": "client2@fantastic.com.au",
        "addresses": [
            {
                "streetAddress": "1 Fantastic Street",
                "state": "VIC",
                "postcode": "3222"
            },
            {
                "streetAddress": "2 Furniture Avenue",
                "state": "VIC",
                "postcode": "3249"
            }
        ]
    },
    {
        "name": "Sleep Doctor",
        "phone": "0333333333",
        "email": "client3@sleepdoctor.com.au",
        "addresses": [
            {
                "streetAddress": "1 Sleepy Street",
                "state": "NSW",
                "postcode": "2111"
            },
            {
                "streetAddress": "1 Bunk Road",
                "state": "VIC",
                "postcode": "3333"
            }
        ]
    },
    {
        "name": "Going Bunks",
        "phone": "0444444444",
        "email": "client4@goingbunks.com.au",
        "addresses": [
            {
                "streetAddress": "1 Bunk Road",
                "state": "VIC",
                "postcode": "3333"
            }
        ]
    },
    {
        "name": "Forty Winks",
        "phone": "0555555555",
        "email": "client5@fortywinks.com.au",
        "addresses": [
            {
                "streetAddress": "40 Wink Street",
                "state": "VIC",
                "postcode": "3444"
            },
            {
                "streetAddress": "41 Dreamy Lane",
                "state": "VIC",
                "postcode": "3450"
            },
            {
                "streetAddress": "42 Pillow Crescent",
                "state": "VIC",
                "postcode": "3465"
            }
        ]
    },
    {
        "name": "Bedshed",
        "phone": "0666666666",
        "email": "client6@bedshed.com.au",
        "addresses": [
            {
                "streetAddress": "1 Bed Road",
                "state": "VIC",
                "postcode": "3555"
            },
            {
                "streetAddress": "2 Mattress Street",
                "state": "VIC",
                "postcode": "3577"
            }
        ]
    }
])


# Insert shipping couriers
db.ShippingCourier.insert_many([
    {
        "name": "Allied Express",
        "phoneNumber": "0543215432",
        "email": "shipping1@alliedexpress.com.au"
    },
    {
        "name": "Hunter Express",
        "phoneNumber": "0678967896",
        "email": "shipping2@hunterexpress.com.au"
    },
    {
        "name": "Toll IPEC",
        "phoneNumber": "0432143214",
        "email": "shipping3@tollgroup.com"
    }
])

melTZ = timezone("Australia/Melbourne")

# Insert orders
# Here, the client, order items and delivery information have been included
db.Order.insert_many([
    {
        "client": {
            "id": db.Client.find_one({"name": "Temple & Webster"})["_id"],
            "name": "Temple & Webster",
            "phone": "0111111111",
            "email": "client1@tpw.com.au",
            "address": {
                "streetAddress": "1 TPW Road",
                "state": "VIC",
                "postcode": "3111"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 1, 10, 30)),
        "dueDate": melTZ.localize(datetime(2024, 10, 9)),
        "status": "Processing",
        "items": [
            {
                "sku": "KF1001-SBB",
                "name": "Single blue racing car bed",
                "quantity": 10,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "KF1001-SBR",
                "name": "Single red racing car bed",
                "quantity": 10,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity": 5,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",                
                "quantity": 5,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "BB3001-SW",
                "name": "Wooden bunk bed",
                "quantity": 5,
                "salePrice": Decimal128("650.00")
            }
        ]
    },
    {
        "client": {
            "id": db.Client.find_one({"name": "Temple & Webster"})["_id"],
            "name": "Temple & Webster",
            "phone": "0111111111",
            "email": "client1@tpw.com.au",
            "address": {
                "streetAddress": "2 TPW Avenue",
                "state": "VIC",
                "postcode": "3145"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 1, 10, 33)),
        "dueDate": melTZ.localize(datetime(2024, 10, 8)),
        "status": "Awaiting pickup",
        "items": [
            {
                "sku": "KF1001-SBB",
                "name": "Single blue racing car bed",
                "quantity": 10,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "KF1001-SBR",
                "name": "Single red racing car bed",
                "quantity": 5,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity": 4,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",                
                "quantity": 3,
                "salePrice": Decimal128("332.50")
            }
        ],
        "delivery": {
            "shippingCourierID": db.ShippingCourier.find_one({"name": "Allied Express"})["_id"],
            "shippingCourierName": "Allied Express",
            "trackingNumber": "TNW111111111"
        }
    },
    {
        "client": {
            "id": db.Client.find_one({"name": "Fantastic Furniture"})["_id"],
            "name": "Fantastic Furniture",
            "phone": "0222222222",
            "email": "client2@fantastic.com.au",
            "address": {
                "streetAddress": "1 Fantastic Street",
                "state": "VIC",
                "postcode": "3222"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 1, 11, 30)),
        "dueDate": melTZ.localize(datetime(2024, 10, 11)),
        "status": "Processing",
        "items": [
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity": 10,
                "salePrice": Decimal128("340.00")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",                
                "quantity": 10,
                "salePrice": Decimal128("340.00")
            },
            {
                "sku": "BB3001-SW",
                "name": "Wooden bunk bed",
                "quantity": 5,
                "salePrice": Decimal128("680.00")
            }
        ]
    },
    {
        "client": {
            "id": db.Client.find_one({"name": "Fantastic Furniture"})["_id"],
            "name": "Fantastic Furniture",
            "phone": "0222222222",
            "email": "client2@fantastic.com.au",
            "address": {
                "streetAddress": "2 Furniture Avenue",
                "state": "VIC",
                "postcode": "3249"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 2, 11, 59)),
        "dueDate": melTZ.localize(datetime(2024, 10, 7)),
        "status": "Shipped",
        "items": [
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity": 5,
                "salePrice": Decimal128("340.00")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",                
                "quantity": 5,
                "salePrice": Decimal128("340.00")
            },
            {
                "sku": "BB3001-SW",
                "name": "Wooden bunk bed",
                "quantity": 2,
                "salePrice": Decimal128("680.00")
            }
        ],
        "delivery": {
            "shippingCourierID": db.ShippingCourier.find_one({"name": "Hunter Express"})["_id"],
            "shippingCourierName": "Hunter Express",
            "trackingNumber": "H222222",
            "shippingDate": melTZ.localize(datetime(2024, 10, 5))
        }
    },
    {
        "client": {
            "id": db.Client.find_one({"name": "Sleep Doctor"})["_id"],
            "name": "Sleep Doctor",
            "phone": "0333333333",
            "email": "client3@sleepdoctor.com.au",
            "address": {
                "streetAddress": "1 Sleepy Street",
                "state": "NSW",
                "postcode": "2111"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 2, 11, 59)),
        "dueDate": melTZ.localize(datetime(2024, 10, 7)),
        "status": "Awaiting pickup",
        "items": [
            {
                "sku": "KF1001-SBB",
                "name": "Single blue racing car bed",
                "quantity": 20,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "KF1001-SBR",
                "name": "Single red racing car bed",
                "quantity": 20,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "KF1001-SBY",
                "name": "Single yellow racing car bed",
                "quantity": 10,
                "salePrice": Decimal128("450.00")
            },
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity": 5,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",               
                "quantity": 5,
                "salePrice": Decimal128("332.50")
            }
        ],
        "delivery": {
            "shippingCourierID": db.ShippingCourier.find_one({"name": "Allied Express"})["_id"],
            "shippingCourierName": "Allied Express",
            "trackingNumber": "AL333333333"
        }
    },
    {
        "client": {
            "id": db.Client.find_one({"name": "Temple & Webster"})["_id"],
            "name": "Temple & Webster",
            "phone": "0111111111",
            "email": "client1@tpw.com.au",
            "address": {
                "streetAddress": "1 TPW Road",
                "state": "VIC",
                "postcode": "3111"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 7, 9, 30)),
        "dueDate": melTZ.localize(datetime(2024, 10, 18)),
        "status": "Processing",
        "items": [
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity": 10,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",                
                "quantity": 10,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "BB3001-SW",
                "name": "Wooden bunk bed",
                "quantity": 5,
                "salePrice": Decimal128("680.00")
            },
            {
                "sku": "BB3002-SODBL",
                "name": "Metal bunk bed frame",
                "quantity": 5,
                "salePrice": Decimal128("810.00")
            }
        ]
    },
    {
        "client": {
            "id": db.Client.find_one({"name": "Forty Winks"})["_id"],
            "name": "Forty Winks",
            "phone": "0555555555",
            "email": "client5@fortywinks.com.au",
            "address": {
                "streetAddress": "40 Wink Street",
                "state": "VIC",
                "postcode": "3444"
            }
        },
        "orderDate": melTZ.localize(datetime(2024, 10, 3, 10, 45)),
        "dueDate": melTZ.localize(datetime(2024, 10, 10)),
        "status": "Awaiting pickup",
        "items": [
            {
                "sku": "MF2001-KSOW",
                "name": "Oak white modern bed",
                "quantity":10,
                "salePrice": Decimal128("332.50")
            },
            {
                "sku": "MF2001-KSG",
                "name": "Grey modern bed",               
                "quantity": 10,
                "salePrice": Decimal128("332.50")
            }
        ],
        "delivery": {
            "shippingCourierID": db.ShippingCourier.find_one({"name": "Hunter Express"})["_id"],
            "shippingCourierName": "Hunter Express",
            "trackingNumber": "H444444"
        }
    }
])


print("Inserted collections")
print("Database setup completed")