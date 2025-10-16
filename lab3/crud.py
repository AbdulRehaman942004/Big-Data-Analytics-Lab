from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# ------------------------------
# Loading environment variables
# ------------------------------
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DATABASE", "crud_app")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "users")

# Connecting to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("✅ Connected to MongoDB successfully!")


# ------------------------------
# CRUD FUNCTIONS
# ------------------------------
def create_user(name, email, age, phone=None, address=None):
    user = {
        "name": name,
        "email": email,
        "age": age,
        "phone": phone,
        "address": address,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    result = collection.insert_one(user)
    print(f"✅ User created with ID: {result.inserted_id}")
    return result.inserted_id


def get_all_users():
    users = list(collection.find())
    print("📋 All Users:")
    for user in users:
        print(user)
    return users


def get_user_by_email(email):
    user = collection.find_one({"email": email})
    if user:
        print("🔍 User found:", user)
    else:
        print("❌ No user found with that email.")
    return user


def update_user(email, updated_data):
    result = collection.update_one(
        {"email": email},
        {"$set": {**updated_data, "updated_at": datetime.now()}}
    )
    if result.modified_count:
        print("✅ User updated successfully.")
    else:
        print("⚠️ No user found or no changes made.")
    return result.modified_count


def delete_user(email):
    result = collection.delete_one({"email": email})
    if result.deleted_count:
        print("🗑️ User deleted successfully.")
    else:
        print("⚠️ No user found to delete.")
    return result.deleted_count


def delete_all_users():
    result = collection.delete_many({})
    print(f"⚠️ Deleted {result.deleted_count} users.")
    return result.deleted_count


def get_stats():
    count = collection.count_documents({})
    print(f"📊 Total users: {count}")
    return count


# ------------------------------
# INTERACTIVE MENU
# ------------------------------
if __name__ == "__main__":
    print("\n=== MongoDB CRUD Application ===")

    while True:
        print("\n----- MENU -----")
        print("1️⃣  Create a new user")
        print("2️⃣  Show all users")
        print("3️⃣  Find user by email")
        print("4️⃣  Update user details")
        print("5️⃣  Delete user by email")
        print("6️⃣  Delete ALL users (⚠️ irreversible)")
        print("7️⃣  Show total user count")
        print("0️⃣  Exit")
        print("----------------")

        choice = input("👉 Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            age = int(input("Enter age: "))
            phone = input("Enter phone (optional): ")
            address = input("Enter address (optional): ")
            create_user(name, email, age, phone, address)

        elif choice == "2":
            get_all_users()

        elif choice == "3":
            email = input("Enter email to search: ")
            get_user_by_email(email)

        elif choice == "4":
            email = input("Enter email of user to update: ")
            print("Leave field empty if you don’t want to change it.")
            name = input("New name: ")
            age = input("New age: ")
            phone = input("New phone: ")
            address = input("New address: ")

            updated_data = {}
            if name: updated_data["name"] = name
            if age: updated_data["age"] = int(age)
            if phone: updated_data["phone"] = phone
            if address: updated_data["address"] = address

            update_user(email, updated_data)

        elif choice == "5":
            email = input("Enter email to delete: ")
            delete_user(email)

        elif choice == "6":
            confirm = input("⚠️ Are you sure you want to delete ALL users? (yes/no): ")
            if confirm.lower() == "yes":
                delete_all_users()
            else:
                print("Operation cancelled.")

        elif choice == "7":
            get_stats()

        elif choice == "0":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")
