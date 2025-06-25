from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Health Checkup Decision API", version="1.0.0")

class PatientData(BaseModel):
    bmi: float = Field(..., description="Body Mass Index", ge=0)
    age: int = Field(..., description="Age in years", ge=0, le=200)

class DecisionResponse(BaseModel):
    decision: str
    plan: str
    doctor: str
    thai_message: str

def get_health_checkup_decision(bmi: float, age: int) -> DecisionResponse:
    """
    Determine health checkup plan based on BMI and age according to the decision table
    """
    
    # Rule 1: BMI 0-25, Age 0-40 -> Plan A
    if 0 <= bmi <= 25 and 0 <= age <= 40:
        return DecisionResponse(
            decision="Check up plan A",
            plan="A",
            doctor="A",
            thai_message="แนะนำให้ส่งผู้ป่วยตรวจสุขภาพตาม แผนตรวจสุขภาพ A และเข้าพบ แพทย์ A ค่ะ"
        )
    
    # Rule 2: BMI 25-1000, Age 0-40 -> Plan B  
    elif 25 < bmi <= 1000 and 0 <= age <= 40:
        return DecisionResponse(
            decision="Check up plan B",
            plan="B", 
            doctor="B",
            thai_message="แนะนำให้ส่งผู้ป่วยตรวจสุขภาพตาม แผนตรวจสุขภาพ B และเข้าพบ แพทย์ B ค่ะ"
        )
    
    # Rule 3: BMI 0-25, Age 40-200 -> Plan C
    elif 0 <= bmi <= 25 and 40 < age <= 200:
        return DecisionResponse(
            decision="Check up plan C",
            plan="C",
            doctor="C", 
            thai_message="แนะนำให้ส่งผู้ป่วยตรวจสุขภาพตาม แผนตรวจสุขภาพ C และเข้าพบ แพทย์ C ค่ะ"
        )
    
    # Rule 4: BMI 25-1000, Age 40-200 -> Plan D
    elif 25 < bmi <= 1000 and 40 < age <= 200:
        return DecisionResponse(
            decision="Check up plan D",
            plan="D",
            doctor="D",
            thai_message="แนะนำให้ส่งผู้ป่วยตรวจสุขภาพตาม แผนตรวจสุขภาพ D และเข้าพบ แพทย์ D ค่ะ"
        )
    
    # If no rules match, raise an error
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid BMI ({bmi}) or Age ({age}) values. Please check the input ranges."
        )

@app.get("/")
async def root():
    return {
        "message": "Health Checkup Decision API",
        "description": "Submit BMI and Age to get health checkup recommendations in Thai",
        "endpoints": {
            "POST /checkup": "Get health checkup decision",
            "GET /docs": "API documentation"
        }
    }

@app.post("/checkup", response_model=DecisionResponse)
async def get_checkup_decision(patient: PatientData):
    """
    Get health checkup decision based on patient's BMI and age
    
    Returns recommendation in Thai language with appropriate checkup plan and doctor assignment.
    """
    try:
        decision = get_health_checkup_decision(patient.bmi, patient.age)
        return decision
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/test")
async def test_cases():
    """
    Test endpoint showing example cases for each decision rule
    """
    test_cases = [
        {"bmi": 20, "age": 30, "expected": "Plan A"},
        {"bmi": 30, "age": 35, "expected": "Plan B"}, 
        {"bmi": 22, "age": 50, "expected": "Plan C"},
        {"bmi": 28, "age": 60, "expected": "Plan D"}
    ]
    
    results = []
    for case in test_cases:
        try:
            decision = get_health_checkup_decision(case["bmi"], case["age"])
            results.append({
                "input": f"BMI: {case['bmi']}, Age: {case['age']}",
                "expected": case["expected"],
                "result": decision.thai_message
            })
        except Exception as e:
            results.append({
                "input": f"BMI: {case['bmi']}, Age: {case['age']}",
                "expected": case["expected"], 
                "error": str(e)
            })
    
    return {"test_results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)