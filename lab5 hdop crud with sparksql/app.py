import time
import os
from hdfs import InsecureClient
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

HDFS_URL = "http://namenode:9870"
HDFS_USER = "root"
HDFS_DIR = "/user/root"
LOCAL_FILE = "example.txt"
SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")

print("Waiting for HDFS and Spark to be ready...")
time.sleep(30)

# ============================================
# HDFS CRUD Operations
# ============================================
print("\n" + "="*60)
print("HDFS CRUD OPERATIONS")
print("="*60)

try:
    client = InsecureClient(HDFS_URL, user=HDFS_USER)
    print(f"Connected to HDFS at {HDFS_URL} as user '{HDFS_USER}'")

    # Ensure directory exists
    client.makedirs(HDFS_DIR)
    print(f"Directory {HDFS_DIR} created or already exists.")

    # --------------------------
    # CREATE
    # --------------------------
    with open(LOCAL_FILE, "w") as f:
        f.write("Hello from Dockerized Python and HDFS!\n")
    print("Local file created successfully.")

    client.upload(HDFS_DIR, LOCAL_FILE, overwrite=True)
    print(f"Uploaded '{LOCAL_FILE}' to HDFS at {HDFS_DIR}")

    # --------------------------
    # READ
    # --------------------------
    hdfs_file_path = f"{HDFS_DIR}/{LOCAL_FILE}"
    with client.read(hdfs_file_path, encoding="utf-8") as reader:
        contents = reader.read()
        print(f"Read from HDFS:\n{contents}")

    # --------------------------
    # UPDATE
    # --------------------------
    updated_content = contents + "This line was appended from Python update operation.\n"
    with open(LOCAL_FILE, "w") as f:
        f.write(updated_content)
    client.upload(HDFS_DIR, LOCAL_FILE, overwrite=True)
    print("File updated successfully in HDFS.")

    # Verify update
    with client.read(hdfs_file_path, encoding="utf-8") as reader:
        new_data = reader.read()
        print(f"Updated HDFS file content:\n{new_data}")

    # --------------------------
    # DELETE
    # --------------------------
    client.delete(hdfs_file_path)
    print(f"File '{hdfs_file_path}' deleted successfully from HDFS.")

except Exception as e:
    print(f"Error during HDFS CRUD operations: {e}")

# ============================================
# Spark SQL Operations
# ============================================
print("\n" + "="*60)
print("SPARK SQL OPERATIONS")
print("="*60)

