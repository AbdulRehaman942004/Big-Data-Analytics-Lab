import redis
import json
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

# ------------------------------
# Loading environment variables
# ------------------------------
load_dotenv()

# Adobe SDFS Configuration (simulating Adobe's data storage patterns)
ADOBE_DATA_STORE_URL = os.getenv("ADOBE_DATA_STORE_URL", "redis://localhost:6379")
ADOBE_AEP_URL = os.getenv("ADOBE_AEP_URL", "http://localhost:3000")
ADOBE_NAMESPACE = os.getenv("ADOBE_NAMESPACE", "crud_app")

# Adobe SDFS Data Store (using Redis to simulate Adobe's data patterns)
adobe_store = redis.from_url(ADOBE_DATA_STORE_URL, decode_responses=True)

# Adobe Experience Platform Simulator
class AdobeSDFS:
    def __init__(self, store, aep_url, namespace):
        self.store = store
        self.aep_url = aep_url
        self.namespace = namespace
        self.collection_key = f"adobe:{namespace}:users"
    
    def _generate_adobe_id(self):
        """Generate Adobe-compatible ID"""
        return f"adobe_{uuid.uuid4().hex[:16]}"
    
    def _create_adobe_xdm_record(self, data):
        """Create Adobe XDM-compliant record"""
        return {
            "@id": self._generate_adobe_id(),
            "xdm:identityMap": {
                "email": [{"id": data["email"], "authenticatedState": "authenticated"}]
            },
            "xdm:person": {
                "name": {"firstName": data["name"].split()[0] if data["name"] else "", 
                        "lastName": data["name"].split()[-1] if len(data["name"].split()) > 1 else ""},
                "age": data["age"],
                "phone": data.get("phone", ""),
                "address": {"fullAddress": data.get("address", "")}
            },
            "xdm:timestamp": datetime.utcnow().isoformat() + "Z",
            "xdm:createdAt": datetime.utcnow().isoformat() + "Z",
            "xdm:updatedAt": datetime.utcnow().isoformat() + "Z"
        }
    
    def create(self, data):
        """Create record in Adobe SDFS"""
        adobe_record = self._create_adobe_xdm_record(data)
        record_id = adobe_record["@id"]
        
        # Store in Adobe SDFS (Redis simulation)
        self.store.hset(self.collection_key, record_id, json.dumps(adobe_record))
        
        # Send to Adobe Experience Platform simulator
        try:
            requests.post(f"{self.aep_url}/api/ingest", 
                         json=adobe_record, 
                         headers={"Content-Type": "application/json"})
        except:
            pass  # Simulator might not be running
        
        return record_id
    
    def find_all(self):
        """Find all records in Adobe SDFS"""
        records = self.store.hgetall(self.collection_key)
        return [json.loads(record) for record in records.values()]
    
    def find_by_email(self, email):
        """Find record by email in Adobe SDFS"""
        records = self.find_all()
        for record in records:
            if record.get("xdm:identityMap", {}).get("email", [{}])[0].get("id") == email:
                return record
        return None
    
    def update_by_email(self, email, update_data):
        """Update record by email in Adobe SDFS"""
        records = self.find_all()
        for record in records:
            if record.get("xdm:identityMap", {}).get("email", [{}])[0].get("id") == email:
                # Update the record
                if "name" in update_data:
                    name_parts = update_data["name"].split()
                    record["xdm:person"]["name"]["firstName"] = name_parts[0] if name_parts else ""
                    record["xdm:person"]["name"]["lastName"] = name_parts[-1] if len(name_parts) > 1 else ""
                if "age" in update_data:
                    record["xdm:person"]["age"] = update_data["age"]
                if "phone" in update_data:
                    record["xdm:person"]["phone"] = update_data["phone"]
                if "address" in update_data:
                    record["xdm:person"]["address"]["fullAddress"] = update_data["address"]
                
                record["xdm:updatedAt"] = datetime.utcnow().isoformat() + "Z"
                
                # Save back to Adobe SDFS
                self.store.hset(self.collection_key, record["@id"], json.dumps(record))
                return 1
        return 0
    
    def delete_by_email(self, email):
        """Delete record by email from Adobe SDFS"""
        records = self.find_all()
        for record in records:
            if record.get("xdm:identityMap", {}).get("email", [{}])[0].get("id") == email:
                self.store.hdel(self.collection_key, record["@id"])
                return 1
        return 0
    
    def delete_all(self):
        """Delete all records from Adobe SDFS"""
        count = self.store.hlen(self.collection_key)
        self.store.delete(self.collection_key)
        return count
    
    def count(self):
        """Count records in Adobe SDFS"""
        return self.store.hlen(self.collection_key)

# Initialize Adobe SDFS
adobe_sdfs = AdobeSDFS(adobe_store, ADOBE_AEP_URL, ADOBE_NAMESPACE)

print("[SUCCESS] Connected to Adobe SDFS successfully!")


