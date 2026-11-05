from pydantic import BaseModel,EmailStr, computed_field, model_validator
from typing import List, Dict


class Patient(BaseModel):
    name:str
    email: EmailStr
    age:int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        height_in_meters = 1.65  # Example height in meters
        bmi = self.weight / (height_in_meters ** 2)
        return round(bmi, 2)

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(f"Calculated BMI: {patient.calculate_bmi}")
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