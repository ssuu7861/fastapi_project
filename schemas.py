from pydantic import BaseModel, Field


# 커뮤니티

class PostCreate(BaseModel):
    category: str = Field(example="관광지")
    title:    str = Field(example="경복궁 다녀왔어요")
    content:  str = Field(example="역사적인 장소라 정말 좋았습니다.")
    nickname: str = Field(example="서울러")
    password: str = Field(example="1234")


class PostUpdate(BaseModel):
    title:    str = Field(example="경복궁 강추합니다!")
    content:  str = Field(example="두 번 가도 좋은 곳입니다.")
    password: str = Field(example="1234")


class PasswordBody(BaseModel):
    password: str = Field(example="1234")


class PostResponse(BaseModel):
    id:         int  = Field(example=1)
    category:   str  = Field(example="관광지")
    title:      str  = Field(example="경복궁 다녀왔어요")
    content:    str  = Field(example="역사적인 장소라 정말 좋았습니다.")
    nickname:   str  = Field(example="서울러")
    created_at: str  = Field(example="2026-07-14 22:00:00")
    updated_at: str  = Field(example="2026-07-14 22:00:00")


class PostListResponse(BaseModel):
    total:     int            = Field(example=42)
    page:      int            = Field(example=1)
    page_size: int            = Field(example=10)
    items:     list[PostResponse]


# 지역정보

class PlaceResponse(BaseModel):
    contentid:     str         = Field(example="1059877")
    contenttypeid: str         = Field(example="12")
    category:      str         = Field(example="관광지")
    title:         str         = Field(example="양화한강공원")
    addr1:         str | None  = Field(example="서울특별시 영등포구 노들로 221")
    addr2:         str | None  = Field(example="(당산동)")
    tel:           str | None  = Field(example="02-000-0000")
    firstimage:    str | None  = Field(example="https://tong.visitkorea.or.kr/...")
    firstimage2:   str | None  = Field(example="https://tong.visitkorea.or.kr/...")
    mapx:          float | None = Field(example=126.9023)
    mapy:          float | None = Field(example=37.5382)


class PlaceListResponse(BaseModel):
    total:     int            = Field(example=783)
    page:      int            = Field(example=1)
    page_size: int            = Field(example=20)
    items:     list[PlaceResponse]


# 지도

class MapPlaceResponse(BaseModel):
    contentid: str        = Field(example="1059877")
    title:     str        = Field(example="양화한강공원")
    addr:      str        = Field(example="서울특별시 영등포구 노들로 221 (당산동)")
    mapx:      float | None = Field(example=126.9023)
    mapy:      float | None = Field(example=37.5382)


# 공통

class MessageResponse(BaseModel):
    message: str = Field(example="삭제되었습니다.")
