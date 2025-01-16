from flask_smorest import Blueprint
from dependency_injector.wiring import Provide, inject
from app import ApplicationContainer
from app.services.doctor_service import DoctorService
from app.models.schemas import DoctorCreateSchema, DoctorUpdateSchema, DoctorResponseSchema
from app.decorators import exception_handler

bp = Blueprint("doctor", "doctor", url_prefix="/doctors")

@bp.route("/", methods=["POST"])
@bp.arguments(DoctorCreateSchema)
@bp.response(201, DoctorResponseSchema)
@exception_handler
@inject
def add_doctor(data, doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    doctor = DoctorResponseSchema(**data)
    return doctor_service.add_doctor(doctor.name, doctor.specialization, doctor.department_id)

@bp.route("/<int:doctor_id>", methods=["PUT"])
@bp.arguments(DoctorUpdateSchema)
@bp.response(200, DoctorResponseSchema)
@exception_handler
@inject
def update_doctor(data, doctor_id, doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    return doctor_service.update_doctor(doctor_id, **data)

@bp.route("/", methods=["GET"])
@bp.response(200, DoctorResponseSchema(many=True))
@exception_handler
@inject
def get_all_doctors(doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    return doctor_service.get_all_doctors()

@bp.route("/<int:doctor_id>", methods=["GET"])
@bp.response(200, DoctorResponseSchema)
@exception_handler
@inject
def get_doctor_by_id(doctor_id, doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    return doctor_service.get_doctor_by_id(doctor_id)

@bp.route("/department/<int:department_id>", methods=["GET"])
@bp.response(200, DoctorResponseSchema(many=True))
@exception_handler
@inject
def get_doctors_by_department(department_id,
                              doctor_service: DoctorService = Provide[ApplicationContainer.doctor_service]):
    return doctor_service.get_doctors_by_department(department_id)
