# Database Project 1st Iteration
2019143073 엄소은
## ER-Diagram & Mapping ERD to Relational Schema

### 1. ER-Diagram
<img width="663" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/86105c22-6dfa-4215-b5f0-b9cb897cc26d">

### 2. Relational Schema
<img width="806" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/b6dbf4fb-df91-4d61-870d-d9ba90779250">

### 3. ERD 작성과 관련해 가정한 내용
1. 사용자는 다른 사용자의 글을 편집하거나 삭제할 수 없다.
2. 사용자는 본인의 글 및 답글에 '도움이 되어요' 를 클릭할 수 없다.

### 4. 일정
- 11/20
  - [X] 스키마 설계
  - [X] 데이터베이스 세팅
  - [X] 사용자 로그인 기능 구현∏
- 11/27 : 
  - [ ] 글 작성 기능
  - [ ] 글 편집 기능
  - [ ] 답글 기능
  - [ ] 검색 기능
- 12/4
  - [ ] 조회 기능
  - [ ] 중요도 기능
  - [ ] 자동 삭제 기능
- 12/11
  - [ ] 보고서 작성

## 시스템 설계 문서 및 중간 구현 내용
- Server Framework : FastAPI
- python version : 3.10
- RDBMS : MySQL

### Application Flowchart

<img width="863" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/e51b3777-a685-44c0-bc2e-79117fe29bd9">
