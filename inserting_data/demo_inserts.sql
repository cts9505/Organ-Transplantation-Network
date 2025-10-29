USE DBMS_PROJECT;

-- Logins (admin already present from create_tables.sql)
INSERT INTO login (username, password) VALUES ('alice', 'alicepass');
INSERT INTO login (username, password) VALUES ('bob', 'bobpass');

-- Users
INSERT INTO User (User_ID, Name, Date_of_Birth, Medical_insurance, Medical_history, Street, City, State) VALUES
(1, 'Alice Johnson', '1985-06-15', 1, 'None', '123 Main St', 'Metropolis', 'CA'),
(2, 'Bob Martinez', '1990-08-20', 0, 'Diabetes', '456 Oak Ave', 'Gotham', 'NY'),
(3, 'Carol Singh', '1975-12-01', 1, 'Hypertension', '789 Pine Rd', 'Star City', 'WA');

-- User phone numbers
INSERT INTO User_phone_no (User_ID, phone_no) VALUES
(1, '555-0101'),
(1, '555-0102'),
(2, '555-0201'),
(3, '555-0301');

-- Organizations
INSERT INTO Organization (Organization_ID, Organization_name, Location, Government_approved) VALUES
(1, 'Central Hospital', 'Metropolis', 1),
(2, 'City Clinic', 'Gotham', 0);

-- Organization phone numbers
INSERT INTO Organization_phone_no (Organization_ID, Phone_no) VALUES
(1, '555-1000'),
(2, '555-2000');

-- Organization heads
INSERT INTO Organization_head (Organization_ID, Employee_ID, Name, Date_of_joining, Term_length) VALUES
(1, 1001, 'Dr. Emily Carter', '2010-01-15', 5),
(2, 2001, 'Mr. Rajesh Kumar', '2015-05-10', 3);

-- Doctors
INSERT INTO Doctor (Doctor_ID, Doctor_Name, Department_Name, organization_ID) VALUES
(101, 'Dr. John Smith', 'Cardiology', 1),
(102, 'Dr. Sarah Lee', 'Nephrology', 1),
(103, 'Dr. Amit Patel', 'General Medicine', 2);

-- Doctor phone numbers
INSERT INTO Doctor_phone_no (Doctor_ID, Phone_no) VALUES
(101, '555-1101'),
(102, '555-1202'),
(103, '555-1303');

-- Patients (Patient_ID, organ_req is part of composite PK)
INSERT INTO Patient (Patient_ID, organ_req, reason_of_procurement, Doctor_ID, User_ID) VALUES
(301, 'Kidney', 'End-stage renal disease', 102, 1),
(302, 'Liver', 'Cirrhosis', 101, 2);

-- Donors (Donor_ID, organ_donated composite PK)
INSERT INTO Donor (Donor_ID, organ_donated, reason_of_donation, Organization_ID, User_ID) VALUES
(201, 'Kidney', 'Living donation', 1, 3),
(202, 'Liver', 'Deceased donor', 2, 2);

-- Organs available (Organ_ID is AUTO_INCREMENT)
INSERT INTO Organ_available (Organ_name, Donor_ID) VALUES
('Kidney', 201),
('Liver', 202);

-- Transactions (Patient_ID, Organ_ID, Donor_ID, Date_of_transaction, Status)
-- Organ_ID values will be the auto-generated IDs assigned above; commonly 1 and 2 in a fresh DB.
-- If Organ_ID values differ, adjust accordingly after checking INSERT results.
INSERT INTO Transaction (Patient_ID, Organ_ID, Donor_ID, Date_of_transaction, Status) VALUES
(301, 1, 201, '2025-10-01', 1),
(302, 2, 202, '2025-10-05', 0);

-- Optional: add a few entries to the log table for demonstration (triggers will also populate this table when inserts happen)
INSERT INTO log (querytime, comment) VALUES
(NOW(), 'Demo log entry: initial data loaded');

COMMIT;
