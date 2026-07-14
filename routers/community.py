from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models import Post, COMMUNITY_CATEGORIES

router = APIRouter(prefix="/api/community", tags=["community"])

PAGE_SIZE = 10


# ── Pydantic 스키마 ───────────────────────────────────────────

class PostCreate(BaseModel):
    category: str
    title: str
    content: str
    nickname: str
    password: str


class PostUpdate(BaseModel):
    title: str
    content: str
    password: str


class PasswordBody(BaseModel):
    password: str


# ── 내부 헬퍼 ────────────────────────────────────────────────

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def serialize(post: Post) -> dict:
    """비밀번호를 제외하고 직렬화"""
    return {
        "id":         post.id,
        "category":   post.category,
        "title":      post.title,
        "content":    post.content,
        "nickname":   post.nickname,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }


# ── 엔드포인트 ───────────────────────────────────────────────

@router.get("/recent")
def get_recent_posts(db: Session = Depends(get_db)):
    """홈 화면용: 최근 게시글 5개"""
    posts = db.query(Post).order_by(Post.id.desc()).limit(5).all()
    return [serialize(p) for p in posts]


@router.get("")
def list_posts(
    category: str = Query(default="전체"),
    title:    str = Query(default=None),
    page:     int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    """게시글 목록 조회 (카테고리 필터 + 제목 검색 + 페이징)"""
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


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """게시글 단건 조회"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return serialize(post)


@router.post("", status_code=201)
def create_post(body: PostCreate, db: Session = Depends(get_db)):
    """게시글 작성"""
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


@router.put("/{post_id}")
def update_post(post_id: int, body: PostUpdate, db: Session = Depends(get_db)):
    """게시글 수정 (비밀번호 확인)"""
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


@router.delete("/{post_id}")
def delete_post(post_id: int, body: PasswordBody, db: Session = Depends(get_db)):
    """게시글 삭제 (비밀번호 확인)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.password != body.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()
    return {"message": "삭제되었습니다."}
