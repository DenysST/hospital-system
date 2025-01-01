from app.config import SingletonMeta
from app.models import Patient
from app.repositories import PatientRepository, WardRepository, DoctorRepository

class PatientService(metaclass=SingletonMeta):
    def __init__(self):
        self._patient_repository = PatientRepository()
        self._ward_repository = WardRepository()
        self._doctor_repository = DoctorRepository()

    def add_patient(self, name: str, problem: str):
        patient = Patient(
            name=name,
            problem=problem,
            ward_id=1,
            doctor_id=1
        )
        return self._patient_repository.add(patient)

    def update_patient(self, patient_id: int, name=None, problem=None, ward_id=None, doctor_id=None, start_date=None,
                       end_date=None):
        patient = self._patient_repository.get_by_id(patient_id)
        if not patient:
            raise ValueError("Patient not found.")

        self._validate_ward(ward_id)
        self._validate_doctor(doctor_id, ward_id)

        if name is not None:
            patient.name = name
        if problem is not None:
            patient.problem = problem
        if ward_id is not None:
            patient.ward_id = ward_id
        if doctor_id is not None:
            patient.doctor_id = doctor_id
        if start_date is not None:
            patient.start_date = start_date
        if end_date is not None:
            patient.end_date = end_date

        return self._patient_repository.update(patient)

    def get_patient_by_id(self, patient_id: int):
        patient = self._patient_repository.get_by_id(patient_id)
        if not patient:
            raise ValueError("Patient not found.")
        return patient

    def get_all_patients(self):
        return self._patient_repository.get_all()

    def get_patients_by_ward(self, ward_id: int):
        return self._patient_repository.get_by_ward(ward_id)

    def get_patients_by_doctor(self, doctor_id: int):
        return self._patient_repository.get_by_doctor(doctor_id)

    def _validate_doctor(self, doctor_id, ward_id):
        if doctor_id is not None:
            doctor = self._doctor_repository.get_by_id(doctor_id)
            if not doctor:
                raise ValueError("Doctor does not exist.")
            if ward_id is not None:
                ward = self._ward_repository.get_by_id(ward_id)
                if doctor.department_id != ward.department_id:
                    raise ValueError("Doctor must belong to the same department as the ward.")

    def _validate_ward(self, ward_id):
        if ward_id is not None:
            ward = self._ward_repository.get_by_id(ward_id)
            if not ward:
                raise ValueError("Ward does not exist.")
            if len(ward.patients) >= ward.bed_capacity:
                raise ValueError("Ward is full.")