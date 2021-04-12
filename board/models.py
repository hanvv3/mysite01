# from django.db import models
from MySQLdb import connect, OperationalError, ProgrammingError
from MySQLdb.cursors import DictCursor


def insert_new_post(title, contents, user_no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행 / now(), g_no = ifnull((select max(g_no) from board as a),0)+1
        sql = "insert into board values(null, %s, %s, 0, now(), ifnull((select max(g_no) from board as a),0)+1, 1, 0, %s)"
        cursor.execute(sql, (title, contents, user_no))

        # commit (transaction종료, db내부 변경 사항을 확정)
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

    except OperationalError as e:
        print(f'error: {e}')


def insert_reply(title, contents, g_no, o_no, depth, user_no):
    try:
        # 연결
        db = conn()
        # cursor 생성
        cursor = db.cursor()

        # SQL 실행 / now(), g_no = ifnull((select max(g_no) from board as a),0)+1
        # 계층형의 반대 답글순서는 이렇게 테스트 해보길: o_no = (select max(o_no) from board as a where g_no = %s)+1
        sql1 = '''
        update board 
           set o_no = o_no + 1 
         where g_no = %s
           and o_no >= %s'''
        sql2 = "insert into board values(null, %s, %s, 0, now(), %s, %s, %s, %s)"
        # sql순서를 반대로 하고 and에  and no != (select max(no))를 사용하면 recursive처럼 되는것 같다.
        cursor.execute(sql1, (g_no, o_no))
        cursor.execute(sql2, (title, contents, g_no, o_no, depth, user_no))

        # commit (transaction종료, db내부 변경 사항을 확정)
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

    except OperationalError as e:
        print(f'error: {e}')


def listall():
    try:
        db = conn()
        cursor = db.cursor(DictCursor)

        sql = '''
          select a.no as ano, b.no as bno, title, name, hit, reg_date as regdate, depth
            from board a, user b
           where a.user_no = b.no
        order by g_no desc, o_no asc, depth asc'''
        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results

    except ProgrammingError as e:
        print(f'error: {e}')


def listbyno(no):
    try:
        db = conn()
        cursor = db.cursor(DictCursor)

        sql = '''
          select a.no as ano, title, contents, b.no as bno, name, hit, reg_date as regdate, g_no, o_no, depth
            from board a, user b
           where a.user_no = b.no
             and a.no = %s'''
        cursor.execute(sql, (no,))

        result = cursor.fetchone()

        cursor.close()
        db.close()

        return result

    except ProgrammingError as e:
        print(f'error: {e}')


def deleteby_no(no):
    try:
        db = conn()
        cursor = db.cursor()

        sql = 'delete from board where no = %s'
        cursor.execute(sql, (no,))

        db.commit()

        cursor.close()
        db.close()

    except ProgrammingError as e:
        print(f'error: {e}')


def findby_no_and_pw(ano, password):
    try:
        db = conn()
        cursor = db.cursor(DictCursor)
        sql = '''
        select b.no as bno, name, email, gender
          from board a, user b
         where a.user_no = b.no
           and a.no = %s
           and password = %s'''
        cursor.execute(sql, (ano, password))

        result = cursor.fetchone()          # 하나만 받는 함수

        cursor.close()
        db.close()

        return result
    except OperationalError as e:
        print(f'error: {e}')


def update(ano, title, contents):
    try:
        db = conn()
        cursor = db.cursor()

        # %s에 들어올 값은 이미 string이기 때문에 ""가 필요 없음.
        sql = '''
        update board
           set title = %s, contents = %s
         where no = %s'''
        cursor.execute(sql, (title, contents, ano))

        db.commit()

        cursor.close()
        db.close()

        print("ok")
    except ProgrammingError as e:
        print(f'error: {e}')


def conn():
    return connect(
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')