from fastapi import APIRouter
from models.request_models import WorkflowRequest
from models.response_models import WorkflowResponse
from services.workflow_service import workflow_service

router = APIRouter()

@router.post("/", response_model=WorkflowResponse)
async def generate_workflow(request: WorkflowRequest):
    return workflow_service.create_workflow(request)
