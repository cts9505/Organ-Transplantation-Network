# 🏥 Smart Patient Registration & Organ Matching System

## 🎯 Overview

A comprehensive patient registration and intelligent organ matching system that streamlines the organ transplant request process.

---

## 🆕 New Features Added

### 1. **Patient Registration Page** (`/user/register_patient`)
Complete registration system for users to register as patients before requesting organs.

### 2. **Smart Organ Request Page** (`/user/request_organ_smart`)
Intelligent page that auto-fetches patient details and shows compatible donor matches.

### 3. **Transaction Initiation** (`/user/initiate_transaction`)
One-click organ request system that creates transactions directly from matches.

---

## 📋 Complete User Flow

```
Step 1: Login as User
   ↓
Step 2: Register as Patient
   │   ├─ Fill patient registration form
   │   ├─ Select organ needed
   │   ├─ Provide medical condition
   │   └─ Assign doctor
   ↓
Step 3: Smart Organ Request
   │   ├─ Auto-fetch patient profile
   │   ├─ Show organ needed
   │   └─ Display medical details
   ↓
Step 4: View Compatible Matches
   │   ├─ AI matching algorithm runs
   │   ├─ Shows compatibility scores
   │   ├─ Displays donor details
   │   └─ Sorted by best match
   ↓
Step 5: Request Organ
   │   ├─ Click "Request This Organ"
   │   └─ Transaction created automatically
   ↓
Step 6: Track Transaction
       └─ View in Transaction History
```

---

## 🎨 Page 1: Patient Registration

### **Route:** `/user/register_patient`

### **Features:**
- ✅ **Auto-detection** of already registered patients
- ✅ Comprehensive medical information collection
- ✅ Urgency level selection (Critical/Urgent/Normal)
- ✅ Blood group and wait time tracking
- ✅ Doctor assignment
- ✅ Additional notes section

### **Form Fields:**

#### **Patient Information:**
- Patient ID (unique identifier)
- Urgency Level (Critical/Urgent/Normal)

#### **Medical Details:**
- Organ Required (dropdown: Kidney, Liver, Heart, etc.)
- Medical Condition (detailed description)
- Primary Diagnosis
- Blood Group (optional)
- Wait Time (optional)

#### **Doctor Information:**
- Assigned Doctor ID
- Doctor Name (optional reference)

#### **Additional:**
- Additional Notes (optional)

### **Validation:**
- ✅ Checks if Patient ID already exists
- ✅ Verifies user is logged in
- ✅ Ensures all required fields are filled

### **Success Flow:**
```
Form Submit → Validate → Insert to Patient table → Redirect to Smart Request Page
```

---

## 🎯 Page 2: Smart Organ Request

### **Route:** `/user/request_organ_smart`

### **Auto-Fetched Patient Data:**
```python
patient_data = {
    'Patient_ID': 201,
    'Organ_Needed': 'Kidney',
    'Medical_Condition': 'Chronic kidney disease stage 5',
    'Doctor_Name': 'Dr. Sarah Williams',
    'Hospital': 'Central Hospital',
    'Status': 'Active'
}
```

### **Intelligent Matching Algorithm:**

#### **Matching Criteria:**
1. **Organ Type Match** (Required)
   - Exact match: Patient needs Kidney → Donor has Kidney available

2. **Compatibility Scoring:**
   ```
   Base Score: 60 points (organ type match)
   + 20 points: Same hospital/organization
   + 10 points: Living donation (better quality)
   + 10 points: Patient has medical insurance
   ─────────────────────────────────
   Maximum: 100% compatibility
   ```

3. **Availability Filter:**
   - Only shows organs not already in transactions
   - Real-time availability check

#### **Scoring Examples:**

**Scenario 1: Excellent Match (90%)**
- ✅ Organ matches (60%)
- ✅ Same hospital (+20%)
- ✅ Patient has insurance (+10%)
- Result: **90% Match**

**Scenario 2: Good Match (70%)**
- ✅ Organ matches (60%)
- ✅ Living donation (+10%)
- Result: **70% Match**

**Scenario 3: Fair Match (60%)**
- ✅ Organ matches (60%)
- Result: **60% Match**

### **Match Display:**

Each match card shows:
```
┌─────────────────────────────────┐
│ 💝 Kidney Donor        [90% Match] │
│                                   │
│ Donor: Bob Martinez              │
│ Donor ID: 302                    │
│ Organ ID: 5002                   │
│ Hospital: Central Hospital       │
│ Type: Living donation            │
│                                   │
│ ⭐ Excellent Match                │
│                                   │
│ [📝 Request This Organ]          │
└─────────────────────────────────┘
```

