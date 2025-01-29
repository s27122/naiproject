from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:admin@cluster0.yewm5.mongodb.net/')
db = client['naiproject']
# Fetch users
users = list(db.users.find())
print("Users:", users)

# Fetch products
products = list(db.products.find())
print("Products:", products)

# Fetch interactions
interactions = list(db.user_product_interactions.find())
print("Interactions:", interactions)