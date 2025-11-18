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
    """데이터베이스를 생성하고 성공 여부를 반환합니다."""
    try:
        conn = mysql.connector.connect(**base_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
        return False

def create_table():
    """테이블을 생성하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
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
        return True
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        # 리소스 정리: 예외 발생 여부와 관계없이 항상 실행
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # 데이터베이스 생성이 성공했을 때만 테이블 생성 시도
    if create_database():
        if create_table():
            print("Database and table created successfully!")
        else:
            print("Table creation failed.")
    else:
        print("Cannot create table: database creation failed.")