# Database Project
- Author : 2019143073 엄소은
### Table of Contents
1. [ER-Diagram & Mapping ERD to Relational Schema](#1-er-diagram--mapping-erd-to-relational-schema)
2. [기능 명세](#2-기능-명세)
3. [실행 방법](#3-실행-방법)
4. [구현 결과](#4-구현-결과)


## 1. ER-Diagram & Mapping ERD to Relational Schema

### ER-Diagram
<img width="500" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/86105c22-6dfa-4215-b5f0-b9cb897cc26d">

### Relational Schema
<img width="500" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/da086b2f-c371-435c-8d0a-dc7359fa69e9">

### ERD 작성과 관련해 가정한 내용
1. 사용자는 다른 사용자의 글을 편집하거나 삭제할 수 없다.
2. 사용자는 본인의 글 및 답글에 '도움이 되어요' 를 클릭할 수 없다.

### 일정
- 11/20
  - [X] 스키마 설계
  - [X] 데이터베이스 세팅
  - [X] 사용자 로그인 기능 구현∏
- 11/27 : 
  - [X] 글 작성 기능
  - [X] 글 편집 기능
  - [X] 답글 기능
  - [X] 검색 기능
- 12/4
  - [X] 조회 기능
  - [X] 중요도 기능
  - [X] 자동 삭제 기능
- 12/11
  - [X] 보고서 작성


-------
## 2. 기능 명세
### 사용자 관리
- [X] 사용자 만드는 기능
  - [X] 사용자 type 은 관리자(1), 일반 사용자(0) 으로 한다
- [X] 사용자 로그인 기능
- [X] 관리자는 사용자의 목록과 글 제출 상태를 관리할 수 있다. 

### 글 쓰기
- [X] 사용자가 로그인해서 글을 쓴다.
  - [X] 글 내용은 이미지, 비디오 가 포함될 수 있다.
  - [X] 보여지는 글에는 작성시간, 수정시간, 글 작성자, 글 내용, 글 조회수가 있다. 
- [X] 처음 글을 쓰면 조회수(view_count) 는 0이고, 중요도(help_count)도 0이다.
- [X] 사용자는 본인이 작성한 글을 편집할 수 있다. 
- [X] 사용자는 본인이 작성한 글을 삭제할 수 있다.

### 답글 쓰기
- [X] 사용자는 로그인해서 다른 사용자들의 글 / 본인의 글에 답글을 달 수 있다.
- [X] 사용자는 본인이 작성한 답글을 편집할 수 있다. 
- [X] 사용자는 본인이 작성한 답글을 삭제할 수 있다.

### 글 / 답글 조회
- [X] 사용자는 키워드로 글을 검색할 수 있다.
- [X] 사용자는 로그인해서 다른 사용자들의 글 / 답글을 볼 수 있다.
- [X] 사용자가 글 / 답글의 내용을 볼 때마다 조회수가 1 씩 올라간다. 
- [X] 사용자는 작성시간 , 조회수, 중요도 수 등의 조건으로 글을 조회할 수 있다.

### 중요해요 누르기
- [X] 사용자는 로그인해서 다른 사람의 글 / 답글에 '추천' 를 선택할 수 있다.
- [X] '추천' 을 선택하면 글/답글의 help_count 가 1씩 증가한다. 
 

### 중요도 관리
- [X] **중요도 = [('중요해요' 누적 클릭수) + 조회수] * 감쇄율** 이며, 매일 자정에 갱신된다.
- [X] 감쇄율은 아래와 같으며, 주기별로 감쇄가 이루어진다. 
  ```json
  {
      "decayPeriod": "7", 
      "decayRate": "0.8",
      "threshold": "3", 
      "viewsWeight": "0.5", 
      "clicksWeight": "0.5" 
  }
  ```
- [X] 중요도가 임계값보다 낮은 글 / 답글은 자동으로 삭제된다. 
  - [X] 예를 들어, 작성 시점이 12/5일 인 글을 보자.
    - 12/5 자정 : 조회수 5, '중요해요' : 1 이면, 중요도 = [5 + 1]* 0.8 = 4.8 이다. 
    - 12/6 자정 : 조회수 10, '중요해요' : 3 이면, 중요도 = [10 * 0.5 + 3 * 0.5]* 0.8^2 = 4.16 이다. 
    - 12/7 자정 : 조회수 30, '중요해요' : 5 이면, 중요도 = [20 * 0.5^2 + 5 * 0.5^2] * 0.8^3 = 4.48 이다. 
    - 12/8 자정 : 조회수 40, '중요해요' : 6 이면, 중요도 = [40 * 0.5^3 + 6 * 0.5^3] * 0.8^3 = 2.994 이다. 
    - 12/8 에 글의 중요도가 임계값(3) 이하이므로 글은 자동삭제 된다.

----
## 3. 실행 방법
### 환경
- Server Framework : FastAPI
- Front Framework : Svelte
- python version : 3.10
- node version : v18.17.0
- RDBMS : MySQL 8.0

- backend 
  1. `cd backend`
  2. `pip install -r requirements.txt`
  3. `uvicorn main:app --reload` 

- frontend
  1. `cd frontend`
  2. `npm run dev`
- Running in http://localhost:5173/
----
## 4. 구현 결과

### 시작 페이지

- **글 목록 정렬 기능** 
  - Sort by Views
  - Sort by Help Count
  - Sort by Date
- **중요도 기반 중요하지 않은 글 삭제** 
  - Update Importance Score

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/95633b71-8e88-446f-9539-2c86a4bfd4ee">

</details>





### 회원가입
- users 테이블에 유저 정보 저장
- 입력한 비밀번호는 hash 알고리즘을 이용해 암호화하여 저장

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/4a69bff3-8437-412c-a46d-51ac2fbf98d8">

</details>



### 로그인

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/c845888e-886d-4e13-b81d-d50df3ba7b73">

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/4938da46-7d8f-431a-a552-88c2c74d6754">

</details>




### 글 등록하기 
- 글은 Markdown 형식을 지원해서, Html format 으로 image url 을 삽입하면 이미지가 렌더링 되도록 구현
- Home 에서 글을 누르면 조회수가 1 증가

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/3700ba53-6e41-4f5e-aff2-a459ca6296c7">

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/34d63c2c-76d8-496d-9349-21267c8b5a4a">

</details>



### 글 수정하기 
- 글 수정하기 버튼은 글 작성한 본인만 보이도록 설정

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/ad755af0-ffcf-41ff-bf90-485aed55084d">

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/10ad6fc6-049a-4fe8-985b-9d106b6b3b1b">


</details>



### 추천 누르기
- 추천 버튼을 누르면 추천수가 1 추가

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/4553df3e-f6be-45d9-9eb4-2a74f518068e">

</details>



### 글 삭제하기
- 글 삭제하기 버튼은 글 작성한 본인만 보이도록 설정

<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/c3b50022-2ab4-4876-8e71-a5f77440ff86">

</details>



### 답글 달기
- 답글에도 추천을 누를 수 있음


<details>
    <summary>구현 화면</summary>

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/633609df-2e57-4a01-96f6-5fed6d54ead9">

<img width="1168" alt="image" src="https://github.com/ddoddii/ddoddii.github.io/assets/95014836/ca0e02b7-183b-47ea-a909-dfb85ddac886">

</details>



