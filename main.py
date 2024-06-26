import ast
import json

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing_extensions import Annotated

from service.gemini_client import GeminiService
from service.mongo_client import TutorService

app = FastAPI()

templates = Jinja2Templates(directory="templates")


availability = [
    {"day": "Saturday", "available_times": [{"start": "", "end": ""}]},
    {"day": "Sunday", "available_times": [{"start": "", "end": ""}]},
    {"day": "Monday", "available_times": [{"start": "", "end": ""}]},
    {"day": "Wednesday", "available_times": [{"start": "", "end": ""}]},
    {"day": "Tuesday", "available_times": [{"start": "", "end": ""}]},
    {"day": "Thursday", "available_times": [{"start": "", "end": ""}]},
    {"day": "Friday", "available_times": [{"start": "", "end": ""}]},
]


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit")
async def submit_form(request: Request, prompt: Annotated[str, Form()]):
    chat_service = GeminiService()
    full_prompt = f"create a mongodb formatted document with day and available times fields using this prompt:{prompt}, and format like this: {availability}"
    raw_response = chat_service.get_response(full_prompt)

    clean_response = raw_response.strip("'''```json\n").strip("``` \n")
    data = json.loads(clean_response)

    return templates.TemplateResponse(
        "calendar.html", {"request": request, "availability": data}
    )


@app.post("/insert")
async def submit_availability(request: Request, availability: Annotated[str, Form()]):

    formatted_response = ast.literal_eval(availability)
    TutorService().insert_slots(formatted_response)
    return {"message": "Data inserted successfully"}