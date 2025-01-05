from datetime import datetime, timedelta
from app.models import Patient
from app.repositories import PatientRepository, WardRepository, DoctorRepository, DepartmentRepository
from app.consts import DEPARTMENT, UNKNOWN_DEPARTMENT, PLANED_HOSPITALISATION_DAYS
from app.services.ai_service import GeminiService
from app.services.notification_service import NotificationService
from app.consts import EMAIL_SUBJECT, EMAIL_BODY


class PatientService:
    def __init__(self, patient_repository: PatientRepository, ward_repository: WardRepository,
                 doctor_repository: DoctorRepository, department_repository: DepartmentRepository,
                 gemini_service: GeminiService, notification_service: NotificationService):
        self._patient_repository = patient_repository
        self._ward_repository = ward_repository
        self._doctor_repository = doctor_repository
        self._department_repository = department_repository
        self._gemini_service = gemini_service
        self._notification_service = notification_service


    def add_patient(self, name: str, problem: str):
        assignment = self._gemini_service.get_assigment(problem)
        if not assignment or assignment[DEPARTMENT] == UNKNOWN_DEPARTMENT:
            raise ValueError("Invalid patient problem. Cannot assign to a department.")
        department = self._department_repository.get_by_name(assignment[DEPARTMENT])
        available_doctor = min(department.doctors, key=lambda d: len(d.patients))
        available_ward = min(department.wards, key=lambda w: len(w.patients))
        end_hospitalisation_date = datetime.now() + timedelta(days=assignment[PLANED_HOSPITALISATION_DAYS])
        patient = Patient(
            name=name,
            problem=problem,
            ward_id=available_ward.id,
            doctor_id=available_doctor.id,
            hospitalisation_start_date=datetime.now(),
            hospitalisation_end_date=end_hospitalisation_date
        )
        created_patient = self._patient_repository.add(patient)
        self._notification_service.send_email(
            "dinis1994@gmail.com",
            EMAIL_SUBJECT,
            EMAIL_BODY.format(created_patient=created_patient, name=name, problem=problem))
        return created_patient

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
            patient.hospitalisation_start_date = start_date
        if end_date is not None:
            patient.hospitalisation_end_date = end_date

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