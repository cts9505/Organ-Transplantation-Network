# 🔗 Login → User Table Linking Guide

## 📋 Overview
This document explains how the login system connects to user profile data.

---

## 🗂️ Database Structure

### **BEFORE Fix:**
```
login table:          User table:
┌──────────┬──────────┐    ┌─────────┬──────────────┬─────────┐
│ username │ password │    │ User_ID │ Name         │ City    │
├──────────┼──────────┤    ├─────────┼──────────────┼─────────┤
│ alice    │ pass123  │    │ 101     │ Alice Johnson│ Boston  │
│ bob      │ pass456  │    │ 102     │ Bob Martinez │ New York│
└──────────┴──────────┘    └─────────┴──────────────┴─────────┘
        ❌ NO CONNECTION!
```

### **AFTER Fix:**
```
login table:                          User table:
┌──────────┬──────────┬─────────┐    ┌─────────┬──────────────┬─────────┐
│ username │ password │ User_ID │───▶│ User_ID │ Name         │ City    │
├──────────┼──────────┼─────────┤    ├─────────┼──────────────┼─────────┤
│ alice    │ pass123  │ 101     │───▶│ 101     │ Alice Johnson│ Boston  │
│ bob      │ pass456  │ 102     │───▶│ 102     │ Bob Martinez │ New York│
│ charlie  │ pass789  │ 103     │───▶│ 103     │ Carol Singh  │ Seattle │
│ diana    │ pass000  │ 104     │───▶│ 104     │ David Lee    │ Chicago │
└──────────┴──────────┴─────────┘    └─────────┴──────────────┴─────────┘
        ✅ LINKED VIA User_ID!
```

---

## 🔧 How to Apply the Fix

### **Step 1: Run the Update SQL**
```bash
mysql -u root -p DBMS_PROJECT < inserting_data/update_login_table.sql
```

This will:
- ✅ Add `User_ID` column to login table
- ✅ Create foreign key relationship
- ✅ Link existing usernames to users
- ✅ Add login accounts for all 10 users

### **Step 2: Verify the Changes**
```sql
-- Check login → user mapping
SELECT l.username, l.User_ID, u.Name, u.City, u.State 
FROM login l 
LEFT JOIN User u ON l.User_ID = u.User_ID 
ORDER BY l.username;
```

**Expected Output:**
```
+----------+---------+----------------+----------+-------+
| username | User_ID | Name           | City     | State |
+----------+---------+----------------+----------+-------+
| admin    | NULL    | NULL           | NULL     | NULL  |
| alice    | 101     | Alice Johnson  | Boston   | MA    |
| bob      | 102     | Bob Martinez   | New York | NY    |
| charlie  | 103     | Carol Singh    | Seattle  | WA    |
| diana    | 104     | David Lee      | Chicago  | IL    |
| emma     | 105     | Emma Wilson    | Austin   | TX    |
| frank    | 106     | Frank Brown    | Miami    | FL    |
| grace    | 107     | Grace Davis    | Denver   | CO    |
| henry    | 108     | Henry Taylor   | Phoenix  | AZ    |
| iris     | 109     | Iris Chen      | Portland | OR    |
| jack     | 110     | Jack Miller    | Atlanta  | GA    |
+----------+---------+----------------+----------+-------+
```

---

## 📱 What Profile Details Are Fetched?

When a user logs in (e.g., `alice`), the system now fetches:

### **1. Basic User Information** (from User table):
```python
user_data = (
    101,                    # User_ID
    'Alice Johnson',        # Name
    '1985-06-15',          # Date_of_Birth
    1,                     # Medical_insurance (1 = yes, 0 = no)
    'None',                # Medical_history
    '123 Main St',         # Street
    'Boston',              # City
    'MA'                   # State
)
```

### **2. Phone Numbers** (from User_phone_no table):
```python
phone_numbers = [
    ('617-555-0101',),
    ('617-555-0102',)
]
```

### **3. Patient Records** (if user is a patient):
```python
# Fetched from Patient table WHERE User_ID = 101
patient_data = (
    Patient_ID,
    organ_req,              # e.g., 'Kidney', 'Heart'
    reason_of_procurement,  # e.g., 'Chronic kidney disease'
    Doctor_ID
)
```

