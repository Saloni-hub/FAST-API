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

# print(patient)
# print(patient.address.city)  # Accessing nested model attribute

temp = patient.model_dump()  # Serializing the Patient model to a dictionary

#include which needed
temp_include = patient.model_dump(include={'name', 'age'})  # Serializing only the 'name' and 'age' fields of the Patient model to a dictionary

temp_exclude = patient.model_dump(exclude={'address'})  # Serializing the Patient model to a dictionary while excluding the 'address' field

temp_exclude_nested = patient.model_dump(exclude={'address': {'zip_code'}})  # Serializing the Patient model to a dictionary while excluding the 'zip_code' field of the nested Address model

temp_json = patient.model_dump_json()  #serializing the Patient model to a JSON string


print(temp)  # Printing the serialized dictionary
# print(type(temp))  # Printing the type of the serialized dictionary
# print(temp_include)  # Printing the serialized dictionary with included fields
# print(temp_exclude)  # Printing the serialized dictionary with excluded fields
# print(temp_exclude_nested)  # Printing the serialized dictionary with excluded nested fields
# print(temp_json)  # Printing the serialized JSON string
# print(type(temp_json))  # Printing the type of the serialized JSON string