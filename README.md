# 서울 관광 API

서울 관광 정보 플랫폼의 FastAPI 백엔드입니다. 한국관광공사 TourAPI 4.0 기반의 서울 지역 데이터를 제공하고, 익명 커뮤니티 게시판과 댓글 기능을 함께 제공합니다.

## 주요 기능

- 서울 관광 데이터 조회: 관광지, 레포츠, 문화시설, 쇼핑, 숙박, 여행코스, 축제공연행사
- 카테고리/키워드 기반 목록 검색 및 페이지네이션
- 지도용 좌표 데이터 제공
- 이번 주 축제공연행사 조회
- 익명 커뮤니티 게시글 CRUD
- 게시글 댓글 CRUD

## 기술 스택

- FastAPI
- SQLAlchemy
- SQLite 기본 사용, `DATABASE_URL` 설정 시 외부 DB 사용 가능
- Pydantic

## 프로젝트 구조

- `main.py`: FastAPI 앱 설정 및 라우터 등록
- `database.py`: DB 연결 및 세션 설정
- `models.py`: ORM 모델 정의
- `schemas.py`: API 요청/응답 스키마 정의
- `routers/places.py`: 지역정보/지도 API
- `routers/community.py`: 커뮤니티 API
- `seed.py`: JSON 데이터를 DB에 적재하는 초기화 스크립트
- `data/서울/*.json`: 서울 관광 원천 데이터

## 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

기본값은 `sqlite:///./seoul.db` 입니다. 다른 DB를 쓰려면 `.env` 또는 실행 환경에 `DATABASE_URL`을 설정하세요.

예시:

```env
DATABASE_URL=sqlite:///./seoul.db
```

### 3. 데이터 적재

```bash
python seed.py
```

이 스크립트는 `data/서울` 폴더의 JSON 파일을 읽어서 `places`와 `festival_details` 테이블을 채웁니다.

### 4. 서버 실행

```bash
python -m venv venv (가상환경 생성)
source venv/Scripts/activate (가상환경 활성화)
uvicorn main:app --reload

deactivate (닫기)
```

기본 접속 주소:

- API 서버: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API 요약

### 커뮤니티

기본 prefix: `/api/community`

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/api/community/recent` | 최근 게시글 5개 조회 |
| GET | `/api/community` | 게시글 목록 조회, 카테고리/제목 검색, 10개씩 페이징 |
| GET | `/api/community/{post_id}` | 게시글 단건 조회 및 댓글 포함 |
| POST | `/api/community` | 게시글 작성 |
| PUT | `/api/community/{post_id}` | 비밀번호 확인 후 게시글 수정 |
| DELETE | `/api/community/{post_id}` | 비밀번호 확인 후 게시글 삭제 |
| GET | `/api/community/{post_id}/comments` | 댓글 목록 조회 |
| POST | `/api/community/{post_id}/comments` | 댓글 작성 |
| PUT | `/api/community/comments/{comment_id}` | 비밀번호 확인 후 댓글 수정 |
| DELETE | `/api/community/comments/{comment_id}` | 비밀번호 확인 후 댓글 삭제 |

게시글 카테고리:

- 전체
- 관광지
- 레포츠
- 문화시설
- 쇼핑
- 숙박
- 여행코스
- 축제공연행사

### 지역정보 · 지도

기본 prefix: `/api/places`

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/api/places` | 장소 목록 조회, 카테고리/키워드 검색, 20개씩 페이징 |
| GET | `/api/places/map` | 지도용 좌표 데이터 전체 반환 |
| GET | `/api/places/festivals/this-week` | 이번 주에 해당하는 축제공연행사 조회 |
| GET | `/api/places/{contentid}` | 장소 단건 조회, 축제인 경우 상세 정보 포함 |

지원 카테고리:

- 관광지
- 레포츠
- 문화시설
- 쇼핑
- 숙박
- 여행코스
- 축제공연행사

## 배포 설정

`render.yaml` 기준으로 배포 시 `python seed.py`를 먼저 실행한 뒤 `uvicorn main:app --host 0.0.0.0 --port $PORT`로 서버를 시작합니다.

## 참고

- CORS는 현재 모든 origin을 허용합니다.
- 데이터는 서울 관광 JSON 파일을 기준으로 초기화됩니다.
- 커뮤니티는 별도 로그인 없이 닉네임과 비밀번호로 글과 댓글을 관리합니다.