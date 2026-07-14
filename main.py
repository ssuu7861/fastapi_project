from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import community, places

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "커뮤니티",
        "description": (
            "익명 커뮤니티 게시판 CRUD. "
            "별도 로그인 없이 닉네임과 비밀번호로 게시글을 작성·수정·삭제합니다."
        ),
    },
    {
        "name": "지역정보 · 지도",
        "description": (
            "한국관광공사 TourAPI 4.0 기반 서울 관광 데이터. "
            "지역정보 탭(목록·검색·페이징)과 지도 탭(카테고리별 좌표 전체 반환)을 제공합니다."
        ),
    },
]

app = FastAPI(
    title="서울 관광 API",
    version="1.0.0",
    description=(
        "서울 관광 정보 플랫폼 백엔드 API입니다.\n\n"
        "- **커뮤니티:** 익명 게시판 CRUD\n"
        "- **지역정보:** 카테고리·키워드 검색, 20개씩 페이징\n"
        "- **지도:** 카테고리별 마커 좌표 전체 반환\n\n"
        "데이터 출처: 한국관광공사 TourAPI 4.0 (공공누리 제3유형)"
    ),
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(community.router)
app.include_router(places.router)
