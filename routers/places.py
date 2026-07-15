from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import FestivalDetail, Place, CONTENT_TYPE_LABEL
from schemas import PlaceDetailResponse, PlaceResponse, PlaceListResponse, MapPlaceResponse, WeeklyFestivalResponse

router = APIRouter(prefix="/api/places", tags=["지역정보 · 지도"])

PAGE_SIZE = 20

LABEL_TO_TYPE_ID = {v: k for k, v in CONTENT_TYPE_LABEL.items()}

CATEGORY_DESC = "관광지, 레포츠, 문화시설, 쇼핑, 숙박, 여행코스, 축제공연행사"


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

def serialize_festival_detail(detail: FestivalDetail | None) -> dict | None:
    if not detail:
        return None
    return {
        "eventstartdate":       detail.eventstartdate,
        "eventenddate":         detail.eventenddate,
        "eventplace":           detail.eventplace,
        "playtime":             detail.playtime,
        "program":              detail.program,
        "subevent":             detail.subevent,
        "sponsor1":             detail.sponsor1,
        "sponsor1tel":          detail.sponsor1tel,
        "sponsor2":             detail.sponsor2,
        "sponsor2tel":          detail.sponsor2tel,
        "eventhomepage":        detail.eventhomepage,
        "bookingplace":         detail.bookingplace,
        "agelimit":             detail.agelimit,
        "festivalgrade":        detail.festivalgrade,
        "placeinfo":            detail.placeinfo,
        "spendtimefestival":    detail.spendtimefestival,
        "discountinfofestival": detail.discountinfofestival,
        "usetimefestival":      detail.usetimefestival,
    }

def current_week_range() -> tuple[str, str]:
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y%m%d"), sunday.strftime("%Y%m%d")

@router.get(
    "",
    response_model=PlaceListResponse,
    summary="지역정보 목록 조회",
    description=(
        "카테고리 필터와 키워드 검색을 조합해 장소 목록을 반환합니다. "
        "20개씩 페이징됩니다.\n\n"
        f"**카테고리 목록:** {CATEGORY_DESC}\n\n"
        "**keyword:** 장소명(title) 또는 주소(addr1) 부분 일치 검색"
    ),
    responses={400: {"description": "유효하지 않은 카테고리"}},
)
def list_places(
    category: str = Query(default=None, description=f"카테고리 ({CATEGORY_DESC})"),
    keyword:  str = Query(default=None, description="장소명 또는 주소 검색어 (부분 일치)"),
    page:     int = Query(default=1, ge=1, description="페이지 번호"),
    db: Session = Depends(get_db),
):
    query = db.query(Place)

    if category:
        type_id = LABEL_TO_TYPE_ID.get(category)
        if not type_id:
            raise HTTPException(status_code=400, detail=f"유효하지 않은 카테고리입니다: {category}")
        query = query.filter(Place.contenttypeid == type_id)

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


@router.get(
    "/map",
    response_model=list[MapPlaceResponse],
    summary="지도용 위치 데이터 조회",
    description=(
        "선택한 카테고리의 모든 장소에 대해 지도 마커 렌더링에 필요한 "
        "최소 데이터(제목, 주소, 좌표)를 반환합니다. 페이징 없이 전체를 반환합니다.\n\n"
        f"**카테고리 목록:** {CATEGORY_DESC}\n\n"
        "※ '전체' 카테고리는 지원하지 않습니다. 카테고리를 반드시 지정해야 합니다."
    ),
    responses={
        400: {"description": "유효하지 않은 카테고리"},
        422: {"description": "카테고리 파라미터 누락"},
    },
)
def map_places(
    category: str = Query(description=f"카테고리 (필수) — {CATEGORY_DESC}"),
    db: Session = Depends(get_db),
):
    type_id = LABEL_TO_TYPE_ID.get(category)
    if not type_id:
        raise HTTPException(status_code=400, detail=f"유효하지 않은 카테고리입니다: {category}")

    rows = (
        db.query(
            Place.contentid,
            Place.title,
            Place.addr1,
            Place.addr2,
            Place.mapx,
            Place.mapy,
        )
        .filter(
            Place.contenttypeid == type_id,
            Place.mapx.isnot(None),
            Place.mapy.isnot(None),
        )
        .all()
    )

    return [
        {
            "contentid": r.contentid,
            "title":     r.title,
            "addr":      " ".join(filter(None, [r.addr1, r.addr2])),
            "mapx":      r.mapx,
            "mapy":      r.mapy,
        }
        for r in rows
    ]

@router.get(
    "/festivals/this-week",
    response_model=WeeklyFestivalResponse,
    summary="이번 주 축제공연행사 조회",
    description="이번 주(월요일~일요일) 기간과 겹치는 축제공연행사를 반환합니다.",
)
def this_week_festivals(db: Session = Depends(get_db)):
    week_start, week_end = current_week_range()

    rows = (
        db.query(Place, FestivalDetail)
        .join(FestivalDetail, FestivalDetail.place_id == Place.id)
        .filter(
            Place.contenttypeid == "15",
            FestivalDetail.eventstartdate.isnot(None),
            FestivalDetail.eventenddate.isnot(None),
            FestivalDetail.eventstartdate <= week_end,
            FestivalDetail.eventenddate >= week_start,
        )
        .order_by(FestivalDetail.eventstartdate.asc(), Place.title.asc())
        .all()
    )

    items = []
    for place, detail in rows:
        items.append(
            {
                "contentid": place.contentid,
                "title": place.title,
                "addr": " ".join(filter(None, [place.addr1, place.addr2])),
                "mapx": place.mapx,
                "mapy": place.mapy,
                "eventstartdate": detail.eventstartdate,
                "eventenddate": detail.eventenddate,
                "eventplace": detail.eventplace,
                "usetimefestival": detail.usetimefestival,
                "agelimit": detail.agelimit,
            }
        )

    return {
        "week_start": week_start,
        "week_end": week_end,
        "total": len(items),
        "items": items,
    }


@router.get(
    "/{contentid}",
    response_model=PlaceDetailResponse,
    summary="장소 단건 조회",
    description="contentid로 장소 정보를 조회합니다. 축제공연행사인 경우 축제 상세도 함께 반환합니다.",
    responses={404: {"description": "장소 없음"}},
)
def get_place(contentid: str, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.contentid == contentid).first()
    if not place:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")

    return {
        **serialize(place),
        "festival_detail": serialize_festival_detail(place.festival_detail),
    }