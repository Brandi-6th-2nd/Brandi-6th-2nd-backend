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

class ProductAddError(Exception):
    error_dict = dict()
    error_dict['ERROR'] = {'message' : '알수없는 에러', 'status_code' : 400}
    error_dict['PA001'] = {'message' : '상품등록에 비유효한 키값 전송', 'status_code' : 400}
    error_dict['PA002'] = {'message' : '상품등록에 빈값 전송', 'status_code' : 400}
    error_dict['PA003'] = {'message' : '상세 상품정보 이미지 등록이 필요합니다.', 'status_code' : 400}
    error_dict['PA004'] = {'message' : '이미지 순서가 맞지 않습니다.', 'status_code' : 400}
    error_dict['PA005'] = {'message' : '메인 이미지를 등록해주세요', 'status_code' : 400}
    def __init__(self, code):
        if code in ProductAddError.error_dict:
            self.error_response = ProductAddError.error_dict[code]
        else:
            self.error_response = ProductAddError.error_dict['ERROR']

class ProductUpdateError(Exception):
    error_dict = dict()
    error_dict['ERROR'] = {'message' : '알수없는 에러', 'status_code' : 400}
    error_dict['PU001'] = {'message' : '상품수정에 비유효한 키값 전송', 'status_code' : 400}
    error_dict['PU002'] = {'message' : '상품수정에 빈값 전송', 'status_code' : 400}
    error_dict['PU003'] = {'message' : '상세 상품정보 이미지 등록이 필요합니다.', 'status_code' : 400}
    error_dict['PU004'] = {'message' : '이미지 순서가 맞지 않습니다.', 'status_code' : 400}
    error_dict['PU005'] = {'message' : '메인 이미지를 등록해주세요', 'status_code' : 400}
    def __init__(self, code):
        if code in ProductUpdateError.error_dict:
            self.error_response = ProductUpdateError.error_dict[code]
        else:
            self.error_response = ProductUpdateError.error_dict['ERROR']

class ValidationError(Exception):
    error_dict = dict()
    error_dict['ERROR'] = {'message' : '알수없는 에러', 'status_code' : 400}
    error_dict['V001'] =  {'message'  : '판매여부 (0, 1) 이외의 값이 전송되었습니다.', 'status_code' : 400}
    error_dict['V002'] =  {'message'  : '전시여부 (0, 1) 이외의 값이 전송되었습니다.', 'status_code' : 400}
    def __init__(self, code):
        if code in ValidationError.error_dict:
            self.error_response = ValidationError.error_dict[code]
        else:
            self.error_response = ValidationError.error_dict['ERROR']
