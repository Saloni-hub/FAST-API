from pydantic import BaseModel, Field,EmailStr, field_validator
from typing import List, Dict, Optional, Annotated

# field validator used fo custom validation of fields in pydantic models. It allows you to define validation logic for specific fields in your model, ensuring that the data meets certain criteria before it is accepted.

class Patient(BaseModel):
    name:str
    email: EmailStr
    age:int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator ('email')
    @classmethod
    def email_validator(cls, value):
        valid_domain = ['hdfc.com','icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        return value

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        return value.upper()


    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value <100:
            return value
        else:
            raise ValueError("Age must be between 0 and 100")

    

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")


patient_info = {
    "name": "saloni",
    "email": "sp@hdfc.com",
    "age":'29',
    "weight": 65.5,
    "married": True,
    "allergies": ["peanuts", "shellfish"],
    "contact_details": {
        "phone": "123-456-7890",
        "address": "123 Main St"
    }
}


patient = Patient(**patient_info)
update_patient(patient)