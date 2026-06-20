from fastapi import APIRouter
from models.request_models import ChecklistRequest
from models.response_models import ChecklistResponse

router = APIRouter()

@router.post("/", response_model=ChecklistResponse)
async def generate_checklist(request: ChecklistRequest):
    return ChecklistResponse(
        items=[
            {"item_id": "chk_01", "task": f"Verify HS Code classification for query: {request.query}", "status": "Pending"},
            {"item_id": "chk_02", "task": "Review import/export licenses and permits", "status": "Pending"},
            {"item_id": "chk_03", "task": "Check customs compliance documentation checklist", "status": "Completed"}
        ]
    )
