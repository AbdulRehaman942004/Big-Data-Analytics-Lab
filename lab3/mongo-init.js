// MongoDB initialization script
db = db.getSiblingDB('crud_app');

// Create a user for the application
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'crud_app'
    }
  ]
});

// Create initial collection with some sample data
db.users.insertMany([
  {
    name: 'John Doe',
    email: 'john.doe@example.com',
    age: 30,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    age: 25,
    created_at: new Date(),
    updated_at: new Date()
  }
]);

print('Database initialized successfully!');

