from datetime import date, datetime
from abc import ABC, abstractmethod
import mysql.connector

class Person(ABC):
    def __init__(self, id, name, birth_year, gender, phone_number, nationality):
        if not all([id, name, birth_year, gender, phone_number, nationality]):  
            raise ValueError("All fields are required and cannot be None or empty.")
        
        if not isinstance(birth_year, int) or birth_year <= 0:
            raise ValueError("Birth year must be a positive integer.")

        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")
        
        self.id = id
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.phone_number = phone_number
        self.nationality = nationality

    def display_info(self):
        print(f"ID: {self.id}, Name: {self.name}, Age: {self.calculate_age()}, Nationality: {self.nationality}")

    def calculate_age(self):
        current_year = date.today().year
        return current_year - self.birth_year

# Abstract Employee class
class Employee(Person, ABC):
    def __init__(self, id, name, birth_year, gender, phone_number, nationality, salary, department):
        super().__init__(id, name, birth_year, gender, phone_number, nationality)
        
        if salary <= 0:
            raise ValueError("Salary must be a positive number.")

        self.salary = salary
        self.department = department
    
    @abstractmethod
    def perform_duties(self):
        pass  # Abstract method to be implemented by subclasses

    def display_info(self):
        super().display_info()
        print(f"Department: {self.department}, Salary: {self.salary}")

    def save_to_db(self):
        db = HospitalDatabase()
        try:
            sql = """
            INSERT INTO employee (id, name, birth_year, gender, phone_number, salary, department, nationality)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (self.id, self.name, self.birth_year, self.gender, self.phone_number, self.salary, self.department, self.nationality)
            db.cursor.execute(sql, values)
            db.conn.commit()
            print(f"✅ Employee {self.name} saved to database.")
        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")

# Doctor class
class Doctor(Employee):
    def __init__(self, id, name, birth_year, gender, phone_number, nationality, salary, department, specialization):
        """Initialize Doctor with required fields."""
        if not all([id, name, birth_year, gender, phone_number, nationality, salary, department, specialization]):
            raise ValueError("❌ All fields are required and cannot be None or empty.")

        if not isinstance(salary, (int, float)) or salary <= 0:
            raise ValueError("❌ Salary must be a positive number.")

        super().__init__(id, name, birth_year, gender, phone_number, nationality, salary, department)
        self.specialization = specialization
    
    def diagnose_patient(self):
        print(f"👨‍⚕️ {self.name} is diagnosing a patient.")
    
    def write_prescription(self, patient, medication):
        if not isinstance(patient, Patient):
            raise TypeError("❌ Invalid patient object.")

        if not isinstance(medication, str) or not medication.strip():
            raise ValueError("❌ Medication must be a non-empty string.")

        prescription = PrescriptionFactory.create_prescription(self, patient, medication)
        patient.add_prescription(prescription)
    
    def perform_duties(self):
        print(f"🩺 {self.name} is treating patients.")

    def display_info(self):
        super().display_info()
        print(f"🩻 Specialization: {self.specialization}")

# Patient class
class Patient(Person):
    def __init__(self, id, name, birth_year, gender, phone_number, nationality, medical_history):
        if not all([id, name, birth_year, gender, phone_number, nationality, medical_history]):
            raise ValueError("All fields are required and cannot be None or empty.")

        if not isinstance(medical_history, list):
            raise TypeError("Medical history must be a list.")

        super().__init__(id, name, birth_year, gender, phone_number, nationality)
        self.medical_history = medical_history
        self.prescriptions = []  # Initialize an empty list of prescriptions

    def add_prescription(self, prescription):
        if prescription in self.prescriptions:
            print(f"⚠️ Prescription for {prescription.medication} already exists for {self.name}.")
        else:
            self.prescriptions.append(prescription)

    def display_info(self):
        super().display_info()
        print(f"Medical History: {', '.join(self.medical_history)}")

    def save_to_db(self):
        db = HospitalDatabase()
        try:
            sql = """
            INSERT INTO patient (id, name, birth_year, gender, phone_number, nationality, medical_history)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            values = (self.id, self.name, self.birth_year, self.gender, self.phone_number, self.nationality, ", ".join(self.medical_history))
            db.cursor.execute(sql, values)
            db.conn.commit()
            print(f"✅ Patient {self.name} saved to database.")
        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")

