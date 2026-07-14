from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Place, CONTENT_TYPE_LABEL

router = APIRouter(prefix="/api/places", tags=["places"])

PAGE_SIZE = 20

# 한국어 카테고리명 → contenttypeid 역매핑
LABEL_TO_TYPE_ID = {v: k for k, v in CONTENT_TYPE_LABEL.items()}


def serialize(place: Place) -> dict:
    return {
        "contentid":     place.contentid,
        "contenttypeid": place.contenttypeid,
        "category":      CONTENT_TYPE_LABEL.get(place.contenttypeid, "기타"),
        "title":         place.title,
        "addr1":         place.addr1,
        "addr2":         place.addr2,
        "tel":           place.tel,
        "firstimage":    place.firstimage,
        "firstimage2":   place.firstimage2,
        "mapx":          place.mapx,
        "mapy":          place.mapy,
    }


@router.get("")
def list_places(
    category: str = Query(default=None, description="카테고리 (예: 관광지, 숙박)"),
    keyword:  str = Query(default=None, description="장소명 또는 주소 검색어"),
    page:     int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    query = db.query(Place)

    # 카테고리 필터
    if category:
        type_id = LABEL_TO_TYPE_ID.get(category)
        if not type_id:
            raise HTTPException(status_code=400, detail=f"유효하지 않은 카테고리입니다: {category}")
        query = query.filter(Place.contenttypeid == type_id)

    # 장소명 또는 주소 검색 (OR 조건)
    if keyword:
        query = query.filter(
            Place.title.like(f"%{keyword}%") |
            Place.addr1.like(f"%{keyword}%")
        )

    total = query.count()
    places = query.offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()

    return {
        "total":     total,
        "page":      page,
        "page_size": PAGE_SIZE,
        "items":     [serialize(p) for p in places],
    }


@router.get("/{contentid}")
def get_place(contentid: str, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.contentid == contentid).first()
    if not place:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return serialize(place)
