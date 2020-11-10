import config
import pymysql

from flask      import Flask, jsonify
from flask_cors import CORS

from view       import SellerView, ProductView
from model      import SellerDao, ProductDao
from service    import SellerService, ProductService

from exceptions import LoginError, SignUpError

class Services:
    pass

def create_app(test_config = None):
    app       = Flask(__name__)
    app.debug = True
    
    CORS(app, resources={r'*': {'origins': '*'}})

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
    
    # Persistance layer
    seller_dao = SellerDao()
    product_dao = ProductDao()
    # Business layer
    services = Services
    services.seller_service = SellerService(seller_dao, app.config)
    services.product_service = ProductService(product_dao, app.config)
    # Endpoint
    SellerView.create_endpoints(app, services)
    ProductView.create_endpoints(app, services)

    #Error Handler
    @app.errorhandler(Exception)
    def handle_error(error):
        return jsonify(error.error_response)

    return app