### **Compatibility Badges:**
- 🟢 **Excellent Match:** 80-100% (Green badge)
- 🟡 **Good Match:** 60-79% (Blue badge)
- 🟠 **Fair Match:** <60% (Orange badge)

### **Statistics Shown:**
- Total compatible matches found
- Number of available donors
- Organ type being searched for

---

## 🔄 Page 3: Transaction Initiation

### **Route:** `/user/initiate_transaction` (POST)

### **How It Works:**
```
1. User clicks "Request This Organ" on match card
   ↓
2. Form submits with hidden fields:
   - patient_id
   - organ_id
   - donor_id
   ↓
3. Backend creates transaction:
   - Current date
   - Status: 0 (Pending)
   ↓
4. Redirect to Transaction History
   ↓
5. User sees new pending transaction
```

### **Transaction Record Created:**
```sql
INSERT INTO Transaction VALUES (
    Patient_ID: 201,
    Organ_ID: 5002,
    Donor_ID: 302,
    Date: 2025-10-28,
    Status: 0  -- Pending approval
)
```

---

## 🗄️ Database Integration

### **Tables Used:**

1. **Patient Table:**
   ```sql
   Patient (
       Patient_ID,
       organ_req,           -- Auto-filled from registration
       reason_of_procurement, -- Medical condition
       Doctor_ID,
       User_ID             -- Linked to logged-in user
   )
   ```

2. **Organ_available Table:**
   ```sql
   Organ_available (
       Organ_ID,
       Organ_name,         -- Must match patient's organ_req
       Donor_ID
   )
   ```

3. **Transaction Table:**
   ```sql
   Transaction (
       Patient_ID,         -- From patient registration
       Organ_ID,          -- From selected match
       Donor_ID,          -- From selected match
       Date_of_transaction, -- Auto: current date
       Status             -- 0 = Pending, 1 = Success
   )
   ```

---

## 🔐 Security Features

### **Authentication:**
- ✅ All routes check `session['login']`
- ✅ User_ID fetched from login table
- ✅ Can only register yourself (not others)

### **Data Validation:**
- ✅ Patient ID uniqueness check
- ✅ Doctor ID must exist
- ✅ Organ type validation
- ✅ SQL injection protection (parameterized queries recommended)

### **Privacy:**
- ✅ Users only see their own patient profile
- ✅ Cannot view other patients' medical records
- ✅ Transaction history shows only user's transactions

---

## 🎨 Updated Dashboard

### **New Cards Added:**

**1. Register as Patient** (Teal border)
```html
📝 Register as Patient
Register yourself as a patient to request organ 
transplants and access matching system.
```

**2. Smart Organ Request** (Yellow border)
```html
🎯 Smart Organ Request
Auto-match with compatible donors using our 
intelligent matching algorithm.
```

**Updated:**
- **Find All Matches** - Now shows all network-wide matches
- Original "Request Organ" removed (replaced by smart system)

---

## 🧪 Testing Flow

### **Test Scenario 1: New Patient Registration**

```bash
# 1. Login as alice
Username: alice
Password: pass123

# 2. Click "Register as Patient"

# 3. Fill form:
Patient ID: 301
Organ Needed: Kidney
Urgency: Critical
Medical Condition: End-stage renal disease
Doctor ID: 1

# 4. Submit → Redirects to Smart Request Page

# 5. See auto-fetched profile:
✓ Patient ID: 301
✓ Organ Needed: Kidney
✓ Medical Condition: End-stage renal disease
✓ Doctor: Dr. Sarah Williams

# 6. View compatible matches (if any Kidney donors exist)

# 7. Click "Request This Organ" on best match

# 8. Verify transaction created in Transaction History
```

### **Test Scenario 2: Already Registered Patient**

```bash
# 1. Login as bob (already registered)

# 2. Click "Smart Organ Request"

# 3. Auto-loads Bob's patient profile

# 4. Shows compatible matches for Bob's needed organ

# 5. Can request directly without re-registering
```

---

## 📊 Matching Algorithm Details

### **SQL Query for Matches:**

```sql
-- Get available organs matching patient's need
SELECT 
    oa.Organ_ID,
    oa.Organ_name,
    oa.Donor_ID,
    don.reason_of_donation,
    don.Organization_ID,
    u.Name as donor_name,
    org.Organization_name
FROM Organ_available oa
INNER JOIN Donor don ON oa.Donor_ID = don.Donor_ID
INNER JOIN User u ON don.User_ID = u.User_ID
INNER JOIN Organization org ON don.Organization_ID = org.Organization_ID
WHERE oa.Organ_name = 'Kidney'  -- Patient's needed organ
AND oa.Organ_ID NOT IN (
    SELECT Organ_ID FROM Transaction  -- Exclude already allocated
)
```

