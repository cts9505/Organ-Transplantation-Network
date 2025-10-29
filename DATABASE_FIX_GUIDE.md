# 🔧 Database Schema Fix Guide

## Problem
```
mysql.connector.errors.ProgrammingError: 1054 (42S22): Unknown column 'User_ID' in 'field list'
```

This error occurs because the `login` table is missing the `User_ID` column, which is needed to link login credentials to user accounts.

---

## 🚀 Quick Fix (Existing Database)

Run this command to add the missing column:

```bash
mysql -u root -proot -D DBMS_PROJECT < fix_login_table.sql
```

Or manually execute:

```bash
mysql -u root -proot -D DBMS_PROJECT
```

```sql
ALTER TABLE login ADD COLUMN User_ID INT AFTER password;
ALTER TABLE login ADD FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE SET NULL;
UPDATE login SET User_ID = 101 WHERE username = 'alice';
```

---

## 🔄 Fresh Database Setup (Recommended)

If you want to start fresh with the corrected schema:

### Step 1: Backup existing data (if needed)
```bash
mysqldump -u root -proot DBMS_PROJECT > backup_$(date +%Y%m%d).sql
```

### Step 2: Drop and recreate database
```bash
mysql -u root -proot -e "DROP DATABASE IF EXISTS DBMS_PROJECT;"
mysql -u root -proot < create_tables_fixed.sql
```

### Step 3: Insert demo data
```bash
mysql -u root -proot DBMS_PROJECT < inserting_data/complete_demo_data.sql
```

---

## 📊 Updated Schema

### Before:
```sql
CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY(username)
);
```

### After:
```sql
CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    User_ID INT,
    PRIMARY KEY(username),
    FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE SET NULL
);
```

---

## ✅ Verify the Fix

After applying the migration, verify it worked:

```bash
mysql -u root -proot -D DBMS_PROJECT -e "DESCRIBE login;"
```

Expected output:
```
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| username | varchar(20) | NO   | PRI | NULL    |       |
| password | varchar(20) | NO   |     | NULL    |       |
| User_ID  | int         | YES  | MUL | NULL    |       |
+----------+-------------+------+-----+---------+-------+
```

Check data:
```bash
mysql -u root -proot -D DBMS_PROJECT -e "SELECT * FROM login;"
```

Expected output:
```
+----------+----------+---------+
| username | password | User_ID |
+----------+----------+---------+
| admin    | admin    | NULL    |
| alice    | pass123  | 101     |
+----------+----------+---------+
```

---

## 🔍 What This Fixes

1. **User Dashboard Access**: Links login credentials to user accounts
2. **Transaction History**: Enables proper user ID tracking
3. **Profile Management**: Allows users to view/edit their profile
4. **Role Detection**: Properly identifies if user is patient/donor
5. **Contact Information**: Shows correct contact details in transactions

---

## 📝 Files Updated

- ✅ `create_tables_fixed.sql` - Schema now creates User table before login table
- ✅ `fix_login_table.sql` - Migration script for existing databases

---

## 🎯 Next Steps

After fixing the database:

1. **Restart the Flask application**:
   ```bash
   python3 main.py
   ```

2. **Test login**:
   - Login as `alice` / `pass123`
   - Navigate to Transaction History
   - Should work without errors!

3. **Add new users**:
   When creating new users, make sure to insert into both `login` and `User` tables:
   
   ```sql
   INSERT INTO User VALUES (102, 'Bob Smith', '1985-05-15', 1, NULL, '456 Oak St', 'Boston', 'MA');
   INSERT INTO login VALUES ('bob', 'password123', 102);
   ```

---

## ⚠️ Important Notes

- The `admin` user has `User_ID = NULL` because it's a system admin, not linked to a patient/donor
- Regular users (patients/donors) MUST have a valid `User_ID` linking to the `User` table
- The FK uses `ON DELETE SET NULL` to prevent login deletion when a user is deleted

---

**Ready to fix?** Run: `mysql -u root -proot -D DBMS_PROJECT < fix_login_table.sql`
