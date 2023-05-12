# fiiiiilm
## 소개
### 현재 상영작의 리뷰를 작성하고 공유하는 서비스입니다.
## 와이어 프레임
### https://www.figma.com/file/x5MlxQWD53HmMhct4ekcbD/fiiiiilm?type=design&node-id=0-1&t=E6dGrX9DReUX8c6c-0
## ERD
![Alt text](https://file.notion.so/f/s/a2adae27-bcf7-40d2-84aa-00868f2e5ed0/Untitled.png?id=79746387-0410-46f5-b252-dbd70e66c8a3&table=block&spaceId=23cd6162-c29e-40ea-b2ea-6d40b7d2a522&expirationTimestamp=1683963697748&signature=rafF63BjvDi8lY18DnDI8NgtDEg1UVPvPgS8PQG2s9k&downloadName=Untitled.png)
## 기능
- 회원기능
  - 소셜 로그인 API를 사용합니다.
    - 카카오 로그인
    - 깃허브 로그인

  - 인증 방식: JWT 인증
  - 팔로우, 언팔로우

- 영화 API
  - TMDb

- 리뷰 CRUD
  - 좋아요

- 댓글 CRUD

## API 설계
|url|Method|기능|Request|Response|
|---|------|---|-------|--------|
|/api/v1/users/|GET|유저 전체 목록 조회||{"pk": pk, "email": 이메일, "nickname": 닉네임, "intro": 자기소개, "followings": 팔로잉, "followers": 팔로워, "reviews": 작성한 리뷰}|
|/api/v1/users/me/|GET|내 정보 조회|{"user"}|{"pk": pk, "email": 이메일, "nickname": 닉네임, "intro": 자기소개, "followings": 팔로잉, "followers": 팔로워, "reviews": 작성한 리뷰}|
|/api/v1/users/<int:pk>/|GET, PUT, DELETE|유저 정보 조회, 수정, 삭제|{"user"}|{"pk": pk, "email": 이메일, "nickname": 닉네임, "intro": 자기소개, "followings": 팔로잉, "followers": 팔로워, "reviews": 작성한 리뷰}|
|/api/v1/users/<int:pk>/follow/|POST|팔로우, 언팔로우|{"user"}||
|/api/v1/users/kakao-login/|POST|카카오 로그인|{"code"}|{"access_token", "refresh_token"}|
|/api/v1/users/github-login/|POST|깃허브 로그인|{"code"}|{"access_token", "refresh_token"}|
|/api/v1/movie/|GET|현재 상영 중인 영화 인기도 순으로 조회||{"rank", "movieCode", "title", "posterPath"}|
|/api/v1/movie/<int:movie_code>/|GET|영화 상세 정보 조회||{"movieCode", "title", "genre", "overview", "posterPath", "releaseDate", "runtime", "rating"}|
|/api/v1/movie/<int:movie_code>/reviews/|GET, POST|리뷰 조회, 작성|{"user", "title", "content", "movie_title"}|{"user", "movie_code", "title", "content", "created_at", "updated_at", "comment_count", "like_count", "movie_title", "avatar"}|
|/api/v1/reviews/recent/|GET|최신 리뷰 조회||{"user", "movie_code", "title", "content", "created_at", "updated_at", "comment_count", "like_count", "movie_title", "avatar"}|
|/api/v1/reviews/<int:pk>/|GET, PUT, DELETE|상세 리뷰 조회, 수정, 삭제|{"user", "title", "content"}|{"user", "movie_code", "title", "content", "created_at", "updated_at", "comments", "comment_count", "like_users" "like_count", "movie_title", "avatar"}|
|/api/v1/reviews/<int:pk>/like/|POST|리뷰 좋아요|{"user"}||
|/api/v1/reviews/<int:pk>/comments/|GET, POST|댓글 조회, 작성|{"user", "content"}|{"user", "review", "content", "created_at", "updated_at"}|
|/api/v1/comments/<int:pk>/|PUT, DELETE|댓글 수정, 삭제|{"user", "content"}|{"user", "review", "content", "created_at", "updated_at"}|


