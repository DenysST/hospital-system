from flask_smorest import Blueprint
from dependency_injector.wiring import Provide, inject
from app import ApplicationContainer
from app.services.ward_service import WardService
from app.models.schemas import WardCreateSchema, WardUpdateSchema, WardResponseSchema
from app.decorators import exception_handler

bp = Blueprint("ward", "ward", url_prefix="/wards")

@bp.route("", methods=["POST"])
@bp.arguments(WardCreateSchema)
@bp.response(201, WardResponseSchema)
@exception_handler
@inject
def add_ward(data, ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    return ward_service.add_ward(**data)

@bp.route("/<int:ward_id>", methods=["PUT"])
@bp.arguments(WardUpdateSchema)
@bp.response(200, WardResponseSchema)
@exception_handler
@inject
def update_ward(data, ward_id, ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    return ward_service.update_ward(ward_id, **data)

@bp.route("", methods=["GET"])
@bp.response(200, WardResponseSchema(many=True))
@exception_handler
@inject
def get_all_wards(ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    return ward_service.get_all_wards()

@bp.route("/<int:ward_id>", methods=["GET"])
@bp.response(200, WardResponseSchema)
@exception_handler
@inject
def get_ward_by_id(ward_id, ward_service: WardService = Provide[ApplicationContainer.ward_service]):
    return ward_service.get_ward_by_id(ward_id)
