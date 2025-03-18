import pytest
from datetime import date
from datetime import datetime
from OrangeFinalBgd import (
    Person, Employee, Doctor, Patient, DataEntry, Manager, Nurse, Prescription ,PrescriptionFactory , HospitalDatabase
)

# ✅ Fixture for valid Person instance
@pytest.fixture
def valid_person():
    return Person(2001, "John Doe", 1990, "Male", "1234567890", "USA")

# ✅ Test Class for Person
class TestPerson:
    
    def test_person_creation(self, valid_person):
        """Test valid person creation"""
        person = valid_person
        assert person.id == 2001
        assert person.name == "John Doe"
        assert person.birth_year == 1990
        assert person.gender == "Male"
        assert person.phone_number == "1234567890"
        assert person.nationality == "USA"

    def test_invalid_person_missing_field(self):
        """Test missing required fields should raise ValueError"""
        with pytest.raises(ValueError):
            Person(None, "John Doe", 1990, "Male", "1234567890", "USA")

        with pytest.raises(ValueError):
            Person(2002, None, 1990, "Male", "1234567890", "USA")

        with pytest.raises(ValueError):
            Person(2003, "Jane Doe", None, "Female", "1234567890", "USA")

        with pytest.raises(ValueError):
            Person(2004, "John Doe", 1990, None, "1234567890", "USA")

        with pytest.raises(ValueError):
            Person(2005, "John Doe", 1990, "Male", None, "USA")

        with pytest.raises(ValueError):
            Person(2006, "John Doe", 1990, "Male", "1234567890", None)

    def test_invalid_birth_year(self):
        """Test invalid birth year should raise ValueError"""
        with pytest.raises(ValueError):
            Person(2007, "John Doe", -1990, "Male", "1234567890", "USA")

        with pytest.raises(ValueError):
            Person(2008, "John Doe", "1990", "Male", "1234567890", "USA")  # String instead of int

    def test_invalid_phone_number(self):
        """Test invalid phone numbers should raise ValueError"""
        with pytest.raises(ValueError):
            Person(2009, "John Doe", 1990, "Male", "123-456-7890", "USA")  # Hyphens not allowed

        with pytest.raises(ValueError):
            Person(2010, "John Doe", 1990, "Male", "12345abc90", "USA")  # Alphabetic characters not allowed

    def test_calculate_age(self, valid_person):
        """Test age calculation based on birth year"""
        person = valid_person
        current_year = date.today().year
        expected_age = current_year - person.birth_year
        assert person.calculate_age() == expected_age

    def test_display_info(self, valid_person, capsys):
        """Test person display info output"""
        valid_person.display_info()
        captured = capsys.readouterr()
        expected_output = f"ID: 2001, Name: John Doe, Age: {date.today().year - 1990}, Nationality: USA\n"
        assert captured.out == expected_output

# ✅ Fixture for valid DataEntry instance
@pytest.fixture
def valid_data_entry():
    return DataEntry(1001, "Alice Smith", 1990, "Female", "1234567890", 4000, "Records", "American")

@pytest.fixture
def valid_employee():
    return Manager(101, "Alice Johnson", 1980, "Female", "1234567890", 90000, "Administration", "American")

@pytest.fixture
def valid_doctor():
    return Doctor(301, "Dr. Emily Carter", 1985, "Female", "5551112222", "Canadian", 120000, "Surgery", "Neurosurgeon")

@pytest.fixture
def valid_nurse():
    return Nurse(202, "Mark Wilson", 1992, "Male", "9876543210", 50000, "ICU", "British", "Emergency Care")

@pytest.fixture
def valid_patient():
    return Patient(401, "John Smith", 1995, "Male", "4445556666", "American", ["Asthma"])


# ✅ Test DataEntry Methods
def test_data_entry_add_record(valid_data_entry, valid_person, capsys):
    """Test DataEntry add record method"""
    valid_data_entry.add_record(valid_person)
    captured = capsys.readouterr()
    assert f"Record added for: {valid_person.name}" in captured.out

def test_data_entry_delete_record(valid_data_entry, valid_person, capsys):
    """Test DataEntry delete record method"""
    valid_data_entry.delete_record(valid_person)
    captured = capsys.readouterr()
    assert f"Record deleted for: {valid_person.name}" in captured.out

def test_data_entry_delete_none(valid_data_entry):
    """Test DataEntry delete record method with None input"""
    with pytest.raises(ValueError):
        valid_data_entry.delete_record(None)

def test_data_entry_perform_duties(valid_data_entry, capsys):
    """Test DataEntry perform duties method"""
    valid_data_entry.perform_duties()
    captured = capsys.readouterr()
    assert "is managing data entries." in captured.out

