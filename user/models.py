from django.db import models
from MySQLdb import connect, OperationalError, ProgrammingError
from MySQLdb.cursors import DictCursor

'''
def deleteby_no_and_pw(no, password):
    try:
        db = conn()

        cursor = db.cursor()

        sql = f"delete from user where no = %s and password = %s"
        count = cursor.execute(sql, (no, password))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except ProgrammingError as e:
        print(f'error: {e}')
'''


def findbyno(no):
    try:
        db = conn()
        cursor = db.cursor(DictCursor)
        sql = '''
        select no, name, email, gender
          from user 
         where no = %s'''
        cursor.execute(sql, (no,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        return result

    except OperationalError as e:
        print(f'error: {e}')


def findby_email_and_password(email, password):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''
        select no, name, email, gender
          from user
         where email = %s
           and password = %s'''
        cursor.execute(sql, (email, password))

        # 결과 받아오기
        result = cursor.fetchone()          # 하나만 받는 함수

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return result

    except OperationalError as e:
        print(f'error: {e}')


def insert(name, email, password, gender):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'insert into user values(null, %s, %s, %s, %s, now())'
        count = cursor.execute(sql, (name, email, password, gender))   # 1:성공/0:실패

        # commit (transaction종료, db내부 변경 사항을 확정)
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 변경 성공/실패
        return count == 1          # True/False

    except OperationalError as e:
        print(f'error: {e}')


def update(name, password, gender, no):
    try:
        db = conn()
        cursor = db.cursor()
        if password is '':
            sql = '''
            update user
               set name = %s, gender = %s
             where no = %s'''
            cursor.execute(sql, (name, gender, no))
        else:
            sql = '''
            update user
               set name = %s, password = %s, gender = %s
             where no = %s'''
            cursor.execute(sql, (name, password, gender, no))
        db.commit()
        cursor.close()
        db.close()
    except OperationalError as e:
        print(f'error:{e}')


def conn():
    return connect(
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')