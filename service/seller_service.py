import jwt
import bcrypt
import re
import boto3

from exceptions import LoginError

class SellerService:
    def __init__(self,seller_dao, config):
        # 에러 리스트 딕셔너리로 저장
        self.seller_dao = seller_dao
        self.config     = config
        self.s3         = boto3.client(
            "s3",
            aws_access_key_id       = config['S3_ACCESS_KEY'],
            aws_secret_access_key   = config['S3_SECRET_KEY'] 
        )

    def validator_accountData(self,accountData):
        # 1. 계정 아이디 유효성 검사
        if len(accountData['account']) < 5:
            return 'SHORT_ACCOUNT_LENGTH'
        # 2. 비밀번호가 8자 이상 20자 이하이면서 영어대소문자, 특수문자, 숫자를 포함해야 함.
        if 8 <= len(accountData['password']) <= 20:
            if re.search('[0-9]+', accountData['password']) and re.search('[A-Z]+', accountData['password']) and re.search('[a-z]+', accountData['password']) and re.search('[!@#$%^&*]+',accountData['password']):
                return None
            return 'INVALID_PASSWORD'
        return 'SHORT_PASSWORD_LENGTH'

    def create_new_seller(self, sellerData, conn):
        message = self.validator_accountData({'account' : sellerData['account'], 'password' : sellerData['password']})
        if message is not None :
            raise Exception(message)
        
        sellerData['password'] = bcrypt.hashpw(sellerData['password'].encode('UTF-8'), bcrypt.gensalt())
        self.seller_dao.insert_account_data(sellerData,conn)
        self.seller_dao.insert_seller_data(sellerData,conn)
        self.seller_dao.insert_manager_data(sellerData,conn)
        
        return 'REGISTER_SUCCESS'

    def login(self, userData, conn):
        #1. userData 받아서 해당하는 아이디가 있는지 확인
        try:            
            #2. 있으면 True, 없으면 False를 리턴            
            accountData = self.seller_dao.get_userdata(userData, conn)
            authorized  = accountData and bcrypt.checkpw(userData['password'].encode('UTF-8'),accountData['password'].encode('UTF-8'))
            
            #3. 계정 일치하고, 비밀번호도 일치하면
            if authorized:
                access_token = jwt.encode({'account_id' : accountData['id'], 'account_type_id' : accountData['account_type_id']}, self.config['JWT_SECRET_KEY'], self.config['ALGORITHM'])
                return {
                    'account_id'      : accountData['id'],
                    'token'           : access_token.decode('UTF-8'),
                    'account_type_id' : accountData['account_type_id']
                }
            return None

        except Exception as e:
            raise e          

    def master_getSellerList(self, filter_data, conn):
        seller_list = self.seller_dao.master_getSellerList(filter_data, conn)
        print("seller_list" , seller_list)
        
        data = { 'count' : self.seller_dao.get_sellerListCount(conn)['count'],
            'data' : [{
                'id'                    : seller['id'],
                'account'               : seller['account'],
                'kor_name'              : seller['kor_name'],
                'eng_name'              : seller['eng_name'],
                'manager_name'          : seller['manager_name'],
                'status_name'           : seller['status_name'],
                'manager_phone_number'  : seller['phone_number'],
                'manager_email'         : seller['email'],
                'created_at'            : str(seller['created_at']),
                'seller_category'       : seller['seller_category_name'],
                'action'                : [action['action_name'] for action in self.seller_dao.get_seller_action(seller['status_name'], conn)]
            }for seller in seller_list]
        }
        return data

    def master_getSellerInfo(self, seller_id, conn):
        seller_info = self.seller_dao.master_getSellerInfo(seller_id, conn)
        return seller_info    

    def master_updateSellerInfo(self, seller_id, seller_img, seller_data, conn):
        prof_img = seller_img['profile']
        back_img = seller_img['background']

        self.s3.upload_fileobj(prof_img, self.config['S3_BUCKET'], prof_img.filename, ExtraArgs = {'ContentType' : prof_img.content_type})
        self.s3.upload_fileobj(back_img, self.config['S3_BUCKET'], back_img.filename, ExtraArgs = {'ContentType' : prof_img.content_type})
        
        seller_image = f"{self.config['S3_BUCKET_URL']}{prof_img.filename}"
        background_image = f"{self.config['S3_BUCKET_URL']}{back_img.filename}"
        input_data = {
            "seller_id"             : seller_id,
            "seller_image"          : seller_image,
            "background_image"      : background_image,
            "category_name"         : seller_data['category_name'],
            "kor_name"              : seller_data['kor_name'],
            "eng_name"              : seller_data['eng_name'],
            "intro"                 : seller_data['intro'],
            "detail_intro"          : seller_data['detail_intro'],
            "manager_name"          : seller_data['manager_name'],
            "manager_phone"         : seller_data['manager_phone'],
            "manager_email"         : seller_data['manager_email'],
            "post_number"           : seller_data['post_number'],
            "post_address"          : seller_data['post_address'],
            "post_detail_address"   : seller_data['post_detail_address'],
            "delivery_info"         : seller_data['delivery_info'],
            "exchange_info"         : seller_data['exchange_info']
        }

        update_info = self.seller_dao.master_updateSellerInfo(input_data, conn)
        return {'MESSAGE' : 'SUCCESS'}

    def change_pw(self, new_password_data, conn):
        try:
            # 기존 비밀번호와 입력한 비밀번호가 맞는지 확인하기 위해 기존 데이터를 db에서 가져와 저장
            password_data  = self.seller_dao.get_accountdata(new_password_data, conn)
            # 사용자가 새로 입력한 비밀번호
            new_password = new_password_data['new_password']
            # 새로운 암호를 bcrypt를 사용하여 암호화  
            new_password_data['new_password'] = bcrypt.hashpw(new_password.encode('UTF-8'), bcrypt.gensalt())
            if bcrypt.checkpw(new_password_data['password'].encode('UTF-8'),password_data['password'].encode('UTF-8')):
                # 새로운 패스워드를 database에 저장
                self.seller_dao.change_pw(new_password_data, conn)
            else:
                return jsonify({"message":"비밀번호가 다릅니다"})
        except Exception as e:
            raise e

