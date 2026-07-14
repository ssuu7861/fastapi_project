from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import community, places

Base.metadata.create_all(bind=engine)

app = FastAPI(title="서울 관광 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(community.router)
app.include_router(places.router)
