from fastapi import APIRouter

router = APIRouter(
    prefix="/router",
    tags=["router"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {"message": "Benvenuto nell'API FastAPI"}