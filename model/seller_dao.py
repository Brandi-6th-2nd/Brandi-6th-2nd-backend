import pymysql
from exceptions import LoginError

class SellerDao:
    def insert_account_data(self, sellerData, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query = """ 
                INSERT INTO accounts(
                    account,
                    password
                )
                VALUES (
                    %(account)s,
                    %(password)s
                )
            """
            affected_row = cursor.execute(query, sellerData)
            if affected_row == 0:
                raise Exception("AccountData 정보 삽입 불가")  
 
    def insert_seller_data(self, sellerData, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:         
            query = """ 
                 INSERT INTO sellers(
                    account_id,
                    kor_name,
                    eng_name,
                    center_phone,
                    seller_category_id
                )
                VALUES (
                    (SELECT id FROM accounts WHERE account = %(account)s),
                    %(kor_name)s,
                    %(eng_name)s,
                    %(center_phone)s,
                    (SELECT id FROM seller_categories WHERE name = %(seller_category)s)
                )
            """      
            affected_row = cursor.execute(query, sellerData)
            if affected_row == 0:
                raise Exception("seller 정보 삽입 불가")  

    def insert_manager_data(self, sellerData, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """ 
                INSERT INTO managers(
                    seller_id,
                    phone_number
                )
                VALUES (
                    (SELECT s.id FROM sellers s INNER JOIN accounts acc ON s.account_id = acc.id
                    WHERE acc.account = %(account)s),
                    %(phone_number)s
                )
                """
            affected_row = cursor.execute(query, sellerData)
            if affected_row == 0:
                raise Exception("manager 정보 삽입 불가") 

    def get_userdata(self, userData, conn):
        sql = """
                 SELECT 
                     id,
                     account,
                     password,
                     account_type_id
                 FROM accounts
                 WHERE account = %(account)s
             """
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql,userData)
            return cursor.fetchone()

    def master_getSellerList(self, filter_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query = """
            SELECT
            s.id           AS id,
            s.kor_name     AS kor_name,
            s.eng_name     AS eng_name,
            s.created_at   AS created_at,
            ss.name        AS status_name,
            sc.name        AS seller_category_name,
            m.name         AS manager_name,
            m.phone_number AS phone_number,
            m.email        AS email, 
            acc.account    AS account
            FROM sellers s
            INNER JOIN accounts AS acc ON s.account_id = acc.id
            INNER JOIN managers AS m ON s.id = m.seller_id
            INNER JOIN sellers_status AS ss ON s.status_id = ss.id
            INNER JOIN seller_categories AS sc ON s.seller_category_id = sc.id

            LIMIT %(offset)s, %(limit)s
            """
            filter_data['offset'] = int(filter_data['offset'])
            filter_data['limit'] = int(filter_data['limit'])
            print(filter_data)
            affected_row = cursor.execute(query, filter_data)
            if affected_row == 0:
                raise Exception("sellerData 존재하지 않음")  

            return cursor.fetchall()

    def get_sellerListCount(self, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query = """
            SELECT COUNT(*) AS count
            FROM sellers
            """
            affected_row = cursor.execute(query)
            if affected_row == 0:
                raise Exception("sellerData 존재하지 않음")  

            return cursor.fetchone()


    def master_getSellerInfo(self, seller_id, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query ="""
            SELECT 
                s.id,
                s.seller_image,
                ss.name AS status_name,
                sc.name AS category_name,
                s.kor_name,
                s.eng_name,
                acc.account,
                s.background_image AS background_image,
                s.intro,
                s.detail_intro,
                m.name AS manager_name,
                m.phone_number AS manager_phone,
                m.email AS manager_email,
                s.post_number,
                s.post_address,
                s.post_detail_address,
                s.center_phone,
                s.delivery_info,
                s.exchange_info

            FROM
                sellers s
            INNER JOIN
                accounts AS acc ON acc.id = s.account_id
            INNER JOIN 
                seller_categories AS sc ON sc.id = s.seller_category_id
            INNER JOIN 
                sellers_status AS ss ON ss.id = s.status_id
            INNER JOIN 
                managers AS m ON m.seller_id = s.id 

            WHERE 
                s.id =%(seller_id)s;
            """


            affected_row = cursor.execute(query, {'seller_id' : seller_id})
            if affected_row == 0:
                raise Exception("sellerData 존재하지 않음")  

            return cursor.fetchone()

    def master_updateSellerInfo(self, seller_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """ 
                UPDATE 
                    sellers AS s 
                INNER JOIN 
                    accounts AS acc ON acc.id = s.account_id
                INNER JOIN 
                    managers AS m ON m.seller_id = s.id
                SET 
                    s.seller_image        = %(seller_image)s,
                    s.background_image    = %(background_image)s,
                    s.kor_name            = %(kor_name)s,
                    s.eng_name            = %(eng_name)s,
                    s.intro               = %(intro)s,
                    s.detail_intro        = %(detail_intro)s,
                    m.name                = %(manager_name)s,
                    m.phone_number        = %(manager_phone)s,
                    m.email               = %(manager_email)s,
                    s.post_number         = %(post_number)s,
                    s.post_address        = %(post_address)s,
                    s.post_detail_address = %(post_detail_address)s,
                    s.delivery_info       = %(delivery_info)s,
                    s.exchange_info       = %(exchange_info)s

                WHERE 
                    s.id = %(seller_id)s; 
                """
            affected_row = cursor.execute(query, seller_data)
            if affected_row == 0:
                raise Exception("master_sellerInfo 업데이트 불가")

    def get_seller_action(self, status_name, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query = """
            SELECT 
            sa.name AS action_name
            
            FROM sellers_status_action AS ssa
            
            INNER JOIN sellers_status AS ss ON ss.id = ssa.status_id
            INNER JOIN sellers_action AS sa ON sa.id = ssa.action_id
            WHERE ss.name = %(status_name)s;
            """
            affected_row = cursor.execute(query, {'status_name' : status_name})
            if affected_row == 0:
                raise Exception("userdata 존재하지 않음")  

            return cursor.fetchall()

    def get_nextStatus(self, seller_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """ 
                SELECT ssa.next_status_id 
                FROM sellers_status_action AS ssa
                WHERE 
                ssa.status_id = (SELECT status_id FROM sellers WHERE sellers.id = %(seller_key_id)s)
                AND 
                ssa.action_id = (SELECT id FROM sellers_action WHERE sellers_action.name = %(action_name)s)
                """
            affected_row = cursor.execute(query, data)
            if affected_row == 0:
                raise Exception("next_status가 없음.")

    def seller_updateSellerStatus(self, seller_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """ 
                UPDATE sellers s
                SET s.status_id = %(next_status_id)s
                WHERE s.id = %(seller_key_id)s 
                """
            affected_row = cursor.execute(query, data)
            if affected_row == 0:
                raise Exception("master_sellerInfo 업데이트 불가")       

    def seller_getSellerInfo(self, seller_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query ="""
            SELECT s.id, s.seller_image,
            ss.name AS status_name,
            sc.name AS category_name,
            s.kor_name, s.eng_name, acc.account, s.background_image AS background_image,
            s.intro, s.detail_intro, m.name AS manager_name, m.phone_number AS manager_phone,
            m.email AS manager_email, s.post_number, s.post_address, s.post_detail_address, s.center_start, s.center_end, s.delivery_info, s.exchange_info

            FROM sellers s
            INNER JOIN accounts AS acc ON acc.id = s.account_id
            INNER JOIN seller_categories AS sc ON sc.id = s.seller_category_id
            INNER JOIN sellers_status AS ss ON ss.id = s.status_id
            INNER JOIN managers AS m ON m.seller_id = s.id 

            WHERE s.id =%(seller_id)s;
            """
            affected_row = cursor.execute(query, seller_data)
            if affected_row == 0:
                raise Exception("userdata 존재하지 않음")  

            return cursor.fetchone()

    def seller_getModifyHistory(self, seller_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
            query ="""
            SELECT smh.id, smh.seller_id, smh.modify_date, ss.name AS status_name
            FROM status_modify_history AS smh
            INNER JOIN sellers AS s
            INNER JOIN sellers_status AS ss
            ON smh.seller_id = s.id AND smh.status_id = ss.id

            WHERE smh.seller_id = %(seller_id)s;
            """
            affected_row = cursor.execute(query, seller_data)
            if affected_row == 0:
                raise Exception("userdata 존재하지 않음")  

            return cursor.fetchall()

    def save_backGroundImage(self, img_url, seller_data, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """ 
                UPDATE sellers AS s
                SET s.background_image
                WHERE s.id = %(seller_id)s 
                """
            affected_row = cursor.execute(query, seller_data)
            if affected_row == 0:
                raise Exception("master_sellerInfo 업데이트 불가")

    def change_pw(self, new_password_data, conn):
        sql = """
            UPDATE 
                accounts
            SET
                password = %(new_password)s
            WHERE
                id = %(account_id)s;
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql,new_password_data)
            
    def get_accountdata(self, userData, conn):
        sql = """
                 SELECT 
                     id,
                     account,
                     password,
                     account_type_id
                 FROM accounts
                 WHERE id = %(account_id)s
             """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql,userData)
            return cursor.fetchone() # 딕셔너리 형태로 결과값 반환
    