### **Scoring Logic:**

```python
def calculate_compatibility(patient, donor, organ):
    score = 60  # Base score for organ match
    
    # Same hospital bonus
    if patient.organization_id == donor.organization_id:
        score += 20
    
    # Living donation bonus (fresher organ)
    if 'living' in donor.donation_reason.lower():
        score += 10
    
    # Medical insurance bonus (better post-op care)
    if patient.has_insurance:
        score += 10
    
    return min(score, 100)  # Cap at 100%
```

---

## 🎯 Benefits

### **For Patients:**
- 🟢 **Easy Registration:** Simple, guided form
- 🟢 **Auto-Matching:** No manual searching
- 🟢 **Transparency:** See compatibility scores
- 🟢 **Quick Requests:** One-click organ requests
- 🟢 **Track Progress:** View all transactions

### **For Hospitals:**
- 🟢 **Efficient Matching:** Automated compatibility scoring
- 🟢 **Priority System:** Urgency levels built-in
- 🟢 **Data Tracking:** Complete patient records
- 🟢 **Better Allocation:** Best matches get priority

### **For System:**
- 🟢 **Scalable:** Handles multiple patients/donors
- 🟢 **Intelligent:** AI-powered matching
- 🟢 **Integrated:** Seamless database flow
- 🟢 **Secure:** User-specific data isolation

---

## 🚀 How to Use

### **1. Apply Database Updates:**
```bash
# Make sure login table is updated
mysql -u root -p DBMS_PROJECT < inserting_data/update_login_table.sql
```

### **2. Start Flask App:**
```bash
python3 main.py
```

### **3. Test the Flow:**
```bash
# Go to: http://127.0.0.1:5000

# Login as alice
Username: alice
Password: pass123

# Navigate:
Dashboard → Register as Patient → Fill Form → 
Smart Request → View Matches → Request Organ
```

---

## 📝 Routes Summary

| Route | Method | Purpose |
|-------|--------|---------|
| `/user/register_patient` | GET | Show patient registration form |
| `/user/submit_patient_registration` | POST | Process registration, create Patient record |
| `/user/request_organ_smart` | GET | Show patient profile + compatible matches |
| `/user/initiate_transaction` | POST | Create transaction from selected match |

---

## 🔄 Data Flow Diagram

```
┌─────────────┐
│   Login     │
│  (alice)    │
└──────┬──────┘
       │
       v
┌─────────────────────┐
│ Get User_ID = 101   │ ← From login table
└──────┬──────────────┘
       │
       v
┌──────────────────────────┐
│ Register as Patient      │
│ - Patient_ID: 301        │
│ - Organ: Kidney          │
│ - User_ID: 101 (alice)   │
└──────┬───────────────────┘
       │
       v
┌──────────────────────────┐
│ Insert to Patient table  │
└──────┬───────────────────┘
       │
       v
┌──────────────────────────────┐
│ Smart Request Page           │
│ - Fetch patient (User_ID=101)│
│ - Get organ needed: Kidney   │
└──────┬───────────────────────┘
       │
       v
┌────────────────────────────────┐
│ Run Matching Algorithm         │
│ - Find Kidney donors           │
│ - Calculate compatibility      │
│ - Sort by score (high→low)     │
└──────┬─────────────────────────┘
       │
       v
┌────────────────────────────────┐
│ Display Matches                │
│ Match 1: 90% - Bob (Kidney)    │
│ Match 2: 70% - Carol (Kidney)  │
└──────┬─────────────────────────┘
       │
       v
┌────────────────────────────────┐
│ User Clicks "Request"          │
│ - Patient_ID: 301              │
│ - Organ_ID: 5002               │
│ - Donor_ID: 302                │
└──────┬─────────────────────────┘
       │
       v
┌────────────────────────────────┐
│ Create Transaction             │
│ - Status: Pending (0)          │
│ - Date: 2025-10-28             │
└──────┬─────────────────────────┘
       │
       v
┌────────────────────────────────┐
│ Transaction History            │
│ Shows new pending request      │
└────────────────────────────────┘
```

---

**Created:** October 28, 2025  
**System:** Organ Transplantation Network  
**Feature:** Smart Patient Registration & Organ Matching  
**Status:** ✅ Complete & Ready to Use
