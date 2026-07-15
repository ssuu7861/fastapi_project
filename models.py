from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship
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

    festival_detail = relationship(
        "FestivalDetail",
        back_populates="place",
        uselist=False,
        cascade="all, delete-orphan",
    )


class FestivalDetail(Base):
    __tablename__ = "festival_details"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    place_id             = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    eventstartdate       = Column(String)
    eventenddate         = Column(String)
    eventplace           = Column(String)
    playtime             = Column(Text)
    program              = Column(Text)
    subevent             = Column(Text)
    sponsor1             = Column(String)
    sponsor1tel          = Column(String)
    sponsor2             = Column(String)
    sponsor2tel          = Column(String)
    eventhomepage        = Column(String)
    bookingplace         = Column(String)
    agelimit             = Column(String)
    festivalgrade        = Column(String)
    placeinfo            = Column(Text)
    spendtimefestival    = Column(String)
    discountinfofestival = Column(String)
    usetimefestival      = Column(String)

    place = relationship("Place", back_populates="festival_detail")

    
COMMUNITY_CATEGORIES = {
    "전체", "관광지", "레포츠", "문화시설", "쇼핑", "숙박", "여행코스", "축제공연행사"
}


class Post(Base):
    __tablename__ = "posts"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    category   = Column(String, nullable=False, index=True)
    title      = Column(String, nullable=False)
    content    = Column(Text, nullable=False)
    nickname   = Column(String, nullable=False)
    password   = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="Comment.id.asc()",
    )

class Comment(Base):
    __tablename__ = "comments"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    post_id    = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    content    = Column(Text, nullable=False)
    nickname   = Column(String, nullable=False)
    password   = Column(String, nullable=False)


    post = relationship("Post", back_populates="comments")