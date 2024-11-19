// init.js

db = db.getSiblingDB('admin');  // Switch to admin database

db.createUser({
  user: "root",
  pwd: "rootpassword",  // Use a strong password in production
  roles: [
    { role: "root", db: "admin" }
  ]
});