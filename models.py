from sqlalchemy import Column, Integer, String, Float
from database import Base



CONTENT_TYPE_LABEL = {
    "12": "관광지",
    "14": "문화시설",
    "15": "축제공연행사",
    "25": "여행코스",
    "28": "레포츠",
    "32": "숙박",
    "38": "쇼핑",
    "39": "음식점",
}


class Place(Base):
    __tablename__ = "places"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    contentid     = Column(String, unique=True, index=True, nullable=False)
    contenttypeid = Column(String, index=True)
    title         = Column(String, index=True)
    addr1         = Column(String)
    addr2         = Column(String)
    zipcode       = Column(String)
    tel           = Column(String)
    mapx          = Column(Float)
    mapy          = Column(Float)
    mlevel        = Column(String)
    areacode      = Column(String)
    sigungucode   = Column(String)
    cat1          = Column(String)
    cat2          = Column(String)
    cat3          = Column(String)
    lclsSystm1    = Column(String)
    lclsSystm2    = Column(String)
    lclsSystm3    = Column(String)
    firstimage    = Column(String)
    firstimage2   = Column(String)
    cpyrhtDivCd   = Column(String)
    createdtime   = Column(String)
    modifiedtime  = Column(String)
