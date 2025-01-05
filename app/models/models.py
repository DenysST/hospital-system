from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    wards = relationship("Ward", back_populates="department", cascade="all, delete-orphan")
    doctors = relationship("Doctor", back_populates="department", cascade="all, delete-orphan")


class Ward(db.Model):
    __tablename__ = 'wards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False, unique=True)
    bed_capacity = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)

    department = relationship("Department", back_populates="wards")
    patients = relationship("Patient", back_populates="ward", cascade="all, delete-orphan")


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)

    department = relationship("Department", back_populates="doctors")
    patients = relationship("Patient", back_populates="doctor")


class Patient(db.Model):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    problem = Column(Text, nullable=False)
    ward_id = Column(Integer, ForeignKey("wards.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    hospitalisation_start_date = Column(DateTime, nullable=True)
    hospitalisation_end_date = Column(DateTime, nullable=True)

    ward = relationship("Ward", back_populates="patients")
    doctor = relationship("Doctor", back_populates="patients")
