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


# 댓글

class CommentCreate(BaseModel):
    nickname: str = Field(example="댓글러")
    content:  str = Field(example="좋은 정보 감사합니다.")
    password: str = Field(example="1234")


class CommentUpdate(BaseModel):
    content:  str = Field(example="내용을 조금 수정합니다.")
    password: str = Field(example="1234")


class CommentResponse(BaseModel):
    id:         int  = Field(example=1)
    post_id:    int  = Field(example=1)
    content:    str  = Field(example="좋은 정보 감사합니다.")
    nickname:   str  = Field(example="댓글러")




class CommentListResponse(BaseModel):
    total:     int              = Field(example=3)
    items:     list[CommentResponse]


class PostDetailResponse(PostResponse):
    comments: list[CommentResponse] = Field(default_factory=list)

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


class FestivalDetailResponse(BaseModel):
    eventstartdate:       str | None = Field(example="20260916")
    eventenddate:         str | None = Field(example="20260920")
    eventplace:           str | None = Field(example="마로니에 공원")
    playtime:             str | None = Field(example="프로그램 별 상이함")
    program:              str | None = Field(example="개막식, 북토크, 워크숍 등")
    subevent:             str | None = Field(example="")
    sponsor1:             str | None = Field(example="한국문화예술위원회")
    sponsor1tel:          str | None = Field(example="070-7954-1369")
    sponsor2:             str | None = Field(example="한국문화예술위원회")
    sponsor2tel:          str | None = Field(example="")
    eventhomepage:        str | None = Field(example="")
    bookingplace:         str | None = Field(example="")
    agelimit:             str | None = Field(example="전 연령")
    festivalgrade:        str | None = Field(example="")
    placeinfo:            str | None = Field(example="")
    spendtimefestival:    str | None = Field(example="")
    discountinfofestival: str | None = Field(example="")
    usetimefestival:      str | None = Field(example="무료")

class WeeklyFestivalItemResponse(BaseModel):
    contentid:       str = Field(example="2751541")
    title:           str = Field(example="문학주간 2026")
    addr:            str = Field(example="서울특별시 종로구 동숭길 3")
    mapx:            float | None = Field(example=127.0043)
    mapy:            float | None = Field(example=37.5805)
    eventstartdate:  str | None = Field(example="20260916")
    eventenddate:    str | None = Field(example="20260920")
    eventplace:      str | None = Field(example="마로니에 공원")
    usetimefestival: str | None = Field(example="무료")
    agelimit:        str | None = Field(example="전 연령")


class WeeklyFestivalResponse(BaseModel):
    week_start: str = Field(example="20260914")
    week_end:   str = Field(example="20260920")
    total:      int = Field(example=12)
    items:      list[WeeklyFestivalItemResponse]


class PlaceDetailResponse(PlaceResponse):
    festival_detail: FestivalDetailResponse | None = None


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
