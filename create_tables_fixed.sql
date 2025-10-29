-- CORRECTED SCHEMA FOR DBMS_PROJECT
-- Fixes: FK referencing composite keys, trigger bugs, casing inconsistencies, Transaction table creation
-- Safe to run: DROP DATABASE first or create fresh DB

CREATE DATABASE IF NOT EXISTS DBMS_PROJECT;
USE DBMS_PROJECT;

-- ============================================================
-- TABLE DEFINITIONS
-- ============================================================

-- Login table (no PK defined - consider adding username as PK if needed)
CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY(username)
) ENGINE=InnoDB;

INSERT INTO login VALUES ('admin','admin');

-- Table 1: User
CREATE TABLE User(
    User_ID INT NOT NULL,
    Name VARCHAR(20) NOT NULL,
    Date_of_Birth DATE NOT NULL,
    Medical_insurance INT,
    Medical_history VARCHAR(20),
    Street VARCHAR(20),
    City VARCHAR(20),
    State VARCHAR(20),
    PRIMARY KEY(User_ID)
) ENGINE=InnoDB;

-- Table 2: User phone numbers
CREATE TABLE User_phone_no(
    User_ID INT NOT NULL,
    Phone_no VARCHAR(15),
    FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table 3: Organization
CREATE TABLE Organization(
    Organization_ID INT NOT NULL,
    Organization_name VARCHAR(20) NOT NULL,
    Location VARCHAR(20),
    Government_approved INT, -- 0 or 1
    PRIMARY KEY(Organization_ID)
) ENGINE=InnoDB;

-- Table 9: Organization phone numbers
CREATE TABLE Organization_phone_no(
    Organization_ID INT NOT NULL,
    Phone_no VARCHAR(15),
    FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table 11: Organization head
CREATE TABLE Organization_head(
    Organization_ID INT NOT NULL,
    Employee_ID INT NOT NULL,
    Name VARCHAR(20) NOT NULL,
    Date_of_joining DATE NOT NULL,
    Term_length INT NOT NULL,
    FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE,
    PRIMARY KEY(Organization_ID, Employee_ID)
) ENGINE=InnoDB;

-- Table 4: Doctor
CREATE TABLE Doctor(
    Doctor_ID INT NOT NULL,
    Doctor_Name VARCHAR(20) NOT NULL,
    Department_Name VARCHAR(20) NOT NULL,
    Organization_ID INT NOT NULL,
    FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE,
    PRIMARY KEY(Doctor_ID)
) ENGINE=InnoDB;

-- Table 10: Doctor phone numbers
CREATE TABLE Doctor_phone_no(
    Doctor_ID INT NOT NULL,
    Phone_no VARCHAR(15),
    FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table 5: Patient
-- Composite PK: (Patient_ID, organ_req)
CREATE TABLE Patient(
    Patient_ID INT NOT NULL,
    organ_req VARCHAR(20) NOT NULL,
    reason_of_procurement VARCHAR(20),
    Doctor_ID INT NOT NULL,
    User_ID INT NOT NULL,
    FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE,
    PRIMARY KEY(Patient_ID, organ_req)
) ENGINE=InnoDB;

-- Table 6: Donor
-- Composite PK: (Donor_ID, organ_donated)
CREATE TABLE Donor(
    Donor_ID INT NOT NULL,
    organ_donated VARCHAR(20) NOT NULL,
    reason_of_donation VARCHAR(20),
    Organization_ID INT NOT NULL,
    User_ID INT NOT NULL,
    FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE,
    PRIMARY KEY(Donor_ID, organ_donated)
) ENGINE=InnoDB;

-- Table 7: Organ_available
-- NOTE: Original FK references Donor(Donor_ID) but Donor has composite PK (Donor_ID, organ_donated).
-- FIXED: Remove FK or add organ_donated to this table to reference full composite key.
-- For simplicity, we remove the FK constraint here (organs are managed by app logic).
CREATE TABLE Organ_available(
    Organ_ID INT NOT NULL AUTO_INCREMENT,
    Organ_name VARCHAR(20) NOT NULL,
    Donor_ID INT NOT NULL,
    PRIMARY KEY(Organ_ID)
    -- NOTE: No FK to Donor because Donor has composite PK.
    -- If you want FK, add organ_donated column and use:
    -- organ_donated VARCHAR(20) NOT NULL,
    -- FOREIGN KEY(Donor_ID, organ_donated) REFERENCES Donor(Donor_ID, organ_donated) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table 8: Transaction
-- FIXED: Removed invalid FKs that referenced partial composite keys.
-- If you need FK enforcement, add organ_req and organ_donated columns to reference Patient and Donor composite keys.
CREATE TABLE `Transaction`(
    Patient_ID INT NOT NULL,
    Organ_ID INT NOT NULL,
    Donor_ID INT NOT NULL,
    Date_of_transaction DATE NOT NULL,
    Status INT NOT NULL, -- 0 or 1
    PRIMARY KEY(Patient_ID, Organ_ID)
    -- NOTE: No FKs here because Patient and Donor have composite PKs.
    -- If you want FK enforcement, modify as follows:
    -- organ_req VARCHAR(20) NOT NULL,
    -- organ_donated VARCHAR(20) NOT NULL,
    -- FOREIGN KEY(Patient_ID, organ_req) REFERENCES Patient(Patient_ID, organ_req) ON DELETE CASCADE,
    -- FOREIGN KEY(Donor_ID, organ_donated) REFERENCES Donor(Donor_ID, organ_donated) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Log table for triggers
CREATE TABLE log(
    querytime DATETIME,
    comment VARCHAR(255)
) ENGINE=InnoDB;

-- ============================================================
-- TRIGGERS
-- ============================================================
-- All triggers fixed: correct column names (Donor_ID, Patient_ID), proper delimiter usage, typo fixes

DELIMITER //

CREATE TRIGGER ADD_DONOR_LOG
AFTER INSERT ON Donor
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Inserted new Donor ', CAST(NEW.Donor_ID AS CHAR)));
END;
//

CREATE TRIGGER UPD_DONOR_LOG
AFTER UPDATE ON Donor
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Updated Donor Details ', CAST(NEW.Donor_ID AS CHAR)));
END;
//

CREATE TRIGGER DEL_DONOR_LOG
AFTER DELETE ON Donor
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Deleted Donor ', CAST(OLD.Donor_ID AS CHAR)));
END;
//

CREATE TRIGGER ADD_PATIENT_LOG
AFTER INSERT ON Patient
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Inserted new Patient ', CAST(NEW.Patient_ID AS CHAR)));
END;
//

CREATE TRIGGER UPD_PATIENT_LOG
AFTER UPDATE ON Patient
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Updated Patient Details ', CAST(NEW.Patient_ID AS CHAR)));
END;
//

CREATE TRIGGER DEL_PATIENT_LOG
AFTER DELETE ON Patient
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Deleted Patient ', CAST(OLD.Patient_ID AS CHAR)));
END;
//

CREATE TRIGGER ADD_TRANSACTION_LOG
AFTER INSERT ON `Transaction`
FOR EACH ROW
BEGIN
    INSERT INTO log (querytime, comment) 
    VALUES (NOW(), CONCAT('Added Transaction :: Patient ID: ', CAST(NEW.Patient_ID AS CHAR), 
                         '; Donor ID: ', CAST(NEW.Donor_ID AS CHAR)));
END;
//

DELIMITER ;

-- ============================================================
-- OPTIONAL: Uncomment these triggers if you want automatic organ management
-- ============================================================
-- DELIMITER //
-- 
-- CREATE TRIGGER ADD_DONOR_ORGAN
-- AFTER INSERT ON Donor
-- FOR EACH ROW
-- BEGIN
--     INSERT INTO Organ_available (Organ_name, Donor_ID)
--     VALUES (NEW.organ_donated, NEW.Donor_ID);
-- END;
-- //
-- 
-- CREATE TRIGGER REMOVE_ORGAN_ON_TRANSACTION
-- AFTER INSERT ON `Transaction`
-- FOR EACH ROW
-- BEGIN
--     DELETE FROM Organ_available WHERE Organ_ID = NEW.Organ_ID;
-- END;
-- //
-- 
-- DELIMITER ;

-- ============================================================
-- NOTES AND RECOMMENDATIONS
-- ============================================================
-- 1. Transaction table: No FKs to Patient/Donor because they have composite PKs.
--    If you need FK enforcement, add organ_req and organ_donated columns.
--
-- 2. Organ_available table: No FK to Donor for same reason.
--    If you want FK, add organ_donated column.
--
-- 3. All triggers use correct column names (Patient_ID, Donor_ID not Patient_Id, Donor_Id).
--
-- 4. All tables use InnoDB engine for FK support.
--
-- 5. Consistent casing: Organization_ID everywhere (not organization_ID).
--
-- 6. login table now has a PRIMARY KEY on username.
--
-- To use this file:
-- Option A (fresh DB): DROP DATABASE DBMS_PROJECT; then run this file
-- Option B (existing DB): DROP all tables first, then run this file
-- Option C (safest): mysql -u root -p < create_tables_fixed.sql
