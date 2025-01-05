from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify
from app import ApplicationContainer
from app.services.patient_service import PatientService
from app.models import PatientCreateSchema, PatientUpdateSchema, PatientResponseSchema
from app.decorators import exception_handler

bp = Blueprint("patient", __name__)

@bp.route("/patients", methods=["POST"])
@exception_handler
@inject
def add_patient(patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    data = PatientCreateSchema(**request.json)
    patient = patient_service.add_patient(data.name, data.problem)
    response = PatientResponseSchema.model_validate(patient)
    return jsonify(response.model_dump()), 201

@bp.route("/patients/<int:patient_id>", methods=["PUT"])
@exception_handler
@inject
def update_patient(patient_id: int,
                   patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    data = PatientUpdateSchema(**request.json)
    patient = patient_service.update_patient(
        patient_id, **data.model_dump(exclude_unset=True)
    )
    response = PatientResponseSchema.model_validate(patient)
    return jsonify(response.model_dump())

@bp.route("/patients", methods=["GET"])
@exception_handler
@inject
def get_all_patients(patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    patients = patient_service.get_all_patients()
    response = [PatientResponseSchema.model_validate(p).model_dump() for p in patients]
    return jsonify(response)

@bp.route("/patients/ward/<int:ward_id>", methods=["GET"])
@exception_handler
@inject
def get_patients_by_ward(ward_id: int,
                         patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    patients = patient_service.get_patients_by_ward(ward_id)
    response = [PatientResponseSchema.model_validate(p).model_dump() for p in patients]
    return jsonify(response)

@bp.route("/patients/doctor/<int:doctor_id>", methods=["GET"])
@exception_handler
@inject
def get_patients_by_doctor(doctor_id: int,
                           patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    patients = patient_service.get_patients_by_doctor(doctor_id)
    response = [PatientResponseSchema.model_validate(p).model_dump() for p in patients]
    return jsonify(response)

@bp.route("/patients/<int:patient_id>", methods=["GET"])
@exception_handler
@inject
def get_patient_by_id(patient_id: int,
                      patient_service: PatientService = Provide[ApplicationContainer.patient_service]):
    patient = patient_service.get_patient_by_id(patient_id)
    response = PatientResponseSchema.model_validate(patient)
    return jsonify(response.model_dump())
