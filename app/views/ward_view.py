from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify
from app import ApplicationContainer
from app.services.ward_service import WardService
from app.models import WardCreateSchema, WardUpdateSchema, WardResponseSchema
from app.decorators import exception_handler

bp = Blueprint("ward", __name__)

@bp.route("/wards", methods=["POST"])
@exception_handler
@inject
def add_ward(ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    data = WardCreateSchema(**request.json)
    ward = ward_service.add_ward(data.number, data.bed_capacity, data.department_id)
    response = WardResponseSchema.model_validate(ward)
    return jsonify(response.model_dump()), 201

@bp.route("/wards/<int:ward_id>", methods=["PUT"])
@exception_handler
@inject
def update_ward(ward_id: int, ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    data = WardUpdateSchema(**request.json)
    ward = ward_service.update_ward(ward_id, **data.model_dump(exclude_unset=True))
    response = WardResponseSchema.model_validate(ward)
    return jsonify(response.model_dump())

@bp.route("/wards", methods=["GET"])
@exception_handler
@inject
def get_all_wards(ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    wards = ward_service.get_all_wards()
    response = [WardResponseSchema.model_validate(ward).model_dump() for ward in wards]
    return jsonify(response)

@bp.route("/wards/<int:ward_id>", methods=["GET"])
@exception_handler
@inject
def get_ward_by_id(ward_id: int, ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    ward = ward_service.get_ward_by_id(ward_id)
    response = WardResponseSchema.model_validate(ward)
    return jsonify(response.model_dump())
