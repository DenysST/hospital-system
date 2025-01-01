from flask import Blueprint, request, jsonify
from app.services.doctor_service import DoctorService
from app.models import DoctorCreateSchema, DoctorUpdateSchema, DoctorResponseSchema
from app.decorators import exception_handler

bp = Blueprint("doctor", __name__)
doctor_service = DoctorService()

@bp.route("/doctors", methods=["POST"])
@exception_handler
def add_doctor():
    data = DoctorCreateSchema(**request.json)
    doctor = doctor_service.add_doctor(data.name, data.specialization, data.department_id)
    response = DoctorResponseSchema.from_orm(doctor)
    return jsonify(response.dict()), 201

@bp.route("/doctors/<int:doctor_id>", methods=["PUT"])
@exception_handler
def update_doctor(doctor_id: int):
    data = DoctorUpdateSchema(**request.json)
    doctor = doctor_service.update_doctor(doctor_id, **data.dict(exclude_unset=True))
    response = DoctorResponseSchema.from_orm(doctor)
    return jsonify(response.dict())

@bp.route("/doctors", methods=["GET"])
@exception_handler
def get_all_doctors():
    doctors = doctor_service.get_all_doctors()
    response = [DoctorResponseSchema.from_orm(doc).dict() for doc in doctors]
    return jsonify(response)

@bp.route("/doctors/<int:doctor_id>", methods=["GET"])
@exception_handler
def get_doctor_by_id(doctor_id: int):
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    response = DoctorResponseSchema.from_orm(doctor)
    return jsonify(response.dict())

@bp.route("/doctors/department/<int:department_id>", methods=["GET"])
@exception_handler
def get_doctors_by_department(department_id: int):
    doctors = doctor_service.get_doctors_by_department(department_id)
    response = [DoctorResponseSchema.from_orm(doc).dict() for doc in doctors]
    return jsonify(response)
