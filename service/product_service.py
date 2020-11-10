import jwt
import bcrypt
import re
import boto3

from werkzeug.utils import secure_filename

class ProductService:
    # 먼 미래
    EXPIRED_AT = '9999-12-31 23:59:59'

    def __init__(self,product_dao, config):
        self.product_dao = product_dao
        self.config     = config
        # boto3 모듈 클라이언트 생성
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id     = config['S3_ACCESS_KEY'],
            aws_secret_access_key = config['S3_SECRET_KEY']
        )

    # 카테고리 목록
    def product_category(self, conn):
        #1차 카테고리 목록
        categories = self.product_dao.product_first_category(conn)
        category_list = []
        for category in categories:
            #1차카테고리에 속한 2차카테고리 목록
            category_second = self.product_dao.product_second_category(category['id'],conn)
            category_dict = {
                "id"     : category['id'],
                "name"   : category['name'],
                "childs" : category_second
            }
            category_list.append(category_dict)           

        return {"productAdd":{ "categories" : category_list}}                

    # 상품 이미지 업로드 함수
    def upload_image(self, image, filename):
        
        self.s3.upload_fileobj(
            image,
            self.config['S3_BUCKET'],
            filename
        )

        return f"{self.config['S3_BUCKET_URL']}{filename}"

    # 상품 이미지 수정 함수
    def update_product(self, product_data, images, detail_image, account_id,  conn):
        try:
            product_detail_dict = product_data
            product_detail_dict["modifier"] = account_id

            filenames = []
            for i, image in enumerate(images):
                filename = secure_filename(image.filename)
                filenames.append(filename)

            images = [ image for image in images if image != None ]

            detail_info_filename = secure_filename(detail_image.filename)
            detail_image_url     = self.upload_image(detail_image, detail_info_filename)
            close_time           = self.product_dao.now_time(conn)

            product_detail_dict['close_time']             = close_time['now()']
            product_detail_dict['productDetailInfoImage'] = detail_image_url

            self.product_dao.update_product_close_time(product_detail_dict, conn)
            
            update_product = self.product_dao.update_product_detail(product_detail_dict, conn)
            
            PRODUCT_IMAGE_COUNT = 5

            for i in range(1, PRODUCT_IMAGE_COUNT+1):
                if i <= len(images):
                    url = self.upload_image(images[i-1], filenames[i-1])
                else:
                    url = None
                if i is 1:
                    product_image_dict = {
                        'url' : url,
                        'order' : i,
                        'is_main' : 1,
                        'product_id' : product_detail_dict['product_id']
                    }
                    self.product_dao.update_product_image(product_image_dict,conn)
                else:
                    product_image_dict = {
                        'url' : url,
                        'order' : i,
                        'is_main' : 0,
                        'product_id' : product_detail_dict['product_id']
                    }
                    self.product_dao.update_product_image(product_image_dict,conn)

        except Exception as e:
            raise e
            
    # 상품 등록 함수
    def add_product(self, product_data, images ,detail_image, account_id, conn):
        try:
            # 상품 기본정보들
            product_dict        = dict()
            
            product_detail_dict = product_data
            # 시험용 데이터
            product_dict['account_id']      = account_id
            code_number                     = self.product_dao.get_product_list(conn)
        
            product_dict['code']            = code_number[-1]['id'] + 1
            product_dict['number']          = code_number[-1]['id'] + 1
            product_detail_dict["modifier"] = account_id
            
            # 상품 등록 후 상품 아이디 반환
            product_id = self.product_dao.create_product(product_dict, conn)
            # 상품 디테일, 이미지 딕셔너리에 상품 아이디 추가
            product_detail_dict['product_id'] = product_id
            filenames = []
            for i, image in enumerate(images):
                filename = secure_filename(image.filename)
                filenames.append(filename)

            detail_info_filename = secure_filename(detail_image.filename)
            detail_image_url = self.upload_image(detail_image, detail_info_filename)

            product_detail_dict['productDetailInfoImage'] = detail_image_url
            self.product_dao.create_product_detail(product_detail_dict, conn)
            
            PRODUCT_IMAGE_COUNT = 5

            for i in range(1, PRODUCT_IMAGE_COUNT+1):
                if i <= len(images):
                    url = self.upload_image(images[i-1], filenames[i-1])
                else:
                    url = None
                if i is 1:
                    product_image_dict = {
                        'url' : url,
                        'order' : i,
                        'is_main' : 1,
                        'product_id' : product_id
                    }
                    self.product_dao.create_product_image(product_image_dict,conn)
                else:
                    product_image_dict = {
                        'url' : url,
                        'order' : i,
                        'is_main' : 0,
                        'product_id' : product_id
                    }
                    self.product_dao.create_product_image(product_image_dict,conn)
                  
        except Exception as e:
            raise e

    # 상품 상세 정보 함수
    def product_detail(self, product_id, conn):
        product_detail_dict = dict()
        product_detail_dict['product_id'] = product_id
        product_detail_dict['expired_at'] = ProductService.EXPIRED_AT # 가장 최신에 수정한 상품 디테일의 만료날짜를 먼 미래 값으로 설정함
        product_detail       = self.product_dao.get_product_detail(product_detail_dict, conn)
        product_detail_image = self.product_dao.get_product_image(product_detail_dict,conn)
        return {"product_info" : product_detail, "product_image" : product_detail_image}
