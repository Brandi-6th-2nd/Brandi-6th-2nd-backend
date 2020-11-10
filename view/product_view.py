import jwt
import bcrypt
import boto3
import json
import config

from flask      import request, jsonify, g
from connection import get_connection
from exceptions import LoginError, ProductAddError, ProductUpdateError
from functools  import wraps

class ProductView:
    
    def create_endpoints(app, services):
        product_service = services.product_service

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
                return f(*args, **kwargs)
            return decorated_function

        @app.route("/product", methods=['GET'])
        def product():
            """
            프로덕트(카테고리 리스트) API
                API 작성: 이도길
            Returns:
                {message: result message}, http status code
            """
            try:
                conn   = get_connection()
                result = product_service.product_category(conn)

                if result:
                    return jsonify(result)

            except Exception as e:
                raise e
                
            finally:
                conn.close() 

        @app.route("/product/<int:product_id>", methods=['PUT'])
        @authorize
        def product_update(product_id):
            """
            상품수정 API
                API 작성: 이도길
            Args:
                product_data : 수정할 상품 데이터
            Returns:
                {message: result message}, http status code
            """
            try:
                conn   = get_connection()
                product_data = dict(request.form)
                product_data['product_id'] = product_id
                detail_image = request.files.get('productDetailInfoImage',None)

                if detail_image:
                    image_range_end = len(request.files)
                else:
                    image_range_end = len(request.files) - 1

                images = []
                for i in range(1,image_range_end):
                    image = request.files.get(f'image_{i}', None)
                    if image is None:
                        return jsonify({'message':'이미지순서 맞춰주시길 바랍니다'})
                    images.append(image)

                product_service.update_product(product_data, images, detail_image, g.user, conn)

            except KeyError: 
                raise ProductUpdateError('C001')

            except TypeError:
                raise ProductUpdateError('C002')

            except Exception as e:
                conn.rollback()
                raise e
                
            else:
                conn.commit()
                return jsonify({"message":"상품 수정 성공"})
            finally:
                
                conn.close() 

        @app.route("/product", methods=['POST'])
        @authorize
        def product_create():
            """
            상품등록 API
                API 작성: 이도길
            Args:
                product_data : 등록할 상품 데이터
            Returns:
                {message: result message}, http status code
            """
            try:
                conn         = get_connection()
                product_data = dict(request.form)
                if request.files:
                    detail_image = request.files.get('productDetailInfoImage',None)
                    if detail_image:
                        image_range_end = len(request.files)
                    else:
                        image_range_end = len(request.files) - 1

                    images = []
                    for i in range(1,image_range_end):
                        image = request.files.get(f'image_{i}', None)
                        if image is None:
                            return jsonify({'message':'이미지순서 맞춰주시기 바랍니다'})
                        images.append(image)
                else:
                    return jsonify({'message':'이미지를 등록해주세요'})

                product_service.add_product(product_data, images, detail_image, g.user, conn)

            except KeyError: 
                raise ProductAddError('C001')

            except TypeError:
                raise ProductAddError('C002')

            except Exception as e:
                conn.rollback()
                raise e

            else:
                conn.commit()
                return jsonify({'message':'상품 등록 성공'}), 200

            finally:
                conn.close()  
