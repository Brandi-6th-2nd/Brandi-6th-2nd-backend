class LoginError(Exception):
    error_dict = dict()
    error_dict['A001'] = {'message' : '로그인에 비유효한 키값 전송', 'status_code' : 400}
    error_dict['A002'] = {'message' : '로그인에 빈값 전송', 'status_code' : 400}
    error_dict['A003'] = {'message' : '로그인 할 유저 정보가 없음', 'status_code' : 400}
    def __init__(self, code):
        if code in LoginError.error_dict:
            self.error_response = LoginError.error_dict[code]
        else: 
            self.error_response = LoginError.error_dict['ERROR']
    
    def __del__(self):
        print('로그인 에러 객체 소멸')

class SignUpError(Exception):    
    error_dict = dict()
    error_dict['ERROR'] = {'message' : '알수없는 에러', 'status_code' : 400}
    error_dict['B001']  = {'message' : '회원가입에 비유효한 키값 전송', 'status_code' : 400}
    error_dict['B002']  = {'message' : '회원가입에 빈값 전송', 'status_code' : 400}
    def __init__(self, code):
        if code in SignUpError.error_dict:
            self.error_response = SignUpError.error_dict[code]
        else:
            self.error_response = SignUpError.error_dict['ERROR']

    def __del__(self):
        print('회원가입 에러 객체 소멸')

class ProductAddError(Exception):
    error_dict = dict()
    error_dict['ERROR'] = {'message' : '알수없는 에러', 'status_code' : 400}
    error_dict['C001']  = {'message' : '상품등록에 비유효한 키값 전송', 'status_code' : 400}
    error_dict['C002']  = {'message' : '상품등록에 빈값 전송', 'status_code' : 400}
    def __init__(self, code):
        if code in ProductAddError.error_dict:
            self.error_response = ProductAddError.error_dict[code]
        else:
            self.error_response = ProductAddError.error_dict['ERROR']

    def __del__(self):
        print('상품등록 에러 객체 소멸')

class ProductUpdateError(Exception):
    error_dict = dict()
    error_dict['ERROR'] = {'message' : '알수없는 에러', 'status_code' : 400}
    error_dict['C001']  = {'message' : '상품수정에 비유효한 키값 전송', 'status_code' : 400}
    error_dict['C002']  = {'message' : '상품수정에 빈값 전송', 'status_code' : 400}
    def __init__(self, code):
        if code in ProductUpdateError.error_dict:
            self.error_response = ProductUpdateError.error_dict[code]
        else:
            self.error_response = ProductUpdateError.error_dict['ERROR']

    def __del__(self):
        print('상품수정 에러 객체 소멸')
