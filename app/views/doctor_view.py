from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify

from app import ApplicationContainer
from app.services.doctor_service import DoctorService
from app.models import DoctorCreateSchema, DoctorUpdateSchema, DoctorResponseSchema
from app.decorators import exception_handler

bp = Blueprint("doctor", __name__)

@bp.route("/doctors", methods=["POST"])
@exception_handler
@inject
def add_doctor(doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    data = DoctorCreateSchema(**request.json)
    doctor = doctor_service.add_doctor(data.name, data.specialization, data.department_id)
    response = DoctorResponseSchema.model_validate(doctor)
    return jsonify(response.model_dump()), 201

@bp.route("/doctors/<int:doctor_id>", methods=["PUT"])
@exception_handler
@inject
def update_doctor(doctor_id: int,
                  doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    data = DoctorUpdateSchema(**request.json)
    doctor = doctor_service.update_doctor(doctor_id, **data.model_dump(exclude_unset=True))
    response = DoctorResponseSchema.model_validate(doctor)
    return jsonify(response.model_dump())

@bp.route("/doctors", methods=["GET"])
@exception_handler
@inject
def get_all_doctors(doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    doctors = doctor_service.get_all_doctors()
    response = [DoctorResponseSchema.model_validate(doc).model_dump() for doc in doctors]
    return jsonify(response)

@bp.route("/doctors/<int:doctor_id>", methods=["GET"])
@exception_handler
@inject
def get_doctor_by_id(doctor_id: int,
                     doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    response = DoctorResponseSchema.model_validate(doctor)
    return jsonify(response.model_dump())

@bp.route("/doctors/department/<int:department_id>", methods=["GET"])
@exception_handler
@inject
def get_doctors_by_department(department_id: int,
                              doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    doctors = doctor_service.get_doctors_by_department(department_id)
    response = [DoctorResponseSchema.model_validate(doc).model_dump() for doc in doctors]
    return jsonify(response)