def test_data_entry_display_info(valid_data_entry, capsys):
    """Test DataEntry display_info output"""
    valid_data_entry.display_info()
    captured = capsys.readouterr()
    assert "Alice Smith" in captured.out


# ✅ Test Manager Methods
def test_manager_creation(valid_employee):
    """Test Manager object creation"""
    assert valid_employee.id == 101
    assert valid_employee.name == "Alice Johnson"

def test_manager_perform_duties(valid_employee, capsys):
    """Test Manager perform duties method"""
    valid_employee.perform_duties()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Alice Johnson is managing the hospital."

def test_manager_display_info(valid_employee, capsys):
    """Test Manager display info output"""
    valid_employee.display_info()
    captured = capsys.readouterr()
    assert "Alice Johnson" in captured.out


# ✅ Test Nurse Methods
def test_nurse_assist_doctor(valid_nurse, valid_doctor, capsys):
    """Test Nurse assisting a Doctor"""
    valid_nurse.assist_doctor(valid_doctor)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Mark Wilson is assisting Dr. Emily Carter in a procedure."

def test_nurse_check_vitals(valid_nurse, valid_patient, capsys):
    """Test Nurse checking patient vitals"""
    valid_nurse.check_vitals(valid_patient)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Mark Wilson is checking vitals for John Smith."

def test_nurse_perform_duties(valid_nurse, capsys):
    """Test Nurse perform duties method"""
    valid_nurse.perform_duties()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Mark Wilson is taking care of patients."

def test_nurse_display_info(valid_nurse, capsys):
    """Test Nurse display info output"""
    valid_nurse.display_info()
    captured = capsys.readouterr()
    assert "Mark Wilson" in captured.out
    assert "Emergency Care" in captured.out  # Ensure specialty is printed


# ✅ Test prescription Methods
@pytest.fixture
def valid_prescription(valid_doctor, valid_patient):
    return Prescription(valid_doctor, valid_patient, "Amoxicillin")

# ✅ Test: Prescription Object Creation
def test_prescription_creation(valid_prescription):
    """Ensure a Prescription object is correctly initialized."""
    assert valid_prescription.doctor.name == "Dr. Emily Carter"
    assert valid_prescription.patient.name == "John Smith"
    assert valid_prescription.medication == "Amoxicillin"
    assert isinstance(valid_prescription.date_issued, datetime)

# ✅ Test: Invalid Prescription (Missing Fields)
@pytest.mark.parametrize("doctor, patient, medication, expected_exception", [
    (None, "valid_patient", "Paracetamol", ValueError),
    ("valid_doctor", None, "Paracetamol", ValueError),
    ("valid_doctor", "valid_patient", None, ValueError),
])
def test_invalid_prescription_missing_field(doctor, patient, medication, expected_exception, valid_doctor, valid_patient):
    """Ensure missing required fields raise ValueError."""
    with pytest.raises(expected_exception):
        Prescription(doctor if doctor != "valid_doctor" else valid_doctor,
                     patient if patient != "valid_patient" else valid_patient,
                     medication)

# ✅ Test: Invalid Prescription (Wrong Types)
@pytest.mark.parametrize("doctor, patient, medication, expected_exception", [
    ("Dr. Fake", "valid_patient", "Paracetamol", TypeError),
    ("valid_doctor", "John Doe", "Paracetamol", TypeError),
    ("valid_doctor", "valid_patient", "", ValueError),
])
def test_invalid_prescription_wrong_type(doctor, patient, medication, expected_exception, valid_doctor, valid_patient):
    """Ensure wrong data types raise TypeError or ValueError."""
    with pytest.raises(expected_exception):
        Prescription(doctor if doctor != "valid_doctor" else valid_doctor,
                     patient if patient != "valid_patient" else valid_patient,
                     medication)
        
# ✅ Test: Prescription Display Method
def test_prescription_display_info(valid_prescription, capsys):
    """Ensure display_prescription() prints correct output."""
    valid_prescription.display_prescription()
    captured = capsys.readouterr()
    assert "Prescription Details:" in captured.out
    assert "Dr. Emily Carter" in captured.out
    assert "John Smith" in captured.out
    assert "Amoxicillin" in captured.out

# ✅ Test: PrescriptionFactory Create Method
def test_prescription_factory(valid_doctor, valid_patient):
    """Ensure the factory correctly creates Prescription objects."""
    prescription = PrescriptionFactory.create_prescription(valid_doctor, valid_patient, "Ibuprofen")
    assert isinstance(prescription, Prescription)
    assert prescription.medication == "Ibuprofen"


# ✅ Test HospitalDatabase Methods
# ✅ Test: HospitalDatabase Singleton
def test_hospital_database_singleton():
    """Ensure HospitalDatabase follows singleton pattern."""
    db1 = HospitalDatabase()
    db2 = HospitalDatabase()
    assert db1 is db2  # Both instances should be the same

