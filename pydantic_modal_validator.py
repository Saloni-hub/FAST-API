from pydantic import BaseModel,EmailStr, model_validator
from typing import List, Dict

# model validator is used for custom validation of the entire model in pydantic. It allows you to define validation logic that applies to the entire model, rather than just individual fields. This can be useful for enforcing complex validation rules that depend on multiple fields or require access to the entire model instance.

class Patient(BaseModel):
    name:str
    email: EmailStr
    age:int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(self):
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError(
                "Emergency contact is required for patients over 60"
            )
        return self

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")


patient_info = {
    "name": "saloni",
    "email": "sp@hdfc.com",
    "age":'65',
    "weight": 65.5,
    "married": True,
    "allergies": ["peanuts", "shellfish"],
    "contact_details": {
        "phone": "123-456-7890",
        "address": "123 Main St",
        "emergency": "987-654-3210"
    
    }
}


patient = Patient(**patient_info)
update_patient(patient)