## 이메일 분류 및 스케쥴링 웹사이트 프로젝트


<br>

### 1. 필수 라이브러리 설치
```
pip install -r requirements.txt
```
<br>

### 2. Api 키 필요
.env파일 생성 후

OPENAI_API_KEY="openai api"

ENCRYPTION_KEY="fernet key"

auth_key = "deepl api"

EMAIL_ADDRESS = "admin email address"

EMAIL_PASSWORD = "admin email passwd"

추가
<br>

### 3. 실행
```
python manage.py runserver
```
<br>

### 4. 접속
127.0.0.1로 접속


<br>

### Truble shooting
1. django-mysql 연동 시 비밀번호 기억 안남...
   - root 계정 삭제 후 새로 계정 만들어즘... 비밀번호를 잘 기억하자..
   - programs files 에 있다 보니 prompt 창을 관리자 권한으로 열어줘야함!
   - root 계정 삭제 안하고 초기화 후 변경하려고 했는데, 뭐가 문제인지는 모르겠는데 안돼...

2. 폰트 적용 안되어서 poppins를 Noto Sans KR로 변경
