import mysql.connector

base_config = {
    "host": "localhost",   # MySQL 서버 주소 (로컬)
    "user": "root",        # MySQL 계정
    "password": "1234"     # MySQL 비밀번호
}

# 사용할 데이터베이스 이름
DB_NAME = "loandb"

table_name = "loans"

# 커넥션과 커서 반환하는 함수
def get_conn():
    return mysql.connector.connect(**base_config, database=DB_NAME)

def create_database():
    conn = mysql.connector.connect(**base_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    cursor.close()
    conn.close()

def create_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    company_name VARCHAR(100) NOT NULL,
                    biz_no VARCHAR(20) NOT NULL,
                    phone VARCHAR(20),
                    address VARCHAR(200),
                    loan_amount BIGINT NOT NULL,
                    term_months INT NOT NULL,
                    annual_rate DECIMAL(5,2) NOT NULL,
                    total_repayment BIGINT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        create_database()
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
    try:
        create_table()
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")