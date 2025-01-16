from flask_smorest import Blueprint
from dependency_injector.wiring import Provide, inject
from app import ApplicationContainer
from app.services.patient_service import PatientService
from app.models.schemas import PatientCreateSchema, PatientUpdateSchema, PatientResponseSchema
from app.decorators import exception_handler

bp = Blueprint("patient", "patient", url_prefix="/patients")

@bp.route("/", methods=["POST"])
@bp.arguments(PatientCreateSchema)
@bp.response(201, PatientResponseSchema)
@exception_handler
@inject
def add_patient(data, patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    patient = PatientCreateSchema(**data)
    return patient_service.add_patient(patient.name, patient.problem)

@bp.route("/<int:patient_id>", methods=["PUT"])
@bp.arguments(PatientUpdateSchema)
@bp.response(200, PatientResponseSchema)
@exception_handler
@inject
def update_patient(data, patient_id, patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    return patient_service.update_patient(patient_id, **data)

@bp.route("/", methods=["GET"])
@bp.response(200, PatientResponseSchema(many=True))
@exception_handler
@inject
def get_all_patients(patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    return patient_service.get_all_patients()

@bp.route("/ward/<int:ward_id>", methods=["GET"])
@bp.response(200, PatientResponseSchema(many=True))
@exception_handler
@inject
def get_patients_by_ward(ward_id, patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    return patient_service.get_patients_by_ward(ward_id)

@bp.route("/doctor/<int:doctor_id>", methods=["GET"])
@bp.response(200, PatientResponseSchema(many=True))
@exception_handler
@inject
def get_patients_by_doctor(doctor_id, patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    return patient_service.get_patients_by_doctor(doctor_id)

@bp.route("/<int:patient_id>", methods=["GET"])
@bp.response(200, PatientResponseSchema)
@exception_handler
@inject
def get_patient_by_id(patient_id, patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    return patient_service.get_patient_by_id(patient_id)
