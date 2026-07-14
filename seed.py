import json
from pathlib import Path
from database import engine, Base, SessionLocal
from models import Place

DATA_DIR = Path("D:/data/서울")

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


def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    total = 0

    for filename in FILES:
        path = DATA_DIR / filename
        if not path.exists():
            print(f"[SKIP] {filename} 파일 없음")
            continue

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        places = [
            Place(
                contentid    = item["contentid"],
                contenttypeid= item["contenttypeid"],
                title        = item["title"],
                addr1        = item["addr1"] or None,
                addr2        = item["addr2"] or None,
                zipcode      = item["zipcode"] or None,
                tel          = item["tel"] or None,
                mapx         = to_float(item["mapx"]),
                mapy         = to_float(item["mapy"]),
                mlevel       = item["mlevel"] or None,
                areacode     = item["areacode"] or None,
                sigungucode  = item["sigungucode"] or None,
                cat1         = item["cat1"] or None,
                cat2         = item["cat2"] or None,
                cat3         = item["cat3"] or None,
                lclsSystm1   = item["lclsSystm1"] or None,
                lclsSystm2   = item["lclsSystm2"] or None,
                lclsSystm3   = item["lclsSystm3"] or None,
                firstimage   = item["firstimage"] or None,
                firstimage2  = item["firstimage2"] or None,
                cpyrhtDivCd  = item["cpyrhtDivCd"] or None,
                createdtime  = item["createdtime"] or None,
                modifiedtime = item["modifiedtime"] or None,
            )
            for item in data["items"]
        ]

        db.bulk_save_objects(places)
        db.commit()
        print(f"[OK] {filename}: {len(places)}건 삽입")
        total += len(places)

    db.close()
    print(f"\n완료: 총 {total}건 삽입")


if __name__ == "__main__":
    seed()