class DataEntry(Employee):
    def __init__(self, id, name, birth_year, gender, phone_number, salary, department, nationality):
        if not all([id, name, birth_year, gender, phone_number, salary, department, nationality]):
            raise ValueError("All fields are required and cannot be None or empty.")

        if not isinstance(salary, (int, float)) or salary <= 0:
            raise ValueError("Salary must be a positive number.")

        super().__init__(id, name, birth_year, gender, phone_number, nationality, salary, department)

    def add_record(self, person):
        print(f"Record added for: {person.name}")

    def delete_record(self, person): 
        if person is None:
            raise ValueError("Cannot delete a non-existent record.")
        print(f"Record deleted for: {person.name}")

    def perform_duties(self):
        print(f"{self.name} is managing data entries.")

    def display_info(self):
        super().display_info()

    def print_prescription(self, prescription_id):
     if not isinstance(prescription_id, int) or prescription_id <= 0:
        raise TypeError("Invalid prescription ID. Must be a positive integer.")

     db = HospitalDatabase()
     try:
        sql = """
        INSERT INTO printed_prescriptions (prescription_id, data_entry_id, printed_at)
        VALUES (%s, %s, %s);
        """
        values = (prescription_id, self.id, datetime.now())
        db.cursor.execute(sql, values)
        db.conn.commit()
        print(f"✅ Prescription {prescription_id} logged as printed by Data Entry ID {self.id}")
     except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

# Manager class
class Manager(Employee):
    def __init__(self, id, name, birth_year, gender, phone_number, salary, department, nationality):
        super().__init__(id, name, birth_year, gender, phone_number, nationality, salary, department)

    def perform_duties(self):
        print(f"{self.name} is managing the hospital.")

    def display_info(self):
        super().display_info()

class Nurse(Employee):
    def __init__(self, id, name, birth_year, gender, phone_number, salary, department, nationality, specialty):
        super().__init__(id, name, birth_year, gender, phone_number, nationality, salary, department)
        self.specialty = specialty

    def assist_doctor(self, doctor):
        print(f"{self.name} is assisting {doctor.name} in a procedure.")

    def check_vitals(self, patient):
        print(f"{self.name} is checking vitals for {patient.name}.")

    def perform_duties(self):
        print(f"{self.name} is taking care of patients.")

    def display_info(self):
        super().display_info()
        print(f"Specialty: {self.specialty}")

class Prescription:
    def __init__(self, doctor, patient, medication):
        if not all([doctor, patient, medication]):
            raise ValueError("Doctor, Patient, and Medication are required and cannot be None or empty.")

        if not isinstance(doctor, Doctor):
            raise TypeError("Doctor must be an instance of the Doctor class.")

        if not isinstance(patient, Patient):
            raise TypeError("Patient must be an instance of the Patient class.")

        if not isinstance(medication, str) or not medication.strip():
            raise ValueError("Medication must be a valid string.")

        self.doctor = doctor
        self.patient = patient
        self.medication = medication
        self.date_issued = datetime.now()
        self.id = None  # Initialize id as None

    def display_prescription(self):
        print(f"Prescription Details:\nDoctor: {self.doctor.name}\nPatient: {self.patient.name}\nMedication: {self.medication}\nDate Issued: {self.date_issued}")

    def save_to_db(self):
        db = HospitalDatabase()
        try:
            sql = """
            INSERT INTO prescription (doctor_id, patient_id, medication, date_issued)
            VALUES (%s, %s, %s, %s);
            """
            values = (self.doctor.id, self.patient.id, self.medication, self.date_issued)
            db.cursor.execute(sql, values)
            db.conn.commit()

            # ✅ Debug: Print last inserted row ID
            print(f"🔍 lastrowid: {db.cursor.lastrowid}")

            self.id = db.cursor.lastrowid  # Assigning last inserted ID

            if self.id is None:
                raise ValueError("❌ Prescription ID was not assigned after saving.")

            print(f"✅ Prescription for {self.medication} saved with ID {self.id}.")
        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")

class PrescriptionFactory:
    @staticmethod
    def create_prescription(doctor, patient, medication):
        if not isinstance(doctor, Doctor):
            raise TypeError("Doctor must be an instance of Doctor class.")
        if not isinstance(patient, Patient):
            raise TypeError("Patient must be an instance of Patient class.")
        return Prescription(doctor, patient, medication)

import mysql.connector

class HospitalDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HospitalDatabase, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        try:
            self.conn = mysql.connector.connect(
                host="mysql",  # Use the Docker service name 'mysql'
                user="root",
                password="12345",
                database="hospitalll_db"
            )
            self.cursor = self.conn.cursor()  # Ensure cursor is initialized after connection
            print("✅ Database connection established.")
        except mysql.connector.Error as e:
            print(f"❌ Database connection failed: {e}")
            self.cursor = None  # Set cursor to None in case of failure

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
            print("🔒 Database cursor closed.")
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed.")
        else:
            print("❌ No connection to close.")

    def execute_query(self, query):
        if self.cursor:
            try:
                self.cursor.execute(query)
                self.conn.commit()
            except mysql.connector.Error as e:
                print(f"❌ Query execution failed: {e}")
        else:
            print("❌ No cursor available to execute query.")

# Main Execution
from datetime import date, datetime
import mysql.connector

# Ensure the HospitalDatabase and other classes are imported
# (Assuming they are already defined in your code)

def test_system():
    # Initialize the database connection
    db = HospitalDatabase()

    try:
        # Clear existing data for a clean test
        db.cursor.execute("DELETE FROM printed_prescriptions;")
        db.cursor.execute("DELETE FROM prescription;")
        db.cursor.execute("DELETE FROM patient;")
        db.cursor.execute("DELETE FROM doctor;")
        db.cursor.execute("DELETE FROM employee;")
        db.conn.commit()
        print("✅ Cleared existing data for a clean test.")

        # Step 1: Create and save a DataEntry employee
        data_entry = DataEntry(
            id=31, name="Masri", birth_year=1990, gender="Male",
            phone_number="111223233", salary=3500, department="Records", nationality="saudi"
        )
        data_entry.save_to_db()
        print("✅ DataEntry employee created and saved.")

        # Step 2: Create and save a Patient
        patient = Patient(
            id=1, name="John Ahmed", birth_year=1985, gender="Male",
            phone_number="123456789", nationality="American", medical_history=["Flu", "Allergies"]
        )
        patient.save_to_db()
        print("✅ Patient created and saved.")

        # Step 3: Create and save a Doctor
        doctor = Doctor(
            id=10, name="Dr. Sami", birth_year=1975, gender="Male",
            phone_number="987654321", nationality="British", salary=8000,
            department="Cardiology", specialization="Cardiologist"
        )
        doctor.save_to_db()
        print("✅ Doctor created and saved.")

        # Step 4: Insert the doctor into the `doctor` table
        db.cursor.execute("INSERT INTO doctor (id, specialization) VALUES (%s, %s);", (doctor.id, doctor.specialization))
        db.conn.commit()
        print("✅ Doctor specialization saved to the `doctor` table.")

        # Step 5: Write a prescription and save it
        doctor.write_prescription(patient, "Paracetamol")
        patient.prescriptions[0].save_to_db()
        print("✅ Prescription created and saved.")

        # Step 6: Log the prescription print event
        prescription_id = patient.prescriptions[0].id  # Get the prescription ID
        data_entry.print_prescription(prescription_id)
        print("✅ Prescription print event logged.")

        # Step 7: Fetch and display data from the database
        print("\n📋 Fetching and displaying data from the database:")

        # Fetch employees
        db.cursor.execute("SELECT * FROM employee;")
        employees = db.cursor.fetchall()
        print("\nEmployees:")
        for emp in employees:
            print(emp)

        # Fetch patients
        db.cursor.execute("SELECT * FROM patient;")
        patients = db.cursor.fetchall()
        print("\nPatients:")
        for pat in patients:
            print(pat)

        # Fetch prescriptions
        db.cursor.execute("SELECT * FROM prescription;")
        prescriptions = db.cursor.fetchall()
        print("\nPrescriptions:")
        for pres in prescriptions:
            print(pres)

        # Fetch printed prescriptions
        db.cursor.execute("SELECT * FROM printed_prescriptions;")
        printed_prescriptions = db.cursor.fetchall()
        print("\nPrinted Prescriptions:")
        for pp in printed_prescriptions:
            print(pp)

        # Step 8: Test error handling
        print("\n🧪 Testing error handling:")

        # Try to save a duplicate employee
        try:
            data_entry.save_to_db()
        except mysql.connector.Error as err:
            print(f"❌ Expected error when saving duplicate employee: {err}")

        # Try to write a prescription with invalid medication
        try:
            doctor.write_prescription(patient, "")
        except ValueError as err:
            print(f"❌ Expected error when writing prescription with invalid medication: {err}")

        # Try to log a print event for a non-existent prescription
        try:
            data_entry.print_prescription(999)  # Non-existent prescription ID
        except mysql.connector.Error as err:
            print(f"❌ Expected error when logging print event for non-existent prescription: {err}")

    finally:
        # Close the database connection
        db.close_connection()
        print("🔒 Database connection closed.")

