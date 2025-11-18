from flask import Flask, render_template, request, redirect, url_for
import service
import db
import base64
import json

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

@app.route('/list', methods=['GET'])
def list():
    loans = db.get_loans()
    return render_template('list.html', loans=loans)

@app.route('/chart', methods=['GET'])
def chart():
    rows = db.get_loans()
    chart_data = service.prepare_chart_data(rows)
    
    # JSON으로 변환하여 전달 (JavaScript에서 사용하기 쉽도록)
    chart_data_json = json.dumps(chart_data, ensure_ascii=False)
    return render_template('chart.html', chart_data_json=chart_data_json)

@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            service.upload_csv(file)
            return redirect(url_for('list'))
    return render_template('upload_csv.html')

if __name__ == '__main__':
    app.run(debug=True)