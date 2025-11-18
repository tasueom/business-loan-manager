from flask import Flask, render_template, request, redirect, url_for
import service
import db
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # 이미지 파일에서 정보 추출
            result = service.extract_business_info(file)
            
            # 추출된 정보
            company_name = result['company_name']
            address = result['address']
            phone = result['phone']
            biz_no = result['biz_no']
            image_file = result['image_file']  # BytesIO 객체
            
            # 이미지를 base64로 인코딩하여 HTML에 표시 가능하게 함
            image_file.seek(0)
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            return render_template('upload.html',
                                    company_name=company_name,
                                    address=address,
                                    phone=phone,
                                    biz_no=biz_no,
                                    image_base64=image_base64)
    return render_template('upload.html')

@app.route('/add', methods=['POST'])
def add():
    company_name = request.form['company_name']
    address = request.form['address']
    phone = request.form['phone']
    biz_no = request.form['biz_no']
    loan_amount = int(request.form['loan_amount'])
    term_months = int(request.form['term_months'])
    annual_rate = float(request.form['annual_rate'])
    total_repayment = service.calculate_total_repayment(loan_amount, term_months, annual_rate)
    db.insert_loan(company_name, biz_no, phone, address, loan_amount, term_months, annual_rate, total_repayment)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)