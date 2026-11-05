from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            title="Name of the patient",
            description="Name must be between 1 and 50 characters",
            examples=["Saloni", "Shivani"],
        ),
    ]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(
        gt=0,
        le=120,
        description="Age must be greater than zero and less than or equal to 120",
    )
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[
        bool, Field(default=None, description="Marital status of the patient")
    ]
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]


def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted")


def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")


patient_info = {
    "name": "saloni",
    "email": "saloni@gmail.com",
    "linkedin_url": "https://www.linkedin.com/in/saloni",
    "age": 30,
    "weight": 61.0,
    "married": True,
    "allergies": ["peanuts"],
    "contact_details": {"email": "saloni@example.com", "phone": "123-456-7890"},
}
patient1 = Patient(**patient_info)

# insert_patient(patient1)
update_patient(patient1)
