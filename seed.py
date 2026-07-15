import json
from pathlib import Path
from database import engine, Base, SessionLocal
from models import FestivalDetail, Place

DATA_DIR = Path(__file__).parent / "data" / "서울"

FILES = [
    "서울_관광지.json",
    "서울_레포츠.json",
    "서울_문화시설.json",
    "서울_쇼핑.json",
    "서울_숙박.json",
    "서울_여행코스.json",
    "서울_축제공연행사.json",
]


def to_float(value: str) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def normalize(value):
    if value is None:
        return None
    if isinstance(value, str):
        v = value.strip()
        return v if v else None
    return str(value)


def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    total = 0

    try:
        for filename in FILES:
            path = DATA_DIR / filename
            if not path.exists():
                print(f"[SKIP] {filename} 파일 없음")
                continue

            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            items = data.get("items", [])
            inserted_or_updated = 0

            for item in items:
                contentid = normalize(item.get("contentid"))
                if not contentid:
                    continue

                place = db.query(Place).filter(Place.contentid == contentid).first()
                if not place:
                    place = Place(contentid=contentid)
                    db.add(place)

                place.contenttypeid = normalize(item.get("contenttypeid"))
                place.title         = normalize(item.get("title"))
                place.addr1         = normalize(item.get("addr1"))
                place.addr2         = normalize(item.get("addr2"))
                place.zipcode       = normalize(item.get("zipcode"))
                place.tel           = normalize(item.get("tel"))
                place.mapx          = to_float(item.get("mapx"))
                place.mapy          = to_float(item.get("mapy"))
                place.mlevel        = normalize(item.get("mlevel"))
                place.areacode      = normalize(item.get("areacode"))
                place.sigungucode   = normalize(item.get("sigungucode"))
                place.cat1          = normalize(item.get("cat1"))
                place.cat2          = normalize(item.get("cat2"))
                place.cat3          = normalize(item.get("cat3"))
                place.lclsSystm1    = normalize(item.get("lclsSystm1"))
                place.lclsSystm2    = normalize(item.get("lclsSystm2"))
                place.lclsSystm3    = normalize(item.get("lclsSystm3"))
                place.firstimage    = normalize(item.get("firstimage"))
                place.firstimage2   = normalize(item.get("firstimage2"))
                place.cpyrhtDivCd   = normalize(item.get("cpyrhtDivCd"))
                place.createdtime   = normalize(item.get("createdtime"))
                place.modifiedtime  = normalize(item.get("modifiedtime"))

                is_festival = place.contenttypeid == "15"

                if is_festival:
                    if not place.festival_detail:
                        place.festival_detail = FestivalDetail()

                    fd = place.festival_detail
                    fd.eventstartdate       = normalize(item.get("eventstartdate"))
                    fd.eventenddate         = normalize(item.get("eventenddate"))
                    fd.eventplace           = normalize(item.get("eventplace"))
                    fd.playtime             = normalize(item.get("playtime"))
                    fd.program              = normalize(item.get("program"))
                    fd.subevent             = normalize(item.get("subevent"))
                    fd.sponsor1             = normalize(item.get("sponsor1"))
                    fd.sponsor1tel          = normalize(item.get("sponsor1tel"))
                    fd.sponsor2             = normalize(item.get("sponsor2"))
                    fd.sponsor2tel          = normalize(item.get("sponsor2tel"))
                    fd.eventhomepage        = normalize(item.get("eventhomepage"))
                    fd.bookingplace         = normalize(item.get("bookingplace"))
                    fd.agelimit             = normalize(item.get("agelimit"))
                    fd.festivalgrade        = normalize(item.get("festivalgrade"))
                    fd.placeinfo            = normalize(item.get("placeinfo"))
                    fd.spendtimefestival    = normalize(item.get("spendtimefestival"))
                    fd.discountinfofestival = normalize(item.get("discountinfofestival"))
                    fd.usetimefestival      = normalize(item.get("usetimefestival"))
                else:
                    if place.festival_detail:
                        db.delete(place.festival_detail)

                inserted_or_updated += 1

            db.commit()
            print(f"[OK] {filename}: {inserted_or_updated}건 반영")
            total += inserted_or_updated

        print(f"\n완료: 총 {total}건 반영")

    finally:
        db.close()



if __name__ == "__main__":
    seed()
