import json
from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(...,description='ID of the patient',examples=['P001'])]
    name: Annotated[str, Field(...,description='Name of the patient',examples=['John Doe'])]
    city: Annotated[str, Field(...,description='City of the patient',examples=['New York'])]
    age: Annotated[int,  Field(...,gt=0,lt=120, description='Age of the patient',examples=[30])]
    gender: Annotated[Literal['Male','Female','Others'], Field(...,description='Gender of the patient',examples=['Male'])]
    height: Annotated[float, Field(...,gt=0, description='Height of the patient in meters')]
    weight: Annotated[float, Field(...,gt=0, description='Weight of the patient in kg')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi


    @computed_field
    @property
    def bmi_category(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"


# Update model
class UpdatePatient(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120)
    gender: Optional[Literal['Male','Female','Others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

#load data
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

# save data
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API built with FastAPI."}




@app.get("/view")
def view():
    data = load_data()
    return data

# PAth and Query parametre


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve",examples="P001")):
    #load all patient data from the JSON file
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")


@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="sort on the basis of height,weight,or bmi"),
    order: str = Query("asc",description="sort order, either asc or desc")):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter. Must be 'height', 'weight', or 'bmi'.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter. Must be 'asc' or 'desc'.")

    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists")
    data[patient.id] = patient.model_dump(exclude=['id']) # convert the Pydantic model to a dictionary

    #save the updated data back to the JSON file
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient: UpdatePatient):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update the patient data with the new values
    existing_patient_info = data[patient_id]
    updated_data = patient.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id  # Ensure the ID remains unchanged
    patient_obj = Patient(**existing_patient_info)  # Validate the updated data using the Patient model

    existing_patient_info = patient_obj.model_dump(exclude='id')  # Convert the Pydantic model to a dictionary, excluding the ID

    #add the dict to data
    data[patient_id] = existing_patient_info
    
    #save the updated data back to the JSON file
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Remove the patient from the data
    del data[patient_id]
    
    # Save the updated data back to the JSON file
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})