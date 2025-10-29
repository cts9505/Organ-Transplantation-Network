-- COMPLETE DEMO DATA FOR DBMS_PROJECT
-- This file contains sample data for all tables with proper relationships
-- Run after creating tables with create_tables_fixed.sql

USE DBMS_PROJECT;

-- Disable foreign key checks temporarily for easier insertion
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- 1. LOGIN DATA (already has admin/admin from schema)
-- ============================================================
-- Note: User_ID links login credentials to User table
-- admin has User_ID = NULL (system admin, not a patient/donor)
INSERT INTO login (username, password, User_ID) VALUES 
('alice', 'pass123', 101),
('bob', 'pass456', 102),
('charlie', 'pass789', 103),
('diana', 'pass000', 104);

-- ============================================================
-- 2. USER DATA
-- ============================================================
INSERT INTO User (User_ID, Name, Date_of_Birth, Medical_insurance, Medical_history, Street, City, State) VALUES
(101, 'Alice Johnson', '1985-06-15', 1, 'None', '123 Main St', 'Boston', 'MA'),
(102, 'Bob Martinez', '1990-08-20', 1, 'Diabetes', '456 Oak Ave', 'New York', 'NY'),
(103, 'Carol Singh', '1975-12-01', 1, 'Hypertension', '789 Pine Rd', 'Seattle', 'WA'),
(104, 'David Lee', '1988-03-10', 0, 'Asthma', '321 Elm St', 'Chicago', 'IL'),
(105, 'Emma Wilson', '1992-11-25', 1, 'None', '654 Maple Dr', 'Austin', 'TX'),
(106, 'Frank Brown', '1980-07-18', 1, 'Heart Disease', '987 Cedar Ln', 'Miami', 'FL'),
(107, 'Grace Davis', '1995-01-30', 1, 'None', '147 Birch Ave', 'Denver', 'CO'),
(108, 'Henry Taylor', '1978-09-05', 0, 'Kidney Disease', '258 Spruce Rd', 'Phoenix', 'AZ'),
(109, 'Iris Chen', '1987-04-12', 1, 'None', '369 Willow Way', 'Portland', 'OR'),
(110, 'Jack Miller', '1993-08-22', 1, 'Liver Disease', '741 Ash Blvd', 'Atlanta', 'GA');

-- ============================================================
-- 3. USER PHONE NUMBERS
-- ============================================================
INSERT INTO User_phone_no (User_ID, Phone_no) VALUES
(101, '617-555-0101'),
(101, '617-555-0102'),
(102, '212-555-0201'),
(103, '206-555-0301'),
(103, '206-555-0302'),
(104, '312-555-0401'),
(105, '512-555-0501'),
(106, '305-555-0601'),
(106, '305-555-0602'),
(107, '303-555-0701'),
(108, '602-555-0801'),
(109, '503-555-0901'),
(110, '404-555-1001'),
(110, '404-555-1002');

-- ============================================================
-- 4. ORGANIZATION DATA
-- ============================================================
INSERT INTO Organization (Organization_ID, Organization_name, Location, Government_approved) VALUES
(1, 'Central Hospital', 'Boston', 1),
(2, 'City Medical Center', 'New York', 1),
(3, 'Regional Clinic', 'Seattle', 0),
(4, 'Metro Health Hub', 'Chicago', 1),
(5, 'County General', 'Austin', 1);

-- ============================================================
-- 5. ORGANIZATION PHONE NUMBERS
-- ============================================================
INSERT INTO Organization_phone_no (Organization_ID, Phone_no) VALUES
(1, '617-555-1000'),
(1, '617-555-1001'),
(2, '212-555-2000'),
(3, '206-555-3000'),
(4, '312-555-4000'),
(4, '312-555-4001'),
(5, '512-555-5000');

-- ============================================================
-- 6. ORGANIZATION HEAD DATA
-- ============================================================
INSERT INTO Organization_head (Organization_ID, Employee_ID, Name, Date_of_joining, Term_length) VALUES
(1, 1001, 'Dr. Emily Carter', '2010-01-15', 5),
(1, 1002, 'Dr. Michael Ross', '2015-06-01', 3),
(2, 2001, 'Mr. Rajesh Kumar', '2012-03-10', 4),
(3, 3001, 'Ms. Sarah Connor', '2018-09-20', 2),
(4, 4001, 'Dr. James Wilson', '2011-11-05', 6),
(5, 5001, 'Dr. Lisa Cuddy', '2014-02-14', 4);

-- ============================================================
-- 7. DOCTOR DATA
-- ============================================================
INSERT INTO Doctor (Doctor_ID, Doctor_Name, Department_Name, Organization_ID) VALUES
(201, 'Dr. John Smith', 'Cardiology', 1),
(202, 'Dr. Sarah Lee', 'Nephrology', 1),
(203, 'Dr. Amit Patel', 'General Medicine', 2),
(204, 'Dr. Maria Garcia', 'Hepatology', 2),
(205, 'Dr. Robert Kim', 'Surgery', 3),
(206, 'Dr. Jennifer Wong', 'Transplant', 4),
(207, 'Dr. Thomas Anderson', 'Cardiology', 4),
(208, 'Dr. Patricia Moore', 'Nephrology', 5);

-- ============================================================
-- 8. DOCTOR PHONE NUMBERS
-- ============================================================
INSERT INTO Doctor_phone_no (Doctor_ID, Phone_no) VALUES
(201, '617-555-2001'),
(202, '617-555-2002'),
(203, '212-555-2003'),
(204, '212-555-2004'),
(205, '206-555-2005'),
(206, '312-555-2006'),
(207, '312-555-2007'),
(208, '512-555-2008');

