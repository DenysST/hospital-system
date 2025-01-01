from flask import Blueprint, request, jsonify
from injector import inject
from app.services.ward_service import WardService
from app.models import WardCreateSchema, WardUpdateSchema, WardResponseSchema
from app.decorators import exception_handler

bp = Blueprint("ward", __name__)
ward_service = WardService()

@bp.route("/wards", methods=["POST"])
@exception_handler
def add_ward():
    data = WardCreateSchema(**request.json)
    ward = ward_service.add_ward(data.number, data.bed_capacity, data.department_id)
    response = WardResponseSchema.from_orm(ward)
    return jsonify(response.dict()), 201

@bp.route("/wards/<int:ward_id>", methods=["PUT"])
@exception_handler
def update_ward(ward_id: int):
    data = WardUpdateSchema(**request.json)
    ward = ward_service.update_ward(ward_id, **data.dict(exclude_unset=True))
    response = WardResponseSchema.from_orm(ward)
    return jsonify(response.dict())

@bp.route("/wards", methods=["GET"])
@exception_handler
def get_all_wards():
    wards = ward_service.get_all_wards()
    response = [WardResponseSchema.from_orm(ward).dict() for ward in wards]
    return jsonify(response)

@bp.route("/wards/<int:ward_id>", methods=["GET"])
@exception_handler
@inject
def get_ward_by_id(ward_id: int):
    ward = ward_service.get_ward_by_id(ward_id)
    response = WardResponseSchema.from_orm(ward)
    return jsonify(response.dict())
