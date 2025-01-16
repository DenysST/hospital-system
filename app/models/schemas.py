from marshmallow import Schema, fields, validate

class WardCreateSchema(Schema):
    number = fields.Int(required=True, validate=validate.Range(min=1),
                        description="Ward number must be a positive integer")
    bed_capacity = fields.Int(required=True, validate=validate.Range(min=1),
                              description="Ward capacity must be a positive integer")
    department_id = fields.Int(required=True, validate=validate.Range(min=1),
                               description="Department ID must be a positive integer")

class WardUpdateSchema(Schema):
    number = fields.Int(validate=validate.Range(min=1), description="Ward number must be a positive integer")
    bed_capacity = fields.Int(validate=validate.Range(min=1), description="Ward capacity must be a positive integer")
    department_id = fields.Int(validate=validate.Range(min=1), description="Department ID must be a positive integer")

class WardResponseSchema(Schema):
    id = fields.Int(required=True)
    number = fields.Int(required=True)
    bed_capacity = fields.Int(required=True)
    department_id = fields.Int(required=True)

class DoctorCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100), description="Name of the doctor")
    specialization = fields.String(required=True, validate=validate.Length(min=1, max=100),
                                   description="Specialization of the doctor")
    department_id = fields.Int(required=True, validate=validate.Range(min=1),
                               description="ID of the associated department")

class DoctorUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=100), description="Updated name of the doctor")
    specialization = fields.String(validate=validate.Length(min=1, max=100), description="Updated specialization")
    department_id = fields.Int(validate=validate.Range(min=1), description="Updated department ID")

class DoctorResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    specialization = fields.String(required=True)
    department_id = fields.Int(required=True)
    email = fields.String(validate=validate.Email(), allow_none=True)

class PatientCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100), description="Name of the patient")
    problem = fields.String(required=True, validate=validate.Length(min=1),
                            description="Description of the patient's problem")

class PatientUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=100), description="Updated name of the patient")
    problem = fields.String(validate=validate.Length(min=1), description="Updated problem description")
    ward_id = fields.Int(validate=validate.Range(min=1), description="Updated ward ID")
    doctor_id = fields.Int(validate=validate.Range(min=1), description="Updated doctor ID")
    end_date = fields.DateTime(allow_none=True)

class PatientResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    problem = fields.String(required=True)
    ward_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    hospitalisation_start_date = fields.DateTime(allow_none=True)
    hospitalisation_end_date = fields.DateTime(allow_none=True)

class DepartmentCreateSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        description="Name of the department"
    )

class DepartmentUpdateSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        description="Updated name of the department"
    )

class DepartmentResponseSchema(Schema):
    id = fields.Int(required=True, description="Unique identifier for the department")
    name = fields.String(required=True, description="Name of the department")
    wards = fields.List(
        fields.Nested("WardResponseSchema"),
        required=True,
        description="List of wards in the department"
    )
    doctors = fields.List(
        fields.Nested("DoctorResponseSchema"),
        required=True,
        description="List of doctors in the department"
    )

class DepartmentOccupancySchema(Schema):
    department_id = fields.Int(
        required=True,
        description="Unique identifier for the department"
    )
    department_name = fields.String(
        required=True,
        description="Name of the department"
    )
    total_beds = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        description="Total number of beds in the department"
    )
    occupied_beds = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        description="Number of beds currently occupied in the department"
    )
    occupancy_percentage = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=100),
        description="Percentage of beds occupied in the department"
    )
