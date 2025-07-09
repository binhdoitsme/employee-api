from fastapi import FastAPI

from employee_api.controllers.search_controller import search_router

app = FastAPI(title="Employee API", version="1.0.0")

app.include_router(search_router)