### **4. Donor Records** (if user is a donor):
```python
# Fetched from Donor table WHERE User_ID = 101
donor_data = (
    Donor_ID,
    organ_donated,          # e.g., 'Kidney', 'Liver'
    reason_of_donation,     # e.g., 'Living donation'
    Organization_ID
)
```

### **5. Transaction History**:
```python
# Fetched from Transaction table for this user
transactions = [
    (Patient_ID, Organ_ID, Donor_ID, Date_of_transaction, Status)
]
```

---

## 🔄 How the Login Flow Works

```
1. User enters credentials
   ┌─────────────────────────┐
   │ Username: alice         │
   │ Password: pass123       │
   └─────────────────────────┘
              ↓
2. Verify credentials in login table
   SELECT * FROM login WHERE username='alice'
              ↓
3. Get User_ID from login table
   SELECT User_ID FROM login WHERE username='alice'
   Result: User_ID = 101
              ↓
4. Fetch user profile data
   SELECT * FROM User WHERE User_ID = 101
              ↓
5. Display personalized dashboard
   ┌──────────────────────────────────┐
   │ Welcome, Alice Johnson!          │
   │ 📍 Boston, MA                    │
   │ 🏥 Medical Insurance: Yes        │
   │ 📞 617-555-0101, 617-555-0102   │
   └──────────────────────────────────┘
```

---

## 🎯 Updated Routes

### **User Dashboard Route** (`/user/dashboard`)
```python
# Gets User_ID from login → shows user's specific stats:
- Your Organ Requests (Patient records for this User_ID)
- Your Donations (Donor records for this User_ID)
- Your Transactions (Transactions involving this User_ID)
- Organs Available (All available organs - global)
```

### **User Profile Route** (`/user/profile`)
```python
# Gets User_ID from login → shows user's profile:
- Name, DOB, Address (from User table)
- Phone numbers (from User_phone_no table)
- Medical insurance status
- Medical history
```

---

## 👥 Complete Login Credentials

| Username | Password | User_ID | Name           | City     | Medical Info        |
|----------|----------|---------|----------------|----------|---------------------|
| admin    | admin    | NULL    | Admin User     | -        | System Admin        |
| alice    | pass123  | 101     | Alice Johnson  | Boston   | No history          |
| bob      | pass456  | 102     | Bob Martinez   | New York | Diabetes            |
| charlie  | pass789  | 103     | Carol Singh    | Seattle  | Hypertension        |
| diana    | pass000  | 104     | David Lee      | Chicago  | Asthma              |
| emma     | pass105  | 105     | Emma Wilson    | Austin   | No history          |
| frank    | pass106  | 106     | Frank Brown    | Miami    | Heart Disease       |
| grace    | pass107  | 107     | Grace Davis    | Denver   | No history          |
| henry    | pass108  | 108     | Henry Taylor   | Phoenix  | Kidney Disease      |
| iris     | pass109  | 109     | Iris Chen      | Portland | No history          |
| jack     | pass110  | 110     | Jack Miller    | Atlanta  | Liver Disease       |

---

## ✅ Testing Steps

1. **Run the update script:**
   ```bash
   mysql -u root -p DBMS_PROJECT < inserting_data/update_login_table.sql
   ```

2. **Start Flask app:**
   ```bash
   python3 main.py
   ```

3. **Login as alice:**
   - Go to: http://127.0.0.1:5000
   - Username: `alice`
   - Password: `pass123`

4. **Check profile page:**
   - Should show: **Alice Johnson** from Boston, MA
   - Phone: 617-555-0101, 617-555-0102

5. **Login as bob:**
   - Username: `bob`
   - Password: `pass456`
   - Should show: **Bob Martinez** from New York, NY
   - Medical History: Diabetes

---

## 🎉 Benefits of This Fix

✅ **Personalized Experience:** Each user sees their own data  
✅ **Data Integrity:** Foreign key ensures valid User_IDs only  
✅ **Better Security:** Can track user actions via User_ID  
✅ **Scalable:** Easy to add more user-specific features  
✅ **Accurate Stats:** Dashboard shows real user's organ requests/donations  

---

## 🚨 Important Notes

- **Admin account** has `User_ID = NULL` (system account, not linked to User table)
- **All user accounts** (alice, bob, etc.) are now linked to real User records
- **Profile pages** now show CORRECT user data based on who logged in
- **Dashboard stats** are personalized for each logged-in user

---

**Created:** October 28, 2025  
**Project:** Organ Transplantation Network  
**Database:** DBMS_PROJECT
