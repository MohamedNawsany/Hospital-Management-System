CREATE DATABASE IF NOT EXISTS hospitalll_db;
USE hospitalll_db;

-- ✅ Parent Table for All Employees
CREATE TABLE IF NOT EXISTS employee (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    department VARCHAR(100) NOT NULL,
    nationality VARCHAR(100) NOT NULL
);

-- ✅ Doctor Table (Inherits from Employee)
CREATE TABLE IF NOT EXISTS doctor (
    id INT PRIMARY KEY,
    specialization VARCHAR(100) NOT NULL,
    FOREIGN KEY (id) REFERENCES employee(id) ON DELETE CASCADE
);

-- ✅ Nurse Table (Inherits from Employee)
CREATE TABLE IF NOT EXISTS nurse (
    id INT PRIMARY KEY,
    specialty VARCHAR(100) NOT NULL,
    FOREIGN KEY (id) REFERENCES employee(id) ON DELETE CASCADE
);

-- ✅ Manager Table (Inherits from Employee)
CREATE TABLE IF NOT EXISTS manager (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES employee(id) ON DELETE CASCADE
);

-- ✅ Data Entry Table (Inherits from Employee)
CREATE TABLE IF NOT EXISTS data_entry (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES employee(id) ON DELETE CASCADE
);

-- ✅ Patient Table
CREATE TABLE IF NOT EXISTS patient (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    medical_history TEXT
);

-- ✅ Prescription Table (Links Doctor & Patient)
CREATE TABLE IF NOT EXISTS prescription (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    medication VARCHAR(255) NOT NULL,
    date_issued DATETIME NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctor(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
);

-- ✅ Printed Prescriptions Table (Logs Prescription Printing)
CREATE TABLE IF NOT EXISTS printed_prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prescription_id INT NOT NULL,
    data_entry_id INT NOT NULL,
    printed_at DATETIME NOT NULL,
    FOREIGN KEY (prescription_id) REFERENCES prescription(id) ON DELETE CASCADE,
    FOREIGN KEY (data_entry_id) REFERENCES data_entry(id) ON DELETE CASCADE
);


