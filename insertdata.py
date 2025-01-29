from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('***********')
db = client['***********']

# Insert users
# users = [
#     {"_id": "1", "name": "John Doe", "email": "john@example.com"},
#     {"_id": "2", "name": "Jane Smith", "email": "jane@example.com"}
# ]
# db.users.insert_many(users)

# Insert products
# products = [
#     {"_id": "101", "name": "Laptop", "category": "Electronics", "price": 1200},
#     {"_id": "102", "name": "Headphones", "category": "Electronics", "price": 150}
# ]
# db.products.insert_many(products)

# Insert user-product interactions
interactions = [
    {"userId": "1", "productId": "101", "rating": 5},
    {"userId": "1", "productId": "102", "rating": 4},
    {"userId": "2", "productId": "101", "rating": 3}
]
db.user_product_interactions.insert_many(interactions)

print("Data inserted successfully!")