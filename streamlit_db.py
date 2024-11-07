
#streamlit run C:\Users\USER\Desktop\streamlit_db.py

import streamlit as st
import pymysql
import pandas as pd


def draw_color_cell(x,color):
    color = f'background-color:{color}'
    return color

def get_order_data(name):
    try:
        dbConn = pymysql.connect(user='root', passwd='1234', host='192.168.126.130', db='madang', charset='utf8')
        cursor = dbConn.cursor(pymysql.cursors.DictCursor)
        
        sql = """
        SELECT o.orderid, c.name, b.bookname, o.saleprice, o.orderdate 
        FROM Customer c, Orders o, Book b 
        WHERE c.name=%s AND c.custid=o.custid AND b.bookid=o.bookid;
        """
        cursor.execute(sql, (name,))
        result = cursor.fetchall()
        dbConn.close()

        result_df = pd.DataFrame(result)
        return result_df
    
    except Exception as e:
        st.error(f"데이터베이스 오류: {str(e)}")
        return None
    
def get_customer_data(name):
    try:
        # MySQL 연결 설정
        dbConn = pymysql.connect(user='root', passwd='1234', host='192.168.126.130', db='madang', charset='utf8')
        cursor = dbConn.cursor(pymysql.cursors.DictCursor)
        
        # SQL 쿼리 작성
        sql = """
        SELECT c.custid, c.name, c.address, c.phone, SUM(o.saleprice) AS 총주문금액, count(*) as 구매횟수
        FROM Customer c, Orders o
        WHERE c.name=%s AND c.custid=o.custid
        GROUP BY c.custid, c.name, c.address, c.phone;
        """
        cursor.execute(sql, (name,))
        result = cursor.fetchall()
        dbConn.close()

        result_df = pd.DataFrame(result)

        return result_df
    
    except Exception as e:
        st.error(f"데이터베이스 오류: {str(e)}")
        return None
    
def get_date_data(date):
    try:
        # MySQL 연결 설정
        dbConn = pymysql.connect(user='root', passwd='1234', host='192.168.126.130', db='madang', charset='utf8')
        cursor = dbConn.cursor(pymysql.cursors.DictCursor)
        
        # SQL 쿼리 작성
        sql = """
        SELECT o.orderid, b.bookname, c.name AS 구매자, o.saleprice, o.orderdate
        FROM Customer c
        JOIN Orders o ON c.custid = o.custid
        JOIN Book b ON o.bookid = b.bookid
        WHERE o.orderdate = %s;
        """
        cursor.execute(sql, (date,))
        result = cursor.fetchall()
        dbConn.close()

        result_df = pd.DataFrame(result)
        return result_df
    
    except Exception as e:
        st.error(f"데이터베이스 오류: {str(e)}")
        return None


def main():
    st.title('madangDB 시스템')

    tab1, tab2, tab3 = st.tabs(["주문내역 검색", "고객 정보", "날짜별 구매 내역"])

    with tab1:
        
        name = st.text_input('고객 이름을 입력하세요:', '')

        if name:
            st.write(f"'{name}'의 주문 내역:")
            order_data = get_order_data(name)

            if order_data is not None and not order_data.empty:
                st.dataframe(order_data)
            else:
                st.write("검색된 주문 내역이 없습니다.")

    with tab2:
        tab2.write("this is tab 2")

        name1 = st.text_input('고객 이름 입력하세요:', '')

        if name1:
            st.write(f"'{name1}'의 이용 정보:")
            order_data = get_customer_data(name1)

            if order_data is not None and not order_data.empty:
                st.dataframe(order_data)
            else:
                st.write("검색된 주문 내역이 없습니다.")

    with tab3:
        date = st.date_input('일자별 주문 이력')

        if date:
            st.write(f"'{date}의 주문")
            order_data = get_date_data(date)

            if order_data is not None and not order_data.empty:
                st.dataframe(order_data)
            else:
                st.write("검색된 주문 내역이 없습니다.")




if __name__ == "__main__":
    main()
