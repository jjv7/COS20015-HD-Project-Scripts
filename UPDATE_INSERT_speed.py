import time
import mysql.connector
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)
mysqlCursor = connection.cursor()


mongoClient = MongoClient(
    host=os.getenv("MONGODB_URI"),
    username=os.getenv("MONGODB_USER"),
    password=os.getenv("MONGODB_PASSWORD"),
    authSource=os.getenv("MONGODB_AUTHSERVER")
)
mongoDb = mongoClient[os.getenv("MONGODB_DB")]
mongoCollection = mongoDb["Client"]


clientData = {
    "client_Name": "John Doe",
    "client_Phone": "12345678910",
    "client_Email": "test@email.com"
}

mysqlInsertTimes = []
mysqlUpdateTimes = []
mongoInsertTimes = []
mongoUpdateTimes = []



def mysqlInsert():
    mysqlCursor.execute("DELETE FROM Client WHERE client_Email = %s", (clientData["client_Email"],))
    mysqlCursor.execute("SET profiling = 1;")                                                                # Enable profiling for this session
    insertQuery = "INSERT INTO Client (client_Name, client_Phone, client_Email) VALUES (%s, %s, %s)"
    mysqlCursor.execute(insertQuery, (clientData["client_Name"], clientData["client_Phone"], clientData["client_Email"]))
    connection.commit()
    
    # Retrieve and print execution time
    mysqlCursor.execute("SHOW PROFILES;")
    profiles = mysqlCursor.fetchall()
    if profiles:
        # Get the last executed query's profiling info
        lastQueryProfile = profiles[-1]
        execTime = lastQueryProfile[1]      # Execution time of the last query
        mysqlInsertTimes.append(execTime)


def mysqlUpdate():
    mysqlCursor.execute("SET profiling = 1;")                                                                 # Enable profiling for this session
    updateQuery = "UPDATE Client SET client_Name = %s WHERE client_Email = %s"
    mysqlCursor.execute(updateQuery, ("Jane Doe", clientData["client_Email"]))
    connection.commit()
    
    # Retrieve and print execution time
    mysqlCursor.execute("SHOW PROFILES;")
    profiles = mysqlCursor.fetchall()
    if profiles:
        # Get the last executed query's profiling info
        lastQueryProfile = profiles[-1]
        execTime = lastQueryProfile[1]      # Execution time of the last query
        mysqlUpdateTimes.append(execTime)


def mongoInsert():
    mongoCollection.delete_many({})         # Clear the collection before each insert
    startTime = time.time()
    mongoCollection.insert_one(clientData)
    execTime = time.time() - startTime
    mongoInsertTimes.append(execTime)


def mongoUpdate():
    startTime = time.time()
    mongoCollection.update_one({"client_Email": clientData["client_Email"]}, {"$set": {"client_Name": "Jane Doe"}})
    execTime = time.time() - startTime
    mongoUpdateTimes.append(execTime)

print("-----Testing MySQL-----")
for i in range(10):
    mysqlInsert()
    mysqlUpdate()

print("\n-----Testing MongoDB-----")
for i in range(10):
    mongoInsert()
    mongoUpdate()

def calculate_average(times):
    return sum(times) / len(times) if times else 0

print("\n-----Execution Times-----")
print(f"MySQL INSERT Execution Times: {mysqlInsertTimes}")
print(f"MySQL UPDATE Execution Times: {mysqlUpdateTimes}")
print(f"MongoDB INSERT Execution Times: {mongoInsertTimes}")
print(f"MongoDB UPDATE Execution Times: {mongoUpdateTimes}")

print("\n-----Average Execution Times-----")
print(f"MySQL INSERT Average Time: {calculate_average(mysqlInsertTimes):.6f} seconds")
print(f"MySQL UPDATE Average Time: {calculate_average(mysqlUpdateTimes):.6f} seconds")
print(f"MongoDB INSERT Average Time: {calculate_average(mongoInsertTimes):.6f} seconds")
print(f"MongoDB UPDATE Average Time: {calculate_average(mongoUpdateTimes):.6f} seconds")

# Close connections
mysqlCursor.close()
connection.close()
mongoClient.close()