# ------------------------------
# CRUD FUNCTIONS
# ------------------------------
def create_user(name, email, age, phone=None, address=None):
    try:
        # Check if user already exists in Adobe SDFS
        existing_user = adobe_sdfs.find_by_email(email)
        if existing_user:
            print("[WARNING] User with this email already exists.")
            return None
            
        # Create new user data
        user_data = {
            "name": name,
            "email": email,
            "age": age,
            "phone": phone or "",
            "address": address or ""
        }
        
        # Store in Adobe SDFS
        record_id = adobe_sdfs.create(user_data)
        print(f"[SUCCESS] User created with Adobe ID: {record_id}")
        return record_id
    except Exception as e:
        print(f"[ERROR] Error creating user: {str(e)}")
        return None


def get_all_users():
    try:
        users = adobe_sdfs.find_all()
        print("[INFO] All Users in Adobe SDFS:")
        for user in users:
            # Extract readable data from Adobe XDM format
            email = user.get("xdm:identityMap", {}).get("email", [{}])[0].get("id", "")
            person = user.get("xdm:person", {})
            name_obj = person.get("name", {})
            name = f"{name_obj.get('firstName', '')} {name_obj.get('lastName', '')}".strip()
            
            user_dict = {
                "adobe_id": user.get("@id", ""),
                "email": email,
                "name": name,
                "age": person.get("age", ""),
                "phone": person.get("phone", ""),
                "address": person.get("address", {}).get("fullAddress", ""),
                "created_at": user.get("xdm:createdAt", ""),
                "updated_at": user.get("xdm:updatedAt", "")
            }
            print(user_dict)
        return users
    except Exception as e:
        print(f"[ERROR] Error fetching users: {str(e)}")
        return []


def get_user_by_email(email):
    try:
        user = adobe_sdfs.find_by_email(email)
        if user:
            # Extract readable data from Adobe XDM format
            person = user.get("xdm:person", {})
            name_obj = person.get("name", {})
            name = f"{name_obj.get('firstName', '')} {name_obj.get('lastName', '')}".strip()
            
            user_dict = {
                "adobe_id": user.get("@id", ""),
                "email": email,
                "name": name,
                "age": person.get("age", ""),
                "phone": person.get("phone", ""),
                "address": person.get("address", {}).get("fullAddress", ""),
                "created_at": user.get("xdm:createdAt", ""),
                "updated_at": user.get("xdm:updatedAt", "")
            }
            print("[SEARCH] User found in Adobe SDFS:", user_dict)
        else:
            print("[ERROR] No user found with that email.")
        return user
    except Exception as e:
        print(f"[ERROR] Error fetching user: {str(e)}")
        return None


def update_user(email, updated_data):
    try:
        result = adobe_sdfs.update_by_email(email, updated_data)
        if result:
            print("[SUCCESS] User updated successfully in Adobe SDFS.")
        else:
            print("[ERROR] No user found with that email.")
        return result
    except Exception as e:
        print(f"[ERROR] Error updating user: {str(e)}")
        return 0


def delete_user(email):
    try:
        result = adobe_sdfs.delete_by_email(email)
        if result:
            print("[DELETE] User deleted successfully from Adobe SDFS.")
        else:
            print("[WARNING] No user found to delete.")
        return result
    except Exception as e:
        print(f"[ERROR] Error deleting user: {str(e)}")
        return 0


def delete_all_users():
    try:
        count = adobe_sdfs.delete_all()
        print(f"[WARNING] Deleted {count} users from Adobe SDFS.")
        return count
    except Exception as e:
        print(f"[ERROR] Error deleting all users: {str(e)}")
        return 0


def get_stats():
    try:
        count = adobe_sdfs.count()
        print(f"[STATS] Total users in Adobe SDFS: {count}")
        return count
    except Exception as e:
        print(f"[ERROR] Error getting stats: {str(e)}")
        return 0


# ------------------------------
# INTERACTIVE MENU
# ------------------------------
if __name__ == "__main__":
    print("\n=== Adobe SDFS CRUD Application ===")

    try:
        while True:
            print("\n----- MENU -----")
            print("1.  Create a new user")
            print("2.  Show all users")
            print("3.  Find user by email")
            print("4.  Update user details")
            print("5.  Delete user by email")
            print("6.  Delete ALL users ([WARNING] irreversible)")
            print("7.  Show total user count")
            print("0.  Exit")
            print("----------------")

            choice = input("-> Enter your choice: ")

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
                print("Leave field empty if you don't want to change it.")
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
                confirm = input("[WARNING] Are you sure you want to delete ALL users? (yes/no): ")
                if confirm.lower() == "yes":
                    delete_all_users()
                else:
                    print("Operation cancelled.")

            elif choice == "7":
                get_stats()

            elif choice == "0":
                print("[GOODBYE] Exiting... Goodbye!")
                break

            else:
                print("[ERROR] Invalid choice. Try again.")
    
    except KeyboardInterrupt:
        print("\n[GOODBYE] Exiting... Goodbye!")
    except Exception as e:
        print(f"[ERROR] Application error: {str(e)}")
