# fiiiiilm
## 소개
### 현재 상영작의 리뷰를 작성하고 공유하는 서비스입니다.
## 와이어 프레임
### https://www.figma.com/file/x5MlxQWD53HmMhct4ekcbD/fiiiiilm?type=design&node-id=0-1&t=E6dGrX9DReUX8c6c-0
## ERD
![Alt text](https://file.notion.so/f/s/357c610e-8fcb-47b1-920c-39c81a939fe5/Untitled.png?id=22f3c1a6-f124-4011-9c84-360ffe223d3d&table=block&spaceId=23cd6162-c29e-40ea-b2ea-6d40b7d2a522&expirationTimestamp=1683886574559&signature=_UNA9WO_DAKUE79NVdq8TFT9uSh0bgY1eqKjm0vkBoQ&downloadName=Untitled.png)
## 기능
- 회원기능
  - 소셜 로그인 API를 사용합니다.
    - 카카오 로그인
    - 깃허브 로그인

  - 인증 방식: JWT 인증

- 영화 API
  - TMDb

- 리뷰 CRUD

- 댓글 CRUD

## API 설계
|url|Method|기능|Request|Response|
|---|------|---|-------|--------|
|/api/v1/users/|GET|유저 전체 목록 조회||{"pk": pk, "email": 이메일, "nickname": 닉네임, "intro": 자기소개, "followings": 팔로잉, "followers": 팔로워, "reviews": 작성한 리뷰}|
|/api/v1/users/me/|GET|내 정보 조회|{"user"}|{"pk": pk, "email": 이메일, "nickname": 닉네임, "intro": 자기소개, "followings": 팔로잉, "followers": 팔로워, "reviews": 작성한 리뷰}|
|/api/v1/users/<int:pk>/|GET, PUT, DELETE|유저 정보 조회, 수정, 삭제|{"user", "pk"}|{"pk": pk, "email": 이메일, "nickname": 닉네임, "intro": 자기소개, "followings": 팔로잉, "followers": 팔로워, "reviews": 작성한 리뷰}|
|/api/v1/users/<int:pk>/follow/|POST|팔로우, 언팔로우|{"user", "pk"}||
|/api/v1/users/kakao-login/|POST|카카오 로그인|{"code"}|{"access_token", "refresh_token"}|
|/api/v1/users/github-login/|POST|깃허브 로그인|{"code"}|{"access_token", "refresh_token"}|
|/api/v1/movie/|GET|현재 상영 중인 영화 인기도 순으로 조회||{"rank": 순위, "movie_code": 영화 코드, "title": 영화 제목, "poster_path": 포스터 경로}|
|/api/v1/movie/detail/|GET|영화 상세 정보 조회|{"movie_code"}|{"movie_code": 영화 코드, "title": 영화 제목, "genres": 영화 장르, "overview": 영화 설명, "poster_path": 포스터 경로, "release_date": 개봉일, "runtime": 상영 시간, "vote_average": 평점}|
|/api/v1/reviews/|GET, POST|리뷰 조회, 작성|{"user", "title", "content", "movie_code"}|{"user", "movie_code", "title", "content", "created_at", "updated_at", "comment_count", "like_count"}|
|/api/v1/reviews/recent/|GET|최신 리뷰 조회||{"user", "movie_code", "title", "content", "created_at", "updated_at", "comment_count", "like_count"}|
|/api/v1/reviews/<int:pk>/|GET, PUT, DELETE|상세 리뷰 조회, 수정, 삭제|{"user", "title", "content", "movie_code"}|{"user", "movie_code", "title", "content", "created_at", "updated_at", "comments", "comment_count", "like_users" "like_count"}|
|/api/v1/reviews/<int:pk>/like/|POST|리뷰 좋아요|{"user", "pk"}||
|/api/v1/reviews/<int:pk>/comments/|GET, POST|댓글 조회, 작성|{"user", "pk", "content"}|{"user", "review", "content", "created_at", "updated_at"}|
|/api/v1/comments/<int:pk>/|PUT, DELETE|댓글 수정, 삭제|{"user", "pk", "content"}|{"user", "review", "content", "created_at", "updated_at"}|


