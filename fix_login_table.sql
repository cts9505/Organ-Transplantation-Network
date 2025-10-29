-- Migration script to add User_ID column to login table
-- Run this on your existing database

USE DBMS_PROJECT;

-- Add User_ID column to login table
ALTER TABLE login ADD COLUMN User_ID INT AFTER password;

-- Add foreign key constraint
ALTER TABLE login ADD FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE SET NULL;

-- Update existing user 'alice' to link with User_ID 101
UPDATE login SET User_ID = 101 WHERE username = 'alice';

-- Verify the changes
SELECT * FROM login;
