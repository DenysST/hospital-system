from flask import Blueprint, request, jsonify
from app.services.patient_service import PatientService
from app.models import PatientCreateSchema, PatientUpdateSchema, PatientResponseSchema
from app.decorators import exception_handler
from app import gemini_model

bp = Blueprint("patient", __name__)
patient_service = PatientService()

@bp.route("/patients", methods=["POST"])
@exception_handler
def add_patient():
    data = PatientCreateSchema(**request.json)
    patient = patient_service.add_patient(data.name, data.problem)
    response = PatientResponseSchema.from_orm(patient)
    return jsonify(response.dict()), 201

@bp.route("/patients/<int:patient_id>", methods=["PUT"])
@exception_handler
def update_patient(patient_id: int):
    data = PatientUpdateSchema(**request.json)
    patient = patient_service.update_patient(
        patient_id, **data.dict(exclude_unset=True)
    )
    response = PatientResponseSchema.from_orm(patient)
    return jsonify(response.dict())

@bp.route("/patients", methods=["GET"])
@exception_handler
def get_all_patients():
    patients = patient_service.get_all_patients()
    response = [PatientResponseSchema.from_orm(p).dict() for p in patients]
    return jsonify(response)

@bp.route("/patients/ward/<int:ward_id>", methods=["GET"])
@exception_handler
def get_patients_by_ward(ward_id: int):
    patients = patient_service.get_patients_by_ward(ward_id)
    response = [PatientResponseSchema.from_orm(p).dict() for p in patients]
    return jsonify(response)

@bp.route("/patients/doctor/<int:doctor_id>", methods=["GET"])
@exception_handler
def get_patients_by_doctor(doctor_id: int):
    patients = patient_service.get_patients_by_doctor(doctor_id)
    response = [PatientResponseSchema.from_orm(p).dict() for p in patients]
    return jsonify(response)

@bp.route("/patients/<int:patient_id>", methods=["GET"])
@exception_handler
def get_patient_by_id(patient_id: int):
    patient = patient_service.get_patient_by_id(patient_id)
    response = PatientResponseSchema.from_orm(patient)
    return jsonify(response.dict())

@bp.route("/patients/gemini", methods=["POST"])
@exception_handler
def add_gemini():
    data = request.json
    response = gemini_model.generate_content(data["prompt"])
    return jsonify({'response': response.text}), 201
