from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import base64
import requests
from openai import OpenAI
import extractor 

gsheets_api_url = "https://your-google-sheets-api-endpoint.com"
openai_api_url = "https://api.openai.com/v1/vision"
openai_api_key = ""
os.environ["OPENAI_API_KEY"] = openai_api_key
client = OpenAI()

app = FastAPI()

# Enabling CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # you may adjust if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_cv(
    name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    cv: UploadFile = File(...)
):
    print("name:",name)
    print("phone_number:",phone_number)
    print("email:",email)

    if not cv.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_location = os.path.join(UPLOAD_DIR, cv.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(cv.file, buffer)


    extractor.extract_informations_from_pdf(cv.filename,name,phone_number,email)

    # imgs =convert_pdf_to_images(file_location)
    # print("images:",len(imgs))
    
    # # CONVERT FILE TO BASE64
    # with open(file_location, "rb") as file:
    #     encoded_cv = base64.b64encode(file.read()).decode("utf-8")

    
    
    # SEND IMAGE TO THE OPENAI VISION API WITH CUSTOM PROMPT
    # headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}
    # openai_payload = {"prompt": "Extract key details from this CV.", "image": encoded_cv}
    # openai_response = requests.post(openai_api_url, json=openai_payload, headers=headers)
    # openai_data = openai_response.json()
    
    # # GET THE RESPONSE FROM THE RESPONSE OBJECT AND SEND TO THE PROVIDED API
    # parsed_data = openai_data.get("choices", [{}])[0].get("text", "No data extracted")
    
    # # UPDATE THE GOOGLE SHEET
    # google_sheets_payload = {
    #     "name": name,
    #     "phone_number": phone_number,
    #     "email": email,
    #     "cv_data": parsed_data
    # }
    # requests.post(gsheets_api_url, json=google_sheets_payload)
    
    return {"allert": "CV uploaded successfully"}