try:
    # Initialize Spark Session
    print(f"Initializing Spark Session (Master: {SPARK_MASTER})...")
    spark = SparkSession.builder \
        .appName("SparkSQLIntegration") \
        .master(SPARK_MASTER) \
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
        .getOrCreate()
    
    print("Spark Session created successfully!")
    print(f"Spark Version: {spark.version}")

    # ============================================
    # Create Dummy Data - Employees Table
    # ============================================
    print("\nCreating dummy data for Employees table...")
    
    employees_data = [
        (1, "John Doe", "Engineering", 75000.0, 28),
        (2, "Jane Smith", "Marketing", 65000.0, 25),
        (3, "Bob Johnson", "Engineering", 80000.0, 32),
        (4, "Alice Williams", "Sales", 60000.0, 27),
        (5, "Charlie Brown", "Engineering", 90000.0, 35),
        (6, "Diana Prince", "HR", 70000.0, 30),
        (7, "Eve Davis", "Marketing", 68000.0, 26),
        (8, "Frank Miller", "Sales", 72000.0, 29),
        (9, "Grace Lee", "Engineering", 85000.0, 33),
        (10, "Henry Wilson", "Finance", 75000.0, 31)
    ]
    
    # Define schema
    employees_schema = StructType([
        StructField("employee_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("department", StringType(), True),
        StructField("salary", DoubleType(), True),
        StructField("age", IntegerType(), True)
    ])
    
    # Create DataFrame
    employees_df = spark.createDataFrame(employees_data, schema=employees_schema)
    
    # Create temporary view for SQL queries
    employees_df.createOrReplaceTempView("employees")
    print("Employees table created with 10 records")

    # ============================================
    # Create Dummy Data - Products Table
    # ============================================
    print("\nCreating dummy data for Products table...")
    
    products_data = [
        (101, "Laptop", "Electronics", 999.99, 50),
        (102, "Mouse", "Electronics", 29.99, 200),
        (103, "Keyboard", "Electronics", 79.99, 150),
        (104, "Monitor", "Electronics", 299.99, 75),
        (105, "Desk Chair", "Furniture", 199.99, 30),
        (106, "Office Desk", "Furniture", 449.99, 20),
        (107, "Notebook", "Stationery", 5.99, 500),
        (108, "Pen Set", "Stationery", 12.99, 300),
        (109, "Headphones", "Electronics", 149.99, 100),
        (110, "Webcam", "Electronics", 89.99, 80)
    ]
    
    products_schema = StructType([
        StructField("product_id", IntegerType(), True),
        StructField("product_name", StringType(), True),
        StructField("category", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("stock_quantity", IntegerType(), True)
    ])
    
    products_df = spark.createDataFrame(products_data, schema=products_schema)
    products_df.createOrReplaceTempView("products")
    print("Products table created with 10 records")

    # ============================================
    # Query 1: Display All Employees
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 1: Display All Employees")
    print("-"*60)
    query1 = spark.sql("SELECT * FROM employees ORDER BY employee_id")
    query1.show(truncate=False)

    # ============================================
    # Query 2: Display All Products
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 2: Display All Products")
    print("-"*60)
    query2 = spark.sql("SELECT * FROM products ORDER BY product_id")
    query2.show(truncate=False)

    # ============================================
    # Query 3: Employees by Department
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 3: Employees Grouped by Department")
    print("-"*60)
    query3 = spark.sql("""
        SELECT 
            department,
            COUNT(*) as employee_count,
            AVG(salary) as avg_salary,
            MAX(salary) as max_salary,
            MIN(salary) as min_salary
        FROM employees
        GROUP BY department
        ORDER BY employee_count DESC
    """)
    query3.show(truncate=False)

    # ============================================
    # Query 4: High Salary Employees
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 4: Employees with Salary > 75000")
    print("-"*60)
    query4 = spark.sql("""
        SELECT 
            employee_id,
            name,
            department,
            salary,
            age
        FROM employees
        WHERE salary > 75000
        ORDER BY salary DESC
    """)
    query4.show(truncate=False)

    # ============================================
    # Query 5: Products by Category
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 5: Products Grouped by Category")
    print("-"*60)
    query5 = spark.sql("""
        SELECT 
            category,
            COUNT(*) as product_count,
            AVG(price) as avg_price,
            SUM(stock_quantity) as total_stock
        FROM products
        GROUP BY category
        ORDER BY product_count DESC
    """)
    query5.show(truncate=False)

    # ============================================
    # Query 6: Top 5 Highest Paid Employees
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 6: Top 5 Highest Paid Employees")
    print("-"*60)
    query6 = spark.sql("""
        SELECT 
            name,
            department,
            salary,
            age
        FROM employees
        ORDER BY salary DESC
        LIMIT 5
    """)
    query6.show(truncate=False)

    # ============================================
    # Query 7: Products with Low Stock
    # ============================================
    print("\n" + "-"*60)
    print("QUERY 7: Products with Stock < 100")
    print("-"*60)
    query7 = spark.sql("""
        SELECT 
            product_id,
            product_name,
            category,
            price,
            stock_quantity
        FROM products
        WHERE stock_quantity < 100
        ORDER BY stock_quantity ASC
    """)
    query7.show(truncate=False)

    # ============================================
    # Display DataFrame Info
    # ============================================
    print("\n" + "-"*60)
    print("DATAFRAME INFORMATION")
    print("-"*60)
    print("\nEmployees DataFrame Schema:")
    employees_df.printSchema()
    print(f"\nEmployees DataFrame Count: {employees_df.count()}")
    
    print("\nProducts DataFrame Schema:")
    products_df.printSchema()
    print(f"\nProducts DataFrame Count: {products_df.count()}")

    print("\nAll Spark SQL operations completed successfully!")

except Exception as e:
    print(f"Error during Spark SQL operations: {e}")
    import traceback
    traceback.print_exc()

# Keep container alive for logs/debug
print("\n" + "="*60)
print("All operations complete. Keeping container alive...")
print("="*60)
while True:
    time.sleep(60)
