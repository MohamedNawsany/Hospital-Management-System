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


# Doctor class
class Doctor(Employee):
    def __init__(self, id, name, birth_year, gender, phone_number, nationality, salary, department, specialization):
        """Initialize Doctor with required fields."""
        # Ensure all required fields are provided
        if not all([id, name, birth_year, gender, phone_number, nationality, salary, department, specialization]):
            raise ValueError("❌ All fields are required and cannot be None or empty.")

        if not isinstance(salary, (int, float)) or salary <= 0:
            raise ValueError("❌ Salary must be a positive number.")

        # Corrected order for super().__init__()
        super().__init__(id, name, birth_year, gender, phone_number, nationality, salary, department)
        
        self.specialization = specialization
    
    def diagnose_patient(self):
        print(f"👨‍⚕️ {self.name} is diagnosing a patient.")
    
    def write_prescription(self, patient, medication):
        if not isinstance(medication, str) or not medication.strip():
            raise ValueError("❌ Medication must be a non-empty string.")

        if not isinstance(patient, Patient):
            raise TypeError("❌ Invalid patient object.")

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
        # Ensure all required fields are provided
        if not all([id, name, birth_year, gender, phone_number, nationality, medical_history]):
            raise ValueError("All fields are required and cannot be None or empty.")

        if not isinstance(medical_history, list):
            raise TypeError("Medical history must be a list.")

        # Call parent constructor
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
        """Logs the printing of a prescription in the database."""
        print(f"Printing prescription {prescription_id}...")

        db = HospitalDatabase()  # Get the Singleton instance
        try:
            sql = """
            INSERT INTO PrintedPrescriptions (prescription_id, data_entry_id, printed_at)
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

        # Call parent constructor
        super().__init__(id, name, birth_year, gender, phone_number, nationality, salary, department)

    def perform_duties(self):
        print(f"{self.name} is managing the hospital.")

    def display_info(self):
        super().display_info()


class Nurse(Employee):
    def __init__(self, id, name, birth_year, gender, phone_number, salary, department, nationality, specialty):
     
        # Call parent constructor
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
        # Ensure all required fields are provided
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

    def display_prescription(self):
        print(f"Prescription Details:\nDoctor: {self.doctor.name}\nPatient: {self.patient.name}\nMedication: {self.medication}\nDate Issued: {self.date_issued}")


# Factory class for creating prescriptions
class PrescriptionFactory:
    @staticmethod
    def create_prescription(doctor, patient, medication):
     if not isinstance(doctor, Doctor):
        raise TypeError("Doctor must be an instance of Doctor class.")
     if not isinstance(patient, Patient):
        raise TypeError("Patient must be an instance of Patient class.")
     return Prescription(doctor, patient, medication)

# Singleton class for database management

import mysql.connector

class HospitalDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HospitalDatabase, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Establish connection to MySQL database"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="OrangeFinal"
            )
            self.cursor = self.conn.cursor()
            print("✅ Database connection established.")
        except mysql.connector.Error as e:
            print(f"❌ Database connection failed: {e}")

    def check_connection(self):
        """Check if the database connection is active"""
        if self.conn.is_connected():
            print("✅ Connection is active.")
        else:
            print("❌ Connection lost. Reconnecting...")
            self._connect()

    def insert_data(self, table, data):
        """Insert data into the specified table"""
        try:
            if table == "manager":
                query = "INSERT INTO manager (id) VALUES (%s)"
            elif table == "nurse":
                query = "INSERT INTO nurse (id, specialty) VALUES (%s, %s)"
            elif table == "data_entry":
                query = "INSERT INTO data_entry (id) VALUES (%s)"
            elif table == "doctor":
                query = "INSERT INTO doctor (id, specialization, name) VALUES (%s, %s, %s)"
            elif table == "employee":
                query = """INSERT INTO employee 
                        (id, name, birth_year, gender, phone_number, salary, department,nationality) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            elif table == "patient":
                query = """INSERT INTO patient 
                        (id, name, birth_year, gender, phone_number, nationality, medical_history) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            elif table == "prescription":
                query = """INSERT INTO prescription 
                        (id, doctor_id, patient_id, medication, date_issued) 
                        VALUES (%s, %s, %s, %s, %s)"""
            elif table == "printed_prescriptions":
                query = """INSERT INTO printed_prescriptions 
                        (id, prescription_id, data_entry_id, printed_at) 
                        VALUES (%s, %s, %s, %s)"""
            else:
                raise ValueError(f"❌ Table '{table}' not recognized.")

            self.cursor.execute(query, data)
            self.conn.commit()
            print(f"✅ Inserted into {table}: {data}")
        except mysql.connector.Error as e:
            print(f"❌ Insert failed: {e}")
        except ValueError as ve:
            print(ve)

    def fetch_data(self, table):
        """Fetch data from the specified table."""
        try:
            # Fetch the column names from the table
            self.cursor.execute(f"SHOW COLUMNS FROM {table}")
            columns = [col[0] for col in self.cursor.fetchall()]
            print(f"\n📋 {table} Table Data:")
            print(", ".join(columns))  # Print column headers

            # Fetch all rows from the table
            self.cursor.execute(f"SELECT * FROM {table}")
            rows = self.cursor.fetchall()

            if rows:
                for row in rows:
                    row_data = dict(zip(columns, row))  # Combine column names with row values
                    print(row_data)  # Print the row as a dictionary
            else:
                print(f"ℹ️ No data found in {table}.")
        except mysql.connector.Error as e:
            print(f"❌ Fetch failed: {e}")

    def close_connection(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()
        print("🔒 Database connection closed.")

def main():
    print("🏥 Hospital System Testing...\n")


# ✅ 1. Test `Person` Class (via `Employee` and `Patient`)
    print("\n🔹 Testing Person Class Inheritance\n")
    try:
        person = Person(id=10, name="John Doe", birth_year=1990, gender="Male", phone_number="1234567890", nationality="USA")
        person.display_info()
    except ValueError as e:
        print(f"❌ Error: {e}")

# ✅ 2. Test `Doctor` as an Employee
    print("\n🔹 Testing Employee (Using Doctor Subclass)\n")
    try:
        doctor = Doctor(
            id=2,
            name="Jane Doe",
            birth_year=1987,
            gender="Female",
            phone_number="0987654321",
            nationality="Canadian",
            salary=80000,
            department="Cardiology",
            specialization="Cardiologist"
        )
        doctor.display_info()  # ✅ Should display all doctor details
        doctor.perform_duties()  # ✅ Should print "🩺 Jane Doe is treating patients."
    except ValueError as e:
        print(f"❌ Error: {e}")

    # ✅ Creating a Doctor
    doctor = Doctor(
        id=516, 
        name="Dr. Ahmed", 
        birth_year=1985, 
        gender="Male", 
        phone_number="1234567890", 
        nationality="Egyptian", 
        salary=50000, 
        department="Cardiology", 
        specialization="Heart Specialist"
    )
    
    # ✅ Creating a Patient
    patient = Patient(
        id=515, 
        name="Ali Hassan", 
        birth_year=1995, 
        gender="Male", 
        phone_number="0987654321", 
        nationality="Egyptian", 
        medical_history=["Diabetes", "High Blood Pressure"]
    )

    # ✅ Creating a Manager
    manager = Manager(
        id=55,
        name="Sara Mohamed",
        birth_year=1980,
        gender="Female",
        phone_number="1122334455",
        nationality="Egyptian",
        salary=70000,
        department="Administration"
    )

    # ✅ Creating a Nurse
    nurse = Nurse(
        id=510,
        name="Mona Tarek",
        birth_year=1990,
        gender="Female",
        phone_number="2233445566",
        nationality="Egyptian",
        salary=30000,
        department="ICU",
        specialty="Emergency Care"
    )

    # ✅ Doctor Writes a Prescription
    doctor.write_prescription(patient, "Aspirin")
    
    # ✅ Displaying Info for All
    print("\n🔎 Displaying Info:\n")
    doctor.display_info()
    patient.display_info()
    manager.display_info()
    nurse.display_info()

    # ✅ Fetching Prescriptions for Patient
    print("\n📜 Prescriptions for Patient:")
    for prescription in patient.prescriptions:
        prescription.display_prescription()

    # ✅ Doctor Diagnosing Patient
    doctor.diagnose_patient()

    # ✅ Nurse Assisting Doctor
    nurse.assist_doctor(doctor)

    # ✅ Nurse Checking Patient's Vitals
    nurse.check_vitals(patient)

    # ✅ Manager Performing Duties
    manager.perform_duties()

    print("\n✅ All tests passed successfully!")



def main2():
    db = HospitalDatabase()

    # Insert employees for all roles (ensure IDs exist)
    employees = [
        (1, "John Doe", 1985, "Male", "1234567890", 60000, "Cardiology", "USA"),  # Doctor
        (2, "Jane Manager", 1980, "Female", "9876543210", 70000, "Management", "UK"),  # Manager
        (3, "Alice Nurse", 1990, "Female", "4567891230", 50000, "Pediatrics", "France"),  # Nurse
        (4, "David Entry", 1995, "Male", "3216549870", 45000, "Admin", "Germany"),  # Data Entry
    ]
    for emp in employees:
        db.insert_data("employee", emp)

    # Insert into doctor (must match an employee ID)
    db.insert_data("doctor", (1, "Cardiologist", "Dr. Alice"))

    # Insert into manager, nurse, and data_entry (matching employee IDs)
    db.insert_data("manager", (2,))
    db.insert_data("nurse", (3, "Pediatrics"))
    db.insert_data("data_entry", (4,))

    # Insert into patient
    db.insert_data("patient", (5, "Jane Smith", 1992, "Female", "0987654321", "Canada", "Diabetes"))

    # Insert into prescription (must reference existing doctor and patient IDs)
    db.insert_data("prescription", (6, 1, 5, "Aspirin", "2025-03-17"))

    # Insert into printed_prescriptions (must reference existing prescription and data_entry IDs)
    db.insert_data("printed_prescriptions", (7, 6, 4, "2025-03-17 10:30:00"))

    # Fetch all table data
    tables = ["employee", "doctor", "manager", "nurse", "data_entry", "patient", "prescription", "printed_prescriptions"]
    for table in tables:
        db.fetch_data(table)

    # Close connection
    db.close_connection()

if __name__ == "__main__":
    main()
    main2()

