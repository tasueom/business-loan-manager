# Business Loan Manager

Flask 기반 기업 대출 정보 관리 시스템입니다. OCR(pytesseract)을 활용한 이미지에서 사업자 정보 추출, CSV 업로드, MySQL 데이터베이스 저장, Chart.js 시각화를 지원합니다.

## 주요 기능

- 📸 **OCR 이미지 인식**: 사업자 등록증 이미지에서 회사명, 사업자등록번호, 연락처, 주소 자동 추출
- 📊 **대출 정보 관리**: 대출 금액, 기간, 연 이율을 입력하여 총 상환액 자동 계산
- 📁 **CSV 일괄 업로드**: CSV 파일을 통한 대량 데이터 입력
- 💾 **MySQL 데이터베이스**: 대출 정보를 MySQL에 저장 및 관리
- 📈 **데이터 시각화**: Chart.js를 활용한 대출 정보 차트 시각화
- 📄 **Excel 다운로드**: 저장된 대출 정보를 Excel 파일로 내보내기
- 📑 **페이징**: 대출 목록 페이지네이션 지원 (페이지당 10건)

## 기술 스택

- **Backend**: Flask (Python)
- **Database**: MySQL
- **OCR**: pytesseract (Tesseract OCR)
- **Data Processing**: pandas, openpyxl
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js

## 설치 및 설정

### 1. 필수 요구사항

- Python 3.7 이상
- MySQL Server
- Tesseract OCR (Windows: [다운로드](https://github.com/UB-Mannheim/tesseract/wiki))

### 2. Tesseract OCR 설치 (Windows)

1. [Tesseract OCR 설치 파일](https://github.com/UB-Mannheim/tesseract/wiki) 다운로드 및 설치
2. 기본 설치 경로: `C:\Program Files\Tesseract-OCR`
3. 한국어 언어팩 포함 확인

### 3. 프로젝트 설정

```bash
# 저장소 클론
git clone <repository-url>
cd business-loan-manager

# 가상환경 생성 및 활성화 (선택사항)
python -m venv venv
venv\Scripts\activate  # Windows

# 필요한 패키지 설치
pip install flask mysql-connector-python pytesseract pillow pandas openpyxl
```

### 4. 데이터베이스 설정

`db.py` 파일에서 MySQL 연결 정보를 수정하세요:

```python
base_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password"  # 실제 비밀번호로 변경
}
```

### 5. 데이터베이스 초기화

```bash
python db.py
```

이 명령어는 `loandb` 데이터베이스와 `loans` 테이블을 자동으로 생성합니다.

## 실행 방법

```bash
python app.py
```

서버가 실행되면 브라우저에서 `http://localhost:5000`으로 접속하세요.

## 프로젝트 구조

```
business-loan-manager/
├── app.py                 # Flask 애플리케이션 메인 파일
├── db.py                  # MySQL 데이터베이스 연결 및 쿼리 함수
├── service.py             # OCR, 계산, 파일 처리 등 비즈니스 로직
├── README.md              # 프로젝트 문서
├── sample.csv             # CSV 업로드 샘플 파일
├── static/
│   ├── style.css          # 스타일시트
│   └── chart.js           # Chart.js 라이브러리
└── templates/
    ├── layout.html        # 기본 레이아웃 템플릿
    ├── index.html         # 홈 페이지
    ├── upload.html         # 이미지 업로드 및 정보 입력 페이지
    ├── upload_csv.html     # CSV 업로드 페이지
    ├── list.html          # 대출 정보 목록 페이지 (페이징 포함)
    └── chart.html         # 차트 시각화 페이지
```

## 주요 라우트

- `GET /` - 홈 페이지
- `GET/POST /upload` - 이미지 업로드 및 OCR 정보 추출
- `POST /add` - 대출 정보 추가
- `GET /list` - 대출 정보 목록 (페이징 지원)
- `GET /chart` - 대출 정보 차트 시각화
- `GET/POST /upload_csv` - CSV 파일 업로드
- `GET /save_excel` - Excel 파일 다운로드

## CSV 파일 형식

CSV 파일은 다음 컬럼을 포함해야 합니다:

- 회사명
- 사업자등록번호
- 연락처
- 주소
- 대출금액
- 대출기간 (개월)
- 연이율 (%)

## 데이터베이스 스키마

### loans 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | INT | 기본키 (자동 증가) |
| company_name | VARCHAR(100) | 회사명 |
| biz_no | VARCHAR(20) | 사업자 등록번호 |
| phone | VARCHAR(20) | 연락처 |
| address | VARCHAR(200) | 주소 |
| loan_amount | BIGINT | 대출 금액 |
| term_months | INT | 대출 기간 (개월) |
| annual_rate | DECIMAL(5,2) | 연 이율 (%) |
| total_repayment | BIGINT | 총 상환액 |
| created_at | TIMESTAMP | 등록 일시 (자동) |

## 주요 기능 설명

### OCR 이미지 인식

사업자 등록증 이미지를 업로드하면 pytesseract를 사용하여 다음 정보를 자동으로 추출합니다:
- 회사명
- 사업자 등록번호
- 연락처
- 주소

### 총 상환액 계산

복리 계산식을 사용하여 총 상환액을 자동 계산합니다:
```
총 상환액 = 대출 금액 × (1 + 연 이율 / 100) ^ (대출 기간 / 12)
```

### 페이징

대출 목록은 페이지당 10건씩 표시되며, 페이지 번호를 클릭하여 이동할 수 있습니다.

## 라이선스

이 프로젝트는 개인 학습 및 포트폴리오 목적으로 제작되었습니다.