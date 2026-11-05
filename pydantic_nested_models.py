from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address

address_city = {'city': 'New York', 'state': 'NY', 'zip_code': '10001', 'street': '123 Main St'}

address = Address(**address_city)

patient_info = {
    "name": "John Doe",
    "gender": "Male",
    "age": 30,
    "address": address
}

patient = Patient(**patient_info)

print(patient)
print(patient.address.city)  # Accessing nested model attribute