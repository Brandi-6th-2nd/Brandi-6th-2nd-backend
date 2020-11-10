import jwt
import bcrypt
import json
import config
import boto3
import pymysql

from flask      import request, jsonify, g
from connection import get_connection
from exceptions import LoginError, SignUpError
from functools  import wraps

class SellerView:    

    def create_endpoints(app, services):
        seller_service = services.seller_service
        ACCOUNT_TYPE = {'MASTER' : 1, 'SELLER' : 2}
        
        def authorize(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not 'Authorization' in request.headers:
                    return {'message' : 'ACCESS NOT ALLOWED'}, 401
                access_token = request.headers.get('Authorization')
                try:
                    payload = jwt.decode(access_token,  config.JWT_SECRET_KEY, config.ALGORITHM)
                except jwt.InvalidTokenError:
                    return {'message' : 'INVALID TOKEN'}, 400
                g.user = payload['account_id']
                g.auth = payload['account_type_id']
                return f(*args, **kwargs)
            return decorated_function

        @app.route("/sign_up", methods=['POST'])
        def sign_up():
            """
            회원가입 API
                API 작성: 문성호
            Args:
                account            : 계정명
                password           : 비밀번호
                kor_name           : 셀러명
                eng_name           : 셀러명(영문)
                center_phone       : 고객센터 전화번호
                seller_category    : 셀러 속성 id
                phone_number       : 담당자 전화번호
            Returns:
                {message: result message}, http status code
            Exceptions:
                KeyError  : JSON Key value가 잘못 입력되었을 때 에러처리.
                TypeError : NoneType이 입력되었을 때 에러처리.
            """
            try:
                conn = get_connection()  
                new_seller = request.get_json()
                message = seller_service.create_new_seller(new_seller, conn)

            except KeyError:
                raise SignUpError('B001')

            except TypeError:
                raise SignUpError('B002')

            except pymysql.IntegrityError:
                conn.rollback()
                return jsonify({'message' : '계정 이미 존재함'}), 400

            except Exception as e:
                conn.rollback()
                return jsonify({'message' : '{}'.format(e)}), 400
            else:
                conn.commit()   
                conn.close() 
                return jsonify({'message':message, "status" : 200}) 
        
        @app.route("/sign_in", methods=['POST'])
        def sign_in():
            """
            로그인 API
                API 작성: 이도길
            Args:
                user_data       : 로그인에 입력된 회원 정보
                authorized_user : 인증된 유저
            Returns:
                {message: result message}, http status code
            Exceptions:
                KeyError  : JSON Key value가 잘못 입력되었을 때 에러처리.
                TypeError : NoneType이 입력되었을 때 에러처리.
            """
            # 1. JSON으로 받은 데이터 예외처리.
            try:
                conn      = get_connection()
                user_data = request.json

            # 2. 로그인 및 토큰 발행.
                authorized_user = seller_service.login(user_data, conn)
            
            # 3. 계정이 없으면 에러 반환, 있으면 user_id와 token 발행.
                if authorized_user is None:
                    return jsonify({'message' : '유효하지 않은 회원정보'}), 401

                return jsonify(authorized_user), 200 

            except KeyError: 
                raise LoginError('A001')

            except TypeError:
                raise LoginError('A002')

            except Exception as e:
                raise e

            else:
                conn.commit()
                
            finally:
                conn.close()  

        @app.route("/master/sellerList", methods=['GET', 'POST'])
        def seller_list():
            try:
                conn    = get_connection()
                filter_data = dict(request.args)
                print(filter_data)
                if request.method == 'GET':  
                    data = seller_service.master_getSellerList(filter_data, conn)

            except KeyError:
                conn.rollback()
                return jsonify({'message' : '키 에러'}), 400
            
            except TypeError:
                conn.rollback()
                return jsonify({'message' : '타입 에러'}), 400

            except pymysql.IntegrityError:
                conn.rollback()
                return jsonify({'message' : '계정 정보 중복'}), 400

            except Exception as e:
                conn.rollback()
                return jsonify({'message' : 'error {}'.format(e)}), 400
            else:
                conn.commit()    
                return jsonify(data), 200 
            finally:
                conn.close() 

        # # 마스터 - 셀러 아이디 누르고 들어가면 셀러 정보 수정하는 페이지 (GET, PUT 다 해야 함)
        @app.route("/master/sellerInfo/<seller_id>", methods=['GET', 'POST'])
        def master_sellerInfoPage(seller_id):
            try:
                conn = get_connection()
                seller_img = request.files
                seller_data = request.form
                
                if request.method == 'GET':
                    seller_info = seller_service.master_getSellerInfo(seller_id, conn)
                if request.method == 'POST':
                    seller_info = seller_service.master_updateSellerInfo(seller_id, seller_img, seller_data, conn)

            except Exception as e:
                conn.rollback()
                return jsonify({'message' : 'error {}'.format(e)}), 400
            else:
                conn.commit()    
                return jsonify({'data' : seller_info}), 200 
            finally:
                conn.close() 
