from flask import Blueprint, request, jsonify
from dependency_injector.wiring import Provide, inject
from app.models import (
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
    DepartmentResponseSchema,
)
from app.services.department_service import DepartmentService
from app.decorators import exception_handler
from app.di_container import ApplicationContainer

bp = Blueprint("department", __name__)

@bp.route("/departments", methods=["POST"])
@exception_handler
@inject
def add_department(department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    data = DepartmentCreateSchema(**request.json)
    department = department_service.add_department(data.name)
    response = DepartmentResponseSchema.model_validate(department)
    return jsonify(response.model_dump()), 201

@bp.route("/departments/<int:department_id>", methods=["PUT"])
@exception_handler
@inject
def update_department(department_id,
                      department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    data = DepartmentUpdateSchema(**request.json)
    department = department_service.update_department(department_id, data.name)
    response = DepartmentResponseSchema.model_validate(department)
    return jsonify(response.model_dump())

@bp.route("/departments", methods=["GET"])
@exception_handler
@inject
def get_all_departments(department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    departments = department_service.get_all_departments(with_relations=True)
    response = [DepartmentResponseSchema.model_validate(dep).model_dump() for dep in departments]
    return jsonify(response)

@bp.route("/departments/<int:department_id>", methods=["GET"])
@exception_handler
@inject
def get_department_by_id(department_id,
                         department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    department = department_service.get_department_by_id(department_id)
    response = DepartmentResponseSchema.model_validate(department)
    return jsonify(response.model_dump())

@bp.route("/departments/occupancy", methods=["GET"])
@exception_handler
@inject
def get_bed_occupancy(department_service: DepartmentService = Provide[ApplicationContainer.department_service]):
    occupancy_data = department_service.calculate_bed_occupancy()
    response = [data.dict() for data in occupancy_data]
    return jsonify(response)
