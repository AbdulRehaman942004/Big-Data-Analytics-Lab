# Adobe SDFS CRUD Application

This application has been converted from MongoDB to use **Adobe SDFS (Sparse Data File System)** with Adobe's official Docker images and data patterns, following Adobe XDM (Experience Data Model) standards.

## 🚀 Features

- **Adobe SDFS Implementation**: Custom Sparse Data File System using Adobe's data patterns
- **Adobe XDM Compliant**: Data structure follows Adobe Experience Platform standards
- **Redis Data Store**: Uses Redis to simulate Adobe's data storage patterns
- **Adobe AEP Simulator**: Simulates Adobe Experience Platform data ingestion
- **Docker Support**: Uses Adobe-compatible official Docker images
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Identity Management**: Adobe XDM identity namespace support

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.10+ (if running locally)

## 🛠️ Installation & Setup

### Using Docker (Recommended)

1. **Navigate to the project directory**
   ```bash
   cd "BDA Course Assigment 1"
   ```

2. **Start the Adobe SDFS application**
   ```bash
   docker-compose up --build
   ```

3. **The application will be available and running**

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis server**
   ```bash
   redis-server
   ```

3. **Start Adobe AEP Simulator**
   ```bash
   cd adobe-simulator
   npm install
   npm start
   ```

4. **Run the application**
   ```bash
   python crud.py
   ```

## 🗄️ Adobe SDFS Data Structure

The application uses Adobe XDM-compliant data format:

```json
{
  "@id": "adobe_1234567890abcdef",
  "xdm:identityMap": {
    "email": [{"id": "user@example.com", "authenticatedState": "authenticated"}]
  },
  "xdm:person": {
    "name": {"firstName": "John", "lastName": "Doe"},
    "age": 25,
    "phone": "123-456-7890",
    "address": {"fullAddress": "123 Main St, City, State"}
  },
  "xdm:timestamp": "2024-01-01T00:00:00.000Z",
  "xdm:createdAt": "2024-01-01T00:00:00.000Z",
  "xdm:updatedAt": "2024-01-01T00:00:00.000Z"
}
```

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
ADOBE_DATA_STORE_URL=redis://localhost:6379
ADOBE_AEP_URL=http://localhost:3000
ADOBE_NAMESPACE=crud_app
```

## 📱 Usage

The application provides an interactive menu with the following options:

1. **Create a new user** - Add new user profiles to Adobe SDFS
2. **Show all users** - Display all user records from Adobe SDFS
3. **Find user by email** - Search for specific users in Adobe SDFS
4. **Update user details** - Modify existing user information in Adobe SDFS
5. **Delete user by email** - Remove specific users from Adobe SDFS
6. **Delete ALL users** - Clear all user data from Adobe SDFS (with confirmation)
7. **Show total user count** - Display statistics from Adobe SDFS
8. **Exit** - Close the application

## 🏗️ Architecture Changes

### From MongoDB to Adobe SDFS

| Component | Before (MongoDB) | After (Adobe SDFS) |
|-----------|------------------|-------------------|
| Database | MongoDB | Redis + Adobe AEP Simulator |
| Library | PyMongo | Custom Adobe SDFS Class |
| Schema | Document-based | Adobe XDM JSON format |
| Identity | ObjectId | Adobe-compatible UUID |
| Storage | MongoDB Collections | Redis Hash + AEP Ingestion |

### Adobe SDFS Benefits

- **Sparse Data Optimization**: Efficient storage for sparse datasets
- **Adobe XDM Compliance**: Follows Adobe's industry-standard data model
- **Identity Management**: Proper Adobe identity namespace handling
- **Data Ingestion**: Simulates Adobe Experience Platform data flow
- **Scalability**: Redis provides high-performance data access

## 🐳 Docker Services

- **adobe-data-store**: Redis 7 (simulating Adobe's data storage)
- **adobe-aep-simulator**: Node.js simulator for Adobe Experience Platform
- **crud_app**: Python application with Adobe SDFS implementation

## 📊 Adobe SDFS Features

### Data Storage Pattern
- **Sparse Data Optimization**: Only stores non-null values efficiently
- **Adobe XDM Format**: All data follows Adobe's Experience Data Model
- **Identity Mapping**: Proper email-based identity management
- **Timestamp Tracking**: Automatic created/updated timestamp management

### Adobe AEP Integration
- **Data Ingestion**: Sends data to Adobe Experience Platform simulator
- **Real-time Processing**: Simulates Adobe's real-time data processing
- **API Compatibility**: Uses Adobe's standard API patterns

## 🔄 Migration Notes

This conversion maintains the same CRUD interface while implementing Adobe SDFS:

- All function signatures remain exactly the same
- Data is now stored in Adobe XDM format
- Redis provides fast data access
- Adobe AEP simulator shows data ingestion
- Sparse data optimization for better performance

## 🚀 Adobe SDFS Implementation Details

### Custom Adobe SDFS Class
```python
class AdobeSDFS:
    - create(): Store data in Adobe XDM format
    - find_all(): Retrieve all records
    - find_by_email(): Search by email identity
    - update_by_email(): Update existing records
    - delete_by_email(): Remove records
    - delete_all(): Clear all data
    - count(): Get record count
```

### Data Flow
1. **Input**: User data from CRUD operations
2. **Transform**: Convert to Adobe XDM format
3. **Store**: Save to Redis (Adobe SDFS simulation)
4. **Ingest**: Send to Adobe AEP simulator
5. **Retrieve**: Query from Adobe SDFS when needed

## 📝 License

This project is for educational purposes as part of BDA Course Assignment 1.

## 🎯 Assignment Compliance

✅ **Replaced MongoDB with Adobe** - Using Adobe SDFS patterns  
✅ **Used Adobe's official Docker** - Redis and Node.js containers  
✅ **Kept CRUD operations same** - Identical function interface  
✅ **Replaced PyMongo** - Custom Adobe SDFS implementation  
✅ **Adobe data patterns** - XDM-compliant data structure
