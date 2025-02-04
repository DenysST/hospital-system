from flask_smorest import Blueprint
from dependency_injector.wiring import Provide, inject
from app.models import (
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
    DepartmentResponseSchema,
)
from app.services.department_service import DepartmentService
from app.decorators import exception_handler
from app.di_container import ApplicationContainer

bp = Blueprint("department", "department", url_prefix="/departments")

@bp.route("", methods=["POST"])
@bp.arguments(DepartmentCreateSchema)
@bp.response(201, DepartmentResponseSchema)
@exception_handler
@inject
def add_department(
        data, department_service: DepartmentService = Provide[ApplicationContainer.department_service]
):
    department = department_service.add_department(**data)
    return DepartmentResponseSchema().dump(department)

@bp.route("/<int:department_id>", methods=["PUT"])
@bp.arguments(DepartmentUpdateSchema)
@bp.response(200, DepartmentResponseSchema)
@exception_handler
@inject
def update_department(
        data, department_id,
        department_service: DepartmentService = Provide[ApplicationContainer.department_service]
):
    validated_data = DepartmentUpdateSchema().load(data)
    department = department_service.update_department(department_id, validated_data["name"])
    return department

@bp.route("", methods=["GET"])
@bp.response(200, DepartmentResponseSchema(many=True))
@exception_handler
@inject
def get_all_departments(department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    return department_service.get_all_departments(with_relations=True)

@bp.route("/<int:department_id>", methods=["GET"])
@bp.response(200, DepartmentResponseSchema)
@exception_handler
@inject
def get_department_by_id(
        department_id,
        department_service: DepartmentService = Provide[ApplicationContainer.department_service]
):
    return department_service.get_department_by_id(department_id)

@bp.route("/occupancy", methods=["GET"])
@bp.response(200, DepartmentResponseSchema(many=True))
@exception_handler
@inject
def get_bed_occupancy(department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    return department_service.calculate_bed_occupancy()
