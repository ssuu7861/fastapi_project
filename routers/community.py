from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Post, COMMUNITY_CATEGORIES
from schemas import (
    PostCreate, PostUpdate, PasswordBody,
    PostResponse, PostListResponse, MessageResponse,
)

router = APIRouter(prefix="/api/community", tags=["커뮤니티"])

PAGE_SIZE = 10


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def serialize(post: Post) -> dict:
    return {
        "id":         post.id,
        "category":   post.category,
        "title":      post.title,
        "content":    post.content,
        "nickname":   post.nickname,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }


@router.get(
    "/recent",
    response_model=list[PostResponse],
    summary="최근 게시글 5개",
    description="홈 화면에 표시할 최근 게시글 5개를 최신순으로 반환합니다.",
)
def get_recent_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id.desc()).limit(5).all()
    return [serialize(p) for p in posts]


@router.get(
    "",
    response_model=PostListResponse,
    summary="게시글 목록 조회",
    description=(
        "카테고리 필터와 제목 검색을 조합해 게시글 목록을 반환합니다. "
        "10개씩 페이징됩니다.\n\n"
        "**카테고리 목록:** 전체, 관광지, 레포츠, 문화시설, 쇼핑, 숙박, 여행코스, 축제공연행사"
    ),
)
def list_posts(
    category: str = Query(default="전체", description="카테고리 (기본값: 전체)"),
    title:    str = Query(default=None,    description="제목 검색어 (부분 일치)"),
    page:     int = Query(default=1, ge=1, description="페이지 번호"),
    db: Session = Depends(get_db),
):
    query = db.query(Post)

    if category != "전체":
        query = query.filter(Post.category == category)
    if title:
        query = query.filter(Post.title.like(f"%{title}%"))

    query = query.order_by(Post.id.desc())
    total = query.count()
    posts = query.offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()

    return {
        "total":     total,
        "page":      page,
        "page_size": PAGE_SIZE,
        "items":     [serialize(p) for p in posts],
    }


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="게시글 단건 조회",
    description="게시글 ID로 단건을 조회합니다.",
    responses={404: {"description": "게시글 없음"}},
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return serialize(post)


@router.post(
    "",
    response_model=PostResponse,
    status_code=201,
    summary="게시글 작성",
    description=(
        "새 게시글을 작성합니다. "
        "수정·삭제 시 필요한 비밀번호를 함께 등록합니다. "
        "비밀번호는 평문으로 저장됩니다.\n\n"
        "**카테고리 목록:** 전체, 관광지, 레포츠, 문화시설, 쇼핑, 숙박, 여행코스, 축제공연행사"
    ),
    responses={400: {"description": "유효하지 않은 카테고리"}},
)
def create_post(body: PostCreate, db: Session = Depends(get_db)):
    if body.category not in COMMUNITY_CATEGORIES:
        raise HTTPException(status_code=400, detail="유효하지 않은 카테고리입니다.")

    now = now_str()
    post = Post(
        category   = body.category,
        title      = body.title,
        content    = body.content,
        nickname   = body.nickname,
        password   = body.password,
        created_at = now,
        updated_at = now,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return serialize(post)


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    summary="게시글 수정",
    description="비밀번호가 일치하는 경우에만 제목과 내용을 수정합니다.",
    responses={
        403: {"description": "비밀번호 불일치"},
        404: {"description": "게시글 없음"},
    },
)
def update_post(post_id: int, body: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.password != body.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    post.title      = body.title
    post.content    = body.content
    post.updated_at = now_str()
    db.commit()
    db.refresh(post)
    return serialize(post)


@router.delete(
    "/{post_id}",
    response_model=MessageResponse,
    summary="게시글 삭제",
    description="비밀번호가 일치하는 경우에만 게시글을 삭제합니다.",
    responses={
        403: {"description": "비밀번호 불일치"},
        404: {"description": "게시글 없음"},
    },
)
def delete_post(post_id: int, body: PasswordBody, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.password != body.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()
    return {"message": "삭제되었습니다."}
