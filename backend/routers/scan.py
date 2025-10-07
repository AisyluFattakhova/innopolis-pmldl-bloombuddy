from fastapi import APIRouter, UploadFile, File
from ai_services.scan_service import analyze_plant_image

router = APIRouter(prefix="/scan", tags=["scan"])

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    result = analyze_plant_image(file)
    return {"result": result}