-- ============================================================
-- 9. PATIENT DATA (Composite PK: Patient_ID, organ_req)
-- ============================================================
INSERT INTO Patient (Patient_ID, organ_req, reason_of_procurement, Doctor_ID, User_ID) VALUES
(301, 'Kidney', 'End-stage renal disease', 202, 102),
(302, 'Liver', 'Cirrhosis', 204, 106),
(303, 'Heart', 'Cardiomyopathy', 201, 104),
(304, 'Kidney', 'Chronic kidney disease', 208, 108),
(305, 'Liver', 'Hepatitis', 204, 110),
(306, 'Lung', 'Pulmonary fibrosis', 205, 104),  -- Same patient (104) needs lung too
(307, 'Heart', 'Heart failure', 207, 106);      -- Same patient (106) needs heart too

-- ============================================================
-- 10. DONOR DATA (Composite PK: Donor_ID, organ_donated)
-- ============================================================
INSERT INTO Donor (Donor_ID, organ_donated, reason_of_donation, Organization_ID, User_ID) VALUES
(401, 'Kidney', 'Living donation', 1, 101),
(402, 'Liver', 'Deceased donor', 2, 103),
(403, 'Heart', 'Deceased donor', 4, 105),
(404, 'Kidney', 'Living donation', 5, 107),
(405, 'Liver', 'Deceased donor', 3, 109),
(406, 'Lung', 'Deceased donor', 1, 101),      -- Same donor (101) donates lung too
(407, 'Heart', 'Deceased donor', 2, 103);     -- Same donor (103) donates heart too

-- ============================================================
-- 11. ORGAN_AVAILABLE DATA
-- Note: Organ_ID is AUTO_INCREMENT, so we let MySQL assign IDs
-- ============================================================
INSERT INTO Organ_available (Organ_name, Donor_ID) VALUES
('Kidney', 401),
('Liver', 402),
('Heart', 403),
('Kidney', 404),
('Liver', 405),
('Lung', 406),
('Heart', 407);

-- ============================================================
-- 12. TRANSACTION DATA
-- Note: We need to match Organ_ID values that were auto-generated above
-- Assuming fresh DB, Organ_IDs will be 1-7 in order
-- ============================================================
INSERT INTO `Transaction` (Patient_ID, Organ_ID, Donor_ID, Date_of_transaction, Status) VALUES
(301, 1, 401, '2025-10-01', 1),  -- Patient 301 receives Kidney from Donor 401 (Success)
(302, 2, 402, '2025-10-05', 1),  -- Patient 302 receives Liver from Donor 402 (Success)
(303, 3, 403, '2025-10-10', 0),  -- Patient 303 receives Heart from Donor 403 (Failed)
(304, 4, 404, '2025-10-15', 1),  -- Patient 304 receives Kidney from Donor 404 (Success)
(305, 5, 405, '2025-10-20', 1),  -- Patient 305 receives Liver from Donor 405 (Success)
(306, 6, 406, '2025-10-22', 0),  -- Patient 306 receives Lung from Donor 406 (Failed)
(307, 7, 407, '2025-10-25', 1);  -- Patient 307 receives Heart from Donor 407 (Success)

-- ============================================================
-- 13. LOG DATA (Manual entries - triggers will also populate this)
-- ============================================================
INSERT INTO log (querytime, comment) VALUES
(NOW(), 'Database initialized with demo data'),
('2025-10-01 09:00:00', 'System startup - data migration completed'),
('2025-10-15 14:30:00', 'Routine backup performed');

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- VERIFICATION QUERIES (Optional - comment out if not needed)
-- ============================================================
-- Uncomment these to verify data was inserted correctly

-- SELECT 'Users' as Table_Name, COUNT(*) as Row_Count FROM User
-- UNION ALL SELECT 'User_phone_no', COUNT(*) FROM User_phone_no
-- UNION ALL SELECT 'Organization', COUNT(*) FROM Organization
-- UNION ALL SELECT 'Organization_phone_no', COUNT(*) FROM Organization_phone_no
-- UNION ALL SELECT 'Organization_head', COUNT(*) FROM Organization_head
-- UNION ALL SELECT 'Doctor', COUNT(*) FROM Doctor
-- UNION ALL SELECT 'Doctor_phone_no', COUNT(*) FROM Doctor_phone_no
-- UNION ALL SELECT 'Patient', COUNT(*) FROM Patient
-- UNION ALL SELECT 'Donor', COUNT(*) FROM Donor
-- UNION ALL SELECT 'Organ_available', COUNT(*) FROM Organ_available
-- UNION ALL SELECT 'Transaction', COUNT(*) FROM `Transaction`
-- UNION ALL SELECT 'log', COUNT(*) FROM log
-- UNION ALL SELECT 'login', COUNT(*) FROM login;

COMMIT;

-- ============================================================
-- DATA SUMMARY
-- ============================================================
-- login: 5 entries (admin + 4 users)
-- User: 10 users
-- User_phone_no: 14 phone numbers
-- Organization: 5 organizations
-- Organization_phone_no: 7 phone numbers
-- Organization_head: 6 heads
-- Doctor: 8 doctors
-- Doctor_phone_no: 8 phone numbers
-- Patient: 7 patients (some users need multiple organs)
-- Donor: 7 donors (some users donate multiple organs)
-- Organ_available: 7 organs
-- Transaction: 7 transactions (5 successful, 2 failed)
-- log: 3 initial entries + triggers will add more
