# 🏥 Organ Transplantation Network

A comprehensive web-based **Organ Transplantation Management System** built with Flask and MySQL. This platform streamlines the organ donation and transplantation process by connecting donors, patients, and healthcare organizations through an intelligent matching algorithm and secure approval workflow.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [User Roles & Functionalities](#-user-roles--functionalities)
- [Smart Matching Algorithm](#-smart-matching-algorithm)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔐 Authentication & Authorization
- Secure user login system with session management
- Role-based access control (Admin, Patient, Donor)
- Password-protected user accounts

### 👤 Patient Features
- **Register as Patient**: Submit medical information and organ requirements
- **Smart Organ Matching**: AI-powered algorithm to find compatible donors
- **Request Transplant**: Initiate transplant requests with duplicate prevention
- **Transaction History**: View all transplant requests with detailed status tracking
- **Donor Contact Info**: Access approved donor contact details post-approval
- **Profile Management**: Update personal and medical information

### 🩸 Donor Features
- **Register as Donor**: Volunteer to donate organs with medical details
- **Available Organs**: List organs available for donation
- **Transaction History**: View donation requests and status
- **Patient Contact Info**: Access approved patient contact details post-approval
- **Profile Management**: Update donation preferences and information

### 🔧 Admin Features
- **Pending Approvals Dashboard**: Review and approve/reject transplant requests
- **All Transactions View**: Monitor all system transactions with complete details
- **User Management**: Add, update, and remove users (patients, donors, doctors, organizations)
- **Statistics Dashboard**: Real-time metrics on total, approved, pending, and rejected transactions
- **System Overview**: Comprehensive admin panel with CRUD operations

### 🧠 Smart Features
- **Intelligent Matching Algorithm**: Scores donor-patient compatibility based on:
  - Organ type compatibility (exact match required)
  - Organization network affiliation (+20 points)
  - Living donation preference (+10 points)
  - Medical insurance status (+10 points)
- **Privacy Protection**: Contact information revealed only after admin approval
- **Bidirectional Information Sharing**: Both patients and donors see relevant details post-approval
- **Real-time Status Updates**: Color-coded transaction cards (Green=Approved, Yellow=Pending, Red=Rejected)
- **Duplicate Prevention**: Prevents multiple requests for the same organ

---

## 🛠 Technologies Used

### Backend
- **Python 3.x** - Core programming language
- **Flask** - Web framework for routing and application logic
- **MySQL** - Relational database for data persistence
- **mysql-connector-python** - Database connectivity

### Frontend
- **HTML5 & CSS3** - Structure and styling
- **Jinja2** - Template engine for dynamic content
- **Bootstrap 4** - Responsive UI components
- **JavaScript** - Client-side interactions and form validations

### Design
- **Gradient Backgrounds** - Modern purple/blue/pink theme
- **Card-based Layout** - Clean and organized UI
- **Responsive Design** - Mobile-friendly interface

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (Client)                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Flask Application (main.py)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes & Controllers                                 │   │
│  │  - Authentication (/login, /signup)                   │   │
│  │  - Patient (/user/register_patient, /user/find_matches) │
│  │  - Donor (/user/donate_organ)                         │   │
│  │  - Admin (/admin/pending_approvals, /admin/all_transactions) │
│  │  - Transactions (/user/initiate_transaction)          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Business Logic                                       │   │
│  │  - Smart Matching Algorithm                           │   │
│  │  - Transaction Management                             │   │
│  │  - User Management (CRUD)                             │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MySQL Database                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tables:                                              │   │
│  │  - User, User_phone_no                                │   │
│  │  - Patient, Donor                                     │   │
│  │  - Doctor, Organization                               │   │
│  │  - Organ_available                                    │   │
│  │  - Transaction                                        │   │
│  │  - login                                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/yourusername/Organ-Transplantation-Network.git
cd Organ-Transplantation-Network-master
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Flask==2.3.0
mysql-connector-python==8.0.33
python-dotenv==1.0.0
```

### Configure Environment Variables

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` file with your MySQL credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=DBMS_PROJECT

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

⚠️ **Important**: Never commit the `.env` file to version control. It's already included in `.gitignore`.

---

## 💾 Database Setup

### 1. Create Database
```bash
mysql -u root -p
```

```sql
CREATE DATABASE DBMS_PROJECT;
USE DBMS_PROJECT;
```

### 2. Create Tables
Run the SQL script to create all necessary tables:

```bash
mysql -u root -p DBMS_PROJECT < create_tables_fixed.sql
```

**Or manually execute:**
```bash
mysql -u root -p DBMS_PROJECT < create_tables.sql
```

### 3. Insert Demo Data (Optional)
Populate the database with sample data:

```bash
mysql -u root -p DBMS_PROJECT < inserting_data/complete_demo_data.sql
```

**Or insert specific data:**
```bash
# Insert users, patients, donors, organizations, doctors
mysql -u root -p DBMS_PROJECT < inserting_data/insert_them_all.sql
```

---

## ▶️ Running the Application

### 1. Install python-dotenv (if not already installed)
```bash
pip install python-dotenv
```

### 2. Configure your environment
Make sure your `.env` file is properly configured with your MySQL credentials (see [Installation](#-installation) section).

### 3. Start the Flask Server
```bash
python3 main.py
```

The application will start on `http://127.0.0.1:5000/`

### Default Login Credentials

**Admin:**
- Username: `admin`
- Password: `admin`

**Test User (Patient):**
- Username: `alice`
- Password: `pass123`

**Test Donors:**
- Donors with IDs 501-508 are available for testing

---

## 👥 User Roles & Functionalities

### 🔴 Admin Role

| Feature | Description | Route |
|---------|-------------|-------|
| Pending Approvals | Review and approve/reject transplant requests | `/admin/pending_approvals` |
| All Transactions | View complete system transaction history | `/admin/all_transactions` |
| User Management | Add/Update/Remove users, patients, donors | `/add_page`, `/update_*`, `/remove_*` |
| Statistics | Real-time dashboard with transaction metrics | Embedded in admin pages |

### 🟢 Patient Role

| Feature | Description | Route |
|---------|-------------|-------|
| Register Patient | Submit medical info and organ requirements | `/user/register_patient` |
| Find Matches | Smart algorithm to find compatible donors | `/user/find_matches` |
| Request Transplant | Initiate transplant request | `/user/initiate_transaction` |
| Transaction History | View all requests with status tracking | `/user/transaction_history` |
| Edit Profile | Update patient information | `/user/edit_patient` |

### 🟡 Donor Role

| Feature | Description | Route |
|---------|-------------|-------|
| Register Donor | Submit donation preferences and medical info | `/user/donate_organ` |
| Transaction History | View donation requests and status | `/user/transaction_history` |
| Profile Management | Update donor information | `/user/profile` |

---

## 🧠 Smart Matching Algorithm

The system uses an intelligent scoring algorithm to match patients with compatible donors:

### Matching Criteria

```python
Base Score: 60 points (organ type exact match required)
+ 20 points: Same organization affiliation
+ 10 points: Living donation (fresher organs)
+ 10 points: Patient has medical insurance

Maximum Score: 100 points
```

### Matching Process

1. **Step 1**: Fetch all patient requests from the database
2. **Step 2**: Retrieve all available organs (not already allocated)
3. **Step 3**: Filter by organ type compatibility
4. **Step 4**: Calculate compatibility score for each match
5. **Step 5**: Sort matches by score (highest first)
6. **Step 6**: Display ranked list to patient

### Example Output
```
Heart Transplant Matches:
1. Donor: John Doe (Score: 90) - Same Organization, Living Donor
2. Donor: Jane Smith (Score: 70) - Living Donor
3. Donor: Bob Wilson (Score: 60) - Base Match
```

---

## 📸 Screenshots

### Login Page
Beautiful gradient-based authentication system

### Patient Dashboard
- Register as patient
- Find organ matches
- Request transplants
- View transaction history

### Admin Dashboard
- Pending approvals with statistics
- Complete transaction monitoring
- User management (CRUD operations)

### Transaction History
- Color-coded status cards
- Detailed patient/donor information
- Contact details (post-approval)
- Bidirectional information sharing

---

## 📁 Project Structure

```
Organ-Transplantation-Network-master/
│
├── main.py                          # Flask application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── LICENSE                          # License information
│
├── ER diagrams/
│   └── ER.png.dup0                 # Entity-Relationship diagram
│
├── templates/                       # HTML templates (Jinja2)
│   ├── login.html                  # Login page
│   ├── home.html                   # Admin home page
│   ├── user_dashboard.html         # User dashboard
│   ├── user_register_patient.html  # Patient registration
│   ├── user_donate_organ.html      # Donor registration
│   ├── user_find_matches.html      # Smart matching page
│   ├── user_transaction_history.html # Transaction history
│   ├── admin_pending_approvals.html  # Admin approvals
│   ├── admin_all_transactions.html   # All transactions view
│   ├── add_page.html               # Add entities
│   ├── update_*.html               # Update pages
│   ├── remove_*.html               # Remove pages
│   └── ...
│
├── static/                          # Static assets (CSS, JS, images)
│
├── inserting_data/                  # SQL data insertion scripts
│   ├── complete_demo_data.sql      # Complete demo dataset
│   ├── insert_them_all.sql         # All entities insert
│   ├── insert_user.sql             # User data
│   ├── insert_patient.sql          # Patient data
│   ├── insert_donor.sql            # Donor data
│   ├── insert_doctor.sql           # Doctor data
│   ├── insert_organization.sql     # Organization data
│   └── update_login_table.sql      # Login credentials
│
└── SQL Scripts/
    ├── create_tables.sql            # Table creation script
    └── create_tables_fixed.sql      # Fixed table schema
```

---

## 🗄 Database Schema

### Core Tables

#### User
```sql
User_ID (PK), Name, Date_of_Birth, Gender, Blood_group,
Street, City, State, Medical_insurance
```

#### User_phone_no
```sql
User_ID (FK), Phone_no
```

#### Patient
```sql
Patient_ID (PK), organ_req, reason_of_procurement,
User_ID (FK), Doctor_ID (FK)
```

#### Donor
```sql
Donor_ID (PK), organ_donated, reason_of_donation,
User_ID (FK), Organization_ID (FK)
```

#### Organ_available
```sql
Organ_ID (PK), Organ_name, Donor_ID (FK)
```

#### Transaction
```sql
Patient_ID (FK), Organ_ID (FK), Donor_ID (FK),
Date_of_transaction, Status
- Status: 0 (Pending), 1 (Approved), 2 (Rejected)
```

#### Doctor
```sql
Doctor_ID (PK), Doctor_Name, Organization_ID (FK)
```

#### Organization
```sql
Organization_ID (PK), Organization_name, Organization_head
```

#### login
```sql
username (PK), password, User_ID (FK)
```

### ER Diagram
See `ER diagrams/ER.png.dup0` for the complete entity-relationship diagram.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Coding Guidelines
- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Test thoroughly before submitting

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact & Support

**Project Maintainer:** Chaitanya Shinde

**Project Link:** [https://github.com/cts9505/Organ-Transplantation-Network](https://github.com/cts9505/Organ-Transplantation-Network)

---

## 🙏 Acknowledgments

- This project was developed as part of a DBMS course project
- Special thanks to all contributors and testers
- Inspired by real-world organ donation networks

---

## 🔮 Future Enhancements

- [ ] Email notifications for transaction status updates
- [ ] Advanced search filters (blood type, location, urgency)
- [ ] Analytics dashboard with charts and graphs
- [ ] Multi-language support
- [ ] Mobile application (React Native/Flutter)
- [ ] API endpoints for third-party integrations
- [ ] Automated matching notifications
- [ ] Waiting list management system
- [ ] Medical record integration
- [ ] Blockchain-based transaction verification

---

## ⚠️ Disclaimer

This is an educational project and should not be used for actual medical organ transplantation management without proper validation, regulatory compliance, and medical oversight.

---

**Made with ❤️ for better healthcare accessibility**
