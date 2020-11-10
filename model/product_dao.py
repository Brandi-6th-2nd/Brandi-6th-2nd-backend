import pymysql

class ProductDao:
    # 상품 리스트 가져오기
    def get_product_list(self, conn):
        sql = """
            select 
                *
            from
                products
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
        
    # 상품 이미지 가져오기
    def get_product_image(self, product_detail_dict, conn):
        sql = """
            select
                url, `order`
            from
                products_images
            where
                product_id = %(product_id)s
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, product_detail_dict)
            return cursor.fetchall()

    # 1차 카테고리
    def product_first_category(self, conn):
        sql = """
                SELECT id, name
                FROM first_categories;
            """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    # 2차 카테고리
    def product_second_category(self, first_category_id, conn):
        sql = """
                SELECT id,name,FIRST_CATEGORY_ID 
                FROM second_categories
                where first_category_id = %s;
            """
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, first_category_id)
            return cursor.fetchall()

    #1. 상품 등록
    def create_product(self, product_dict, conn):
        print(product_dict)
        sql = """
                INSERT INTO products (
                    account_id,
                    code,
                    number
                ) VALUES (
                    %(account_id)s,
                    %(code)s,
                    %(number)s
                );
            """
        with conn.cursor() as cursor:
            cursor.execute(sql, product_dict)
        # 등록된 상품 아이디 값 반환
        return cursor.lastrowid

    #2. 상품 디테일 등록
    def create_product_detail(self, product_detail_dict, conn):
        print(product_detail_dict['sellOption'])
        sql = """
            INSERT INTO products_details (
                product_id,
                name,
                is_sold,
                is_display,
                description,
                detail_description,
                first_category_id,
                second_category_id,
                modifier,
                manufacture_company,
                manufacture_date,
                manufacture_country
            ) VALUES (
                %(product_id)s,
                %(productName)s,
                %(sellOption)s,
                %(displayOption)s,
                %(productDesc)s,
                %(productDetailInfoImage)s,
                %(currentFirstCategory)s,
                %(currentSecondCategory)s,
                %(modifier)s,
                %(manufacturer)s,
                %(manufactureDate)s,
                %(countryOption)s
            );
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, product_detail_dict)

    # 상품 이미지 추가
    def create_product_image(self, product_image_dict, conn):
        print(product_image_dict)
        sql = """
            INSERT INTO products_images (
                url,
                `order`,
                is_main,
                product_id
            ) VALUES (
                %(url)s,
                %(order)s,
                %(is_main)s,
                %(product_id)s
            );
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, product_image_dict)

    # 선분이력 close_time 수정
    def update_product_close_time(self, product_detail_dict, conn):
        sql = """
            UPDATE 
                products_details
            SET
                expired_at = %(close_time)s
            WHERE
                product_id = %(product_id)s
                and 
                expired_at = '9999-12-31 23:59:59';
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql,product_detail_dict)
            return cursor.fetchone()

    # 현재 시간 가져오기
    def now_time(self, conn):
        sql = """
            SELECT now()
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    # 상품 상세 수정
    def update_product_detail(self, product_detail_dict, conn):
        sql = """
            INSERT INTO products_details (
                product_id,
                name,
                is_sold,
                is_display,
                description,
                detail_description,
                first_category_id,
                second_category_id,
                modifier,
                manufacture_company,
                manufacture_date,
                manufacture_country,
                created_at
            ) VALUES (
                %(product_id)s,
                %(productName)s,
                %(sellOption)s,
                %(displayOption)s,
                %(productDesc)s,
                %(productDetailInfoImage)s,
                %(currentFirstCategory)s,
                %(currentSecondCategory)s,
                %(modifier)s,
                %(manufacturer)s,
                %(manufactureDate)s,
                %(countryOption)s,
                %(close_time)s
            );
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, product_detail_dict)
            return cursor.fetchall()

    # 상품 이미지 수정
    def update_product_image(self, product_image_dict, conn):
        sql = """
            UPDATE 
                products_images 
            SET
                url = %(url)s,
                `order` = %(order)s,
                is_main = %(is_main)s,
                product_id = %(product_id)s
            WHERE
                product_id = %(product_id)s
            AND
                `order` = %(order)s;
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, product_image_dict)
