import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import uuid

class AdobeSDFS:
    """Adobe SDFS - Simple Distributed File System for CRUD operations"""
    
    def __init__(self, storage_path: str = "./adobe_sdfs_storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.files = {}  # file_id -> file_info
        
    def _generate_adobe_id(self):
        """Generate Adobe-compatible file ID"""
        return f"adobe_{uuid.uuid4().hex[:16]}"
    
    def create(self, file_path: str, metadata: dict = None) -> str:
        """CREATE: Upload file"""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                raise FileNotFoundError(f"File {file_path} not found")
            
            # Generate Adobe file ID
            file_id = self._generate_adobe_id()
            
            # Create destination path
            dest_path = self.storage_path / f"{file_id}_{source_path.name}"
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            
            # Store file info
            self.files[file_id] = {
                "file_id": file_id,
                "original_name": source_path.name,
                "stored_path": str(dest_path),
                "size_bytes": source_path.stat().st_size,
                "uploaded_at": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            }
            
            return file_id
            
        except Exception as e:
            print(f"[ERROR] Failed to create file: {e}")
            return None
    
    def read_all(self) -> list:
        """READ: Get all files"""
        return list(self.files.values())
    
    def read_by_id(self, file_id: str) -> dict:
        """READ: Get specific file by ID"""
        return self.files.get(file_id)
    
    def download(self, file_id: str, dest_path: str) -> bool:
        """READ: Download file"""
        try:
            if file_id not in self.files:
                return False
            
            file_info = self.files[file_id]
            source_path = Path(file_info["stored_path"])
            dest_path = Path(dest_path)
            
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to download file: {e}")
            return False
    
    def update_metadata(self, file_id: str, new_metadata: dict) -> bool:
        """UPDATE: Update file metadata"""
        try:
            if file_id not in self.files:
                return False
            
            # Update metadata
            current_metadata = self.files[file_id].get("metadata", {})
            self.files[file_id]["metadata"] = {**current_metadata, **new_metadata}
            self.files[file_id]["updated_at"] = datetime.utcnow().isoformat()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to update metadata: {e}")
            return False
    
    def delete(self, file_id: str) -> bool:
        """DELETE: Remove file"""
        try:
            if file_id not in self.files:
                return False
            
            file_info = self.files[file_id]
            file_path = Path(file_info["stored_path"])
            
            # Delete file
            if file_path.exists():
                file_path.unlink()
            
            # Remove from tracking
            del self.files[file_id]
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to delete file: {e}")
            return False
    
    def delete_all(self) -> int:
        """DELETE: Remove all files"""
        count = len(self.files)
        for file_id in list(self.files.keys()):
            self.delete(file_id)
        return count
    
    def count(self) -> int:
        """Count files"""
        return len(self.files)

# Initialize Adobe SDFS
adobe_sdfs = AdobeSDFS()

print("[SUCCESS] Adobe SDFS initialized successfully!")

# ------------------------------
# CRUD FUNCTIONS
# ------------------------------

def create_file(file_path, file_name=None, description=None):
    """CREATE: Upload a file to Adobe SDFS"""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            print("[ERROR] File not found.")
            return None
        
        # Prepare file metadata
        file_metadata = {
            "file_name": file_name or file_path.stem,
            "description": description or ""
        }
        
        # Upload to Adobe SDFS
        file_id = adobe_sdfs.create(str(file_path), file_metadata)
        
        if file_id:
            print(f"[SUCCESS] File created with Adobe ID: {file_id}")
            print(f"[INFO] File: {file_metadata['file_name']}")
            return file_id
        else:
            print("[ERROR] Failed to create file in Adobe SDFS.")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error creating file: {str(e)}")
        return None


def get_all_files():
    """READ: Get all files from Adobe SDFS"""
    try:
        files = adobe_sdfs.read_all()
        print("[INFO] All Files in Adobe SDFS:")
        print("-" * 50)
        
        if not files:
            print("[INFO] No files found in Adobe SDFS.")
            return []
        
        for file_info in files:
            metadata = file_info.get("metadata", {})
            print(f"Adobe ID: {file_info['file_id']}")
            print(f"Name: {metadata.get('file_name', 'Unknown')}")
            print(f"Size: {file_info['size_bytes']:,} bytes")
            print(f"Uploaded: {file_info['uploaded_at']}")
            print(f"Description: {metadata.get('description', 'No description')}")
            print("-" * 50)
        
        return files
    except Exception as e:
        print(f"[ERROR] Error fetching files: {str(e)}")
        return []


def get_file_by_id(file_id):
    """READ: Get specific file by Adobe ID"""
    try:
        file_info = adobe_sdfs.read_by_id(file_id)
        if file_info:
            metadata = file_info.get("metadata", {})
            print("[SEARCH] File found in Adobe SDFS:")
            print("-" * 40)
            print(f"Adobe ID: {file_info['file_id']}")
            print(f"Name: {metadata.get('file_name', 'Unknown')}")
            print(f"Size: {file_info['size_bytes']:,} bytes")
            print(f"Uploaded: {file_info['uploaded_at']}")
            print(f"Description: {metadata.get('description', 'No description')}")
            print("-" * 40)
        else:
            print("[ERROR] No file found with that Adobe ID.")
        return file_info
    except Exception as e:
        print(f"[ERROR] Error fetching file: {str(e)}")
        return None


def download_file(file_id, download_path=None):
    """READ: Download file from Adobe SDFS"""
    try:
        file_info = adobe_sdfs.read_by_id(file_id)
        if not file_info:
            print("[ERROR] File not found.")
            return False
        
        metadata = file_info.get("metadata", {})
        original_name = file_info.get("original_name", "unknown_file")
        
        if not download_path:
            download_path = f"./downloads/{original_name}"
        
        # Download from Adobe SDFS
        success = adobe_sdfs.download(file_id, download_path)
        
        if success:
            print(f"[SUCCESS] File downloaded successfully!")
            print(f"[INFO] Saved to: {download_path}")
            print(f"[INFO] File: {metadata.get('file_name', 'Unknown')}")
        else:
            print("[ERROR] Failed to download file.")
        
        return success
    except Exception as e:
        print(f"[ERROR] Error downloading file: {str(e)}")
        return False


def update_file_metadata(file_id, new_metadata):
    """UPDATE: Update file metadata"""
    try:
        success = adobe_sdfs.update_metadata(file_id, new_metadata)
        if success:
            print("[SUCCESS] File metadata updated successfully.")
            print(f"[INFO] Updated fields: {', '.join(new_metadata.keys())}")
        else:
            print("[ERROR] File not found.")
        return success
    except Exception as e:
        print(f"[ERROR] Error updating file metadata: {str(e)}")
        return False


def delete_file(file_id):
    """DELETE: Remove file from Adobe SDFS"""
    try:
        file_info = adobe_sdfs.read_by_id(file_id)
        if not file_info:
            print("[ERROR] File not found.")
            return False
        
        metadata = file_info.get("metadata", {})
        file_name = metadata.get("file_name", "Unknown")
        
        # Delete from Adobe SDFS
        success = adobe_sdfs.delete(file_id)
        
        if success:
            print(f"[DELETE] File '{file_name}' deleted successfully.")
        else:
            print("[ERROR] Failed to delete file.")
        
        return success
    except Exception as e:
        print(f"[ERROR] Error deleting file: {str(e)}")
        return False


def delete_all_files():
    """DELETE: Remove all files from Adobe SDFS"""
    try:
        count = adobe_sdfs.delete_all()
        print(f"[WARNING] Deleted {count} files.")
        return count
    except Exception as e:
        print(f"[ERROR] Error deleting all files: {str(e)}")
        return 0


def get_stats():
    """Get Adobe SDFS statistics"""
    try:
        count = adobe_sdfs.count()
        print(f"[STATS] Total files: {count}")
        return count
    except Exception as e:
        print(f"[ERROR] Error getting stats: {str(e)}")
        return 0


# ------------------------------
# INTERACTIVE MENU
# ------------------------------
if __name__ == "__main__":
    print("\n=== Adobe SDFS File Management ===")

    try:
        while True:
            print("\n----- MENU -----")
            print("1.  Upload file (CREATE)")
            print("2.  List all files (READ)")
            print("3.  Find file by Adobe ID (READ)")
            print("4.  Download file (READ)")
            print("5.  Update file metadata (UPDATE)")
            print("6.  Delete file by Adobe ID (DELETE)")
            print("7.  Delete ALL files ([WARNING] irreversible)")
            print("8.  Show total file count")
            print("0.  Exit")
            print("----------------")

            choice = input("-> Enter your choice: ")

            if choice == "1":
                file_path = input("Enter file path to upload: ")
                file_name = input("Enter file name (optional): ")
                description = input("Enter description (optional): ")
                create_file(file_path, file_name, description)

            elif choice == "2":
                get_all_files()

            elif choice == "3":
                file_id = input("Enter Adobe ID to search: ")
                get_file_by_id(file_id)

            elif choice == "4":
                file_id = input("Enter Adobe ID to download: ")
                download_path = input("Enter download path (optional): ")
                download_file(file_id, download_path if download_path else None)

            elif choice == "5":
                file_id = input("Enter Adobe ID to update: ")
                print("Enter new metadata (leave empty to skip):")
                new_name = input("New file name: ")
                new_description = input("New description: ")
                
                update_data = {}
                if new_name: update_data["file_name"] = new_name
                if new_description: update_data["description"] = new_description
                
                if update_data:
                    update_file_metadata(file_id, update_data)
                else:
                    print("[INFO] No updates provided.")

            elif choice == "6":
                file_id = input("Enter Adobe ID to delete: ")
                delete_file(file_id)

            elif choice == "7":
                confirm = input("[WARNING] Are you sure you want to delete ALL files? (yes/no): ")
                if confirm.lower() == "yes":
                    delete_all_files()
                else:
                    print("Operation cancelled.")

            elif choice == "8":
                get_stats()

            elif choice == "0":
                print("[GOODBYE] Exiting Adobe SDFS... Goodbye!")
                break

            else:
                print("[ERROR] Invalid choice. Try again.")
    
    except KeyboardInterrupt:
        print("\n[GOODBYE] Exiting Adobe SDFS... Goodbye!")
    except Exception as e:
        print(f"[ERROR] Application error: {str(e)}")