# Run the test
if __name__ == "__main__":
    test_system()


import pytest
from datetime import datetime
from hospital import Doctor, Patient, Prescription, PrescriptionFactory, HospitalDatabase

# ✅ Fixture for valid Doctor instance
@pytest.fixture
def valid_doctor():
    return Doctor(301, "Dr. Emily Carter", 1985, "Female", "5551112222", "Canadian", 120000, "Surgery", "Neurosurgeon")

# ✅ Fixture for valid Patient instance
@pytest.fixture
def valid_patient():
    return Patient(401, "John Smith", 1995, "Male", "4445556666", "American", ["Asthma"])

# ✅ Fixture for valid Prescription instance
@pytest.fixture
def valid_prescription(valid_doctor, valid_patient):
    return Prescription(valid_doctor, valid_patient, "Amoxicillin")

# ✅ Fixture for HospitalDatabase instance (ensure a clean test DB)
@pytest.fixture(scope="module")
def hospital_db():
    db = HospitalDatabase()
    yield db
    db.close_connection()  # Ensure connection closes after tests


# ✅ Test Prescription Object Creation
def test_prescription_creation(valid_prescription):
    """Test that a Prescription object is correctly initialized"""
    assert valid_prescription.doctor.name == "Dr. Emily Carter"
    assert valid_prescription.patient.name == "John Smith"
    assert valid_prescription.medication == "Amoxicillin"
    assert isinstance(valid_prescription.date_issued, datetime)


# ✅ Test Invalid Prescription (Missing Fields)
def test_invalid_prescription_missing_field(valid_doctor, valid_patient):
    """Test that missing fields raise ValueError"""
    with pytest.raises(ValueError):
        Prescription(None, valid_patient, "Paracetamol")  # Missing doctor
    
    with pytest.raises(ValueError):
        Prescription(valid_doctor, None, "Paracetamol")  # Missing patient
    
    with pytest.raises(ValueError):
        Prescription(valid_doctor, valid_patient, None)  # Missing medication

# ✅ Test Invalid Prescription (Wrong Type)
def test_invalid_prescription_wrong_type(valid_doctor, valid_patient):
    """Test incorrect object types raise TypeError"""
    with pytest.raises(TypeError):
        Prescription("Dr. Fake", valid_patient, "Paracetamol")  # Doctor must be an instance of Doctor class

    with pytest.raises(TypeError):
        Prescription(valid_doctor, "John Doe", "Paracetamol")  # Patient must be an instance of Patient class

    with pytest.raises(ValueError):
        Prescription(valid_doctor, valid_patient, "")  # Medication must be non-empty string


# ✅ Test Prescription Display Method
def test_prescription_display_info(valid_prescription, capsys):
    """Test the display_prescription method"""
    valid_prescription.display_prescription()
    captured = capsys.readouterr()
    assert "Prescription Details:" in captured.out
    assert "Dr. Emily Carter" in captured.out
    assert "John Smith" in captured.out
    assert "Amoxicillin" in captured.out


# ✅ Test PrescriptionFactory Create Method
def test_prescription_factory(valid_doctor, valid_patient):
    """Test that the factory correctly creates Prescription objects"""
    prescription = PrescriptionFactory.create_prescription(valid_doctor, valid_patient, "Ibuprofen")
    assert isinstance(prescription, Prescription)
    assert prescription.medication == "Ibuprofen"


# ✅ Test Prescription Save to Database
def test_prescription_save_to_db(valid_prescription, hospital_db):
    """Test that the prescription can be saved to the database"""
    try:
        valid_prescription.save_to_db()
        assert valid_prescription.id is not None  # ID should be set after saving
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


# ✅ Test HospitalDatabase Singleton
def test_hospital_database_singleton():
    """Ensure that only one instance of the database exists"""
    db1 = HospitalDatabase()
    db2 = HospitalDatabase()
    assert db1 is db2  # Both instances should be the same


# ✅ Test HospitalDatabase Connection
def test_hospital_database_connection(hospital_db):
    """Test that the database connection is established"""
    assert hospital_db.conn is not None
    assert hospital_db.cursor is not None


# ✅ Test HospitalDatabase Closing Connection
def test_hospital_database_close_connection(hospital_db):
    """Ensure that closing the database connection works"""
    hospital_db.close_connection()
    with pytest.raises(Exception):
        hospital_db.cursor.execute("SELECT 1;")  # Should fail if connection is closed
