import pytesseract
import os
from PIL import Image
import re
from io import BytesIO
import pandas as pd
import db

# Tesseract 실행 파일 경로, 아래 구문은 항상 나와야함
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 한국어 또는 다른 나라 언어팩이 들어있는 위치 지정, tessdata 경로 명시
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"

def extract_business_info(file):
    image = Image.open(file)
    
    custom_config = r'-c tessedit_char_blacklist=*=~--"\' --oem 3 --psm 6'
    text_raw = pytesseract.image_to_string(image, lang='kor', config=custom_config)
    
    # 인식된 텍스트를 콘솔에 출력
    print("=== 인식된 텍스트 (원본) ===")
    print(text_raw)
    print("===================")
    
    # 텍스트에서 모든 띄어쓰기 제거 (공백, 탭 등)
    text_no_spaces = re.sub(r'[ \t]+', '', text_raw)
    
    # 줄바꿈은 유지하여 줄 단위로 처리
    lines = text_no_spaces.strip().split('\n')
    
    print("=== 띄어쓰기 제거 후 텍스트 ===")
    print(text_no_spaces)
    print("===================")
    
    # 회사명: 첫 줄
    company_name = lines[0].strip() if lines else ""
    
    # 주소: "주소"로 시작하는 줄에서 주소 이후 내용 추출
    address = ""
    for line in lines:
        if line.strip().startswith('주소'):
            # "주소" 또는 "주소:" 이후의 내용 추출
            address = re.sub(r'^주소:?', '', line.strip())
            break
    
    # 연락처: "연락처"로 시작하는 줄에서 연락처 이후 내용 추출
    phone = ""
    for line in lines:
        if line.strip().startswith('연락처'):
            # "연락처" 또는 "연락처:" 이후의 내용 추출
            phone = re.sub(r'^연락처:?', '', line.strip())
            break
    
    # 사업자 등록번호: "사업자" 또는 "사업자등록번호"로 시작하는 줄에서 추출
    biz_no = ""
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith('사업자'):
            # "사업자", "사업자등록번호", "사업자 등록번호" 등 이후의 내용 추출
            biz_no = re.sub(r'^사업자(등록번호)?:?', '', line_stripped)
            break
    
    # 이미지를 BytesIO로 변환하여 반환
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return {
        'company_name': company_name,
        'address': address,
        'phone': phone,
        'biz_no': biz_no,
        'image_file': img_byte_arr
    }

def calculate_total_repayment(loan_amount, term_months, annual_rate):
    return int(loan_amount * ((1 + annual_rate / 100) ** (term_months / 12)))

def prepare_chart_data(rows):
    """대출 정보 리스트를 차트용 데이터 구조로 변환합니다."""
    chart_data = {
        'labels': [],  # x 라벨 (ID)
        'values': [],  # y 라벨 (총 상환액)
        'tooltips': []  # 툴팁 정보 (회사명, 주소, 연락처, 사업자번호 등)
    }
    
    for row in rows:
        # row 구조: (id, company_name, biz_no, phone, address, loan_amount, term_months, annual_rate, total_repayment, created_at)
        chart_data['labels'].append(str(row[0]))  # ID를 문자열로
        chart_data['values'].append(int(row[8]) if row[8] else 0)  # 총 상환액 (숫자로 변환)
        
        # 툴팁 정보 딕셔너리
        tooltip = {
            'company_name': row[1] or '',
            'biz_no': row[2] or '',
            'phone': row[3] or '',
            'address': row[4] or '',
            'loan_amount': row[5] or 0,
            'term_months': row[6] or 0,
            'annual_rate': float(row[7]) if row[7] else 0.0,
            'created_at': str(row[9]) if row[9] else ''
        }
        chart_data['tooltips'].append(tooltip)
    
    return chart_data

def upload_csv(file):
    csv_data = pd.read_csv(file, encoding='utf-8-sig')
    for row in csv_data.itertuples(index=False):
        company_name = row.회사명
        biz_no = row.사업자등록번호
        phone = row.연락처
        address = row.주소
        loan_amount = int(row.대출금액)
        term_months = int(row.대출기간)
        annual_rate = float(row.연이율)
        total_repayment = calculate_total_repayment(loan_amount, term_months, annual_rate)
        db.insert_loan(company_name, biz_no, phone, address, loan_amount, term_months, annual_rate, total_repayment)
    print("CSV 파일 업로드 완료")