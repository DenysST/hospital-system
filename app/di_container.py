import os
import logging
import google.generativeai as genai
from flask import Flask
from flask_mail import Mail
from dependency_injector.ext import flask
from dependency_injector import containers, providers
from app.repositories import DepartmentRepository, WardRepository, DoctorRepository, PatientRepository
from app.services.ai_service import GeminiService
from app.services.department_service import DepartmentService
from app.services.doctor_service import DoctorService
from app.services.notification_service import NotificationService
from app.services.patient_service import PatientService
from app.services.ward_service import WardService
from app.consts import GEMINI_MODEL


class ApplicationContainer(containers.DeclarativeContainer):
    app = flask.Application(Flask, __name__)

    # external services
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    genai_model_name = providers.Object(os.environ.get("GEMINI_MODEL", GEMINI_MODEL))
    generative_model = providers.Singleton(genai.GenerativeModel, genai_model_name)
    mail_provider = providers.Singleton(Mail, app)

    # repositories
    department_repository = providers.Singleton(DepartmentRepository)
    ward_repository = providers.Singleton(WardRepository)
    doctor_repository = providers.Singleton(DoctorRepository)
    patient_repository = providers.Singleton(PatientRepository)

    # services
    gemini_service = providers.Singleton(GeminiService, generative_model)
    notification_service = providers.Singleton(NotificationService, mail_provider)
    department_service = providers.Singleton(DepartmentService, department_repository)
    ward_service = providers.Singleton(WardService,ward_repository, department_repository)
    doctor_service = providers.Singleton(DoctorService, doctor_repository, department_repository)
    patient_service = providers.Singleton(PatientService, patient_repository, ward_repository,
                                          doctor_repository, department_repository,
                                          gemini_service, notification_service)

