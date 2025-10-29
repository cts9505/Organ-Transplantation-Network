-- UPDATE LOGIN TABLE TO LINK WITH USER TABLE
-- This adds User_ID column and links usernames to actual users

USE DBMS_PROJECT;

-- Step 1: Add User_ID column to login table
ALTER TABLE login ADD COLUMN User_ID INT;

-- Step 2: Add foreign key constraint
ALTER TABLE login ADD FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE;

-- Step 3: Update existing login records with proper User_IDs
UPDATE login SET User_ID = 101 WHERE username = 'alice';    -- Alice Johnson
UPDATE login SET User_ID = 102 WHERE username = 'bob';      -- Bob Martinez
UPDATE login SET User_ID = 103 WHERE username = 'charlie';  -- Carol Singh
UPDATE login SET User_ID = 104 WHERE username = 'diana';    -- David Lee

-- Step 4: Add more login accounts for other users
INSERT INTO login (username, password, User_ID) VALUES 
('emma', 'pass105', 105),      -- Emma Wilson
('frank', 'pass106', 106),     -- Frank Brown
('grace', 'pass107', 107),     -- Grace Davis
('henry', 'pass108', 108),     -- Henry Taylor
('iris', 'pass109', 109),      -- Iris Chen
('jack', 'pass110', 110);      -- Jack Miller

-- Verify the updates
SELECT l.username, l.User_ID, u.Name, u.City, u.State 
FROM login l 
LEFT JOIN User u ON l.User_ID = u.User_ID 
ORDER BY l.username;
