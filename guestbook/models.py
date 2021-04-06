from django.db import models
from MySQLdb import connect, OperationalError, ProgrammingError
from MySQLdb.cursors import DictCursor


def insert(name, password, message):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'insert into guestbook values(null, %s, %s, %s, now())'
        count = cursor.execute(sql, (name, password, message))   # 1:성공/0:실패

        # commit (transaction종료, db내부 변경 사항을 확정)
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 변경 성공/실패
        return count == 1          # True/False

    except OperationalError as e:
        print(f'error: {e}')


def deleteby_no_and_pw(no, password):
    try:
        db = conn()

        cursor = db.cursor()

        sql = f"delete from guestbook where no = %s and password = %s"
        count = cursor.execute(sql, (no, password))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except ProgrammingError as e:
        print(f'error: {e}')


def findall():
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''
        select no,
               name,
               message,
               date_format(reg_date, "%Y-%m-%d %p %h:%i:%s") as regdate
          from guestbook order by regdate desc'''
        cursor.execute(sql)

        # 결과 받아오기
        results = cursor.fetchall()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return results

    except OperationalError as e:
        print(f'error: {e}')


def conn():
    return connect(
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')