
from fastapi import FastAPI, HTTPException

from .schemas import RequestCreate
from .events import send_maintenance_event


app = FastAPI(
    title="Equipment Maintenance API",
    description="API для управления заявками на обслуживание оборудования",
    version="1.0.0",
)


# Временное хранилище заявок в памяти
requests_db = []


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "FastAPI"
    }


@app.get("/requests")
def get_requests():
    return requests_db


@app.get("/requests/{request_id}")
def get_request(request_id: int):
    for request in requests_db:
        if request["id"] == request_id:
            return request

    raise HTTPException(
        status_code=404,
        detail="Заявка не найдена"
    )


@app.post("/requests")
def create_request(request_data: RequestCreate):
    new_id = len(requests_db) + 1

    new_request = {
        "id": new_id,
        "equipment_id": request_data.equipment_id,
        "description": request_data.description,
        "priority": request_data.priority,
        "status": "new",
    }

    requests_db.append(new_request)

    # Отправляем событие о создании заявки в RabbitMQ
    send_maintenance_event({
        "event": "maintenance_request_created",
        "request": new_request
    })

    return new_request
