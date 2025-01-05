from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class WardCreateSchema(BaseModel):
    number: int = Field(..., ge=1, description="Ward number must be a positive integer")
    bed_capacity: int = Field(..., ge=1, description="Ward capacity must be a positive integer")
    department_id: int = Field(..., ge=1, description="Department ID must be a positive integer")


class WardUpdateSchema(BaseModel):
    number: Optional[int] = Field(None, ge=1, description="Ward number must be a positive integer")
    bed_capacity: Optional[int] = Field(None, ge=1, description="Ward capacity must be a positive integer")
    department_id: Optional[int] = Field(None, ge=1, description="Department ID must be a positive integer")


class WardResponseSchema(BaseModel):
    id: int
    number: int
    bed_capacity: int
    department_id: int

    class Config:
        from_attributes=True


class DoctorCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the doctor")
    specialization: str = Field(..., min_length=1, max_length=100, description="Specialization of the doctor")
    department_id: int = Field(..., ge=1, description="ID of the associated department")


class DoctorUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated name of the doctor")
    specialization: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated specialization")
    department_id: Optional[int] = Field(None, ge=1, description="Updated department ID")


class DoctorResponseSchema(BaseModel):
    id: int
    name: str
    specialization: str
    department_id: int
    email: str

    class Config:
        from_attributes=True


class PatientCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the patient")
    problem: str = Field(..., min_length=1, description="Description of the patient's problem")


class PatientUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated name of the patient")
    problem: Optional[str] = Field(None, min_length=1, description="Updated problem description")
    ward_id: Optional[int] = Field(None, ge=1, description="Updated ward ID")
    doctor_id: Optional[int] = Field(None, ge=1, description="Updated doctor ID")
    end_date: Optional[datetime] = None


class PatientResponseSchema(BaseModel):
    id: int
    name: str
    problem: str
    ward_id: int
    doctor_id: int
    hospitalisation_start_date: Optional[datetime]
    hospitalisation_end_date: Optional[datetime]

    class Config:
        from_attributes=True


class DepartmentCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the department")


class DepartmentUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Updated name of the department")


class DepartmentResponseSchema(BaseModel):
    id: int
    name: str
    wards: list[WardResponseSchema]
    doctors: list[DoctorResponseSchema]

    class Config:
        from_attributes=True

class DepartmentOccupancySchema(BaseModel):
    department_id: int = Field(..., description="Unique identifier for the department")
    department_name: str = Field(..., description="Name of the department")
    total_beds: int = Field(..., ge=0, description="Total number of beds in the department")
    occupied_beds: int = Field(..., ge=0, description="Number of beds currently occupied in the department")
    occupancy_percentage: float = Field(..., ge=0, le=100, description="Percentage of beds occupied in the department")
