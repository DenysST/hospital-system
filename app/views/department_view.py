from flask import Blueprint, request, jsonify
from app.models import (
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
    DepartmentResponseSchema,
)
from app.services.department_service import DepartmentService
from app.decorators import exception_handler

bp = Blueprint("department", __name__)
department_service = DepartmentService()

@bp.route("/departments", methods=["POST"])
@exception_handler
def add_department():
    data = DepartmentCreateSchema(**request.json)
    department = department_service.add_department(data.name)
    response = DepartmentResponseSchema.from_orm(department)
    return jsonify(response.dict()), 201

@bp.route("/departments/<int:department_id>", methods=["PUT"])
@exception_handler
def update_department(department_id):
    data = DepartmentUpdateSchema(**request.json)
    department = department_service.update_department(department_id, data.name)
    response = DepartmentResponseSchema.from_orm(department)
    return jsonify(response.dict())

@bp.route("/departments", methods=["GET"])
@exception_handler
def get_all_departments():
    departments = department_service.get_all_departments(with_relations=True)
    response = [DepartmentResponseSchema.from_orm(dep).dict() for dep in departments]
    return jsonify(response)

@bp.route("/departments/<int:department_id>", methods=["GET"])
@exception_handler
def get_department_by_id(department_id):
    department = department_service.get_department_by_id(department_id)
    response = DepartmentResponseSchema.from_orm(department)
    return jsonify(response.dict())

@bp.route("/departments/occupancy", methods=["GET"])
@exception_handler
def get_bed_occupancy():
    occupancy_data = department_service.calculate_bed_occupancy()
    response = [data.dict() for data in occupancy_data]
    return jsonify(response)
