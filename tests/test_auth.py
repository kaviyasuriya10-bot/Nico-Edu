import sys
sys.path.insert(0,'backend')
from utils.security import hash_password,verify_password,create_token,decode_token
def test_passwords_are_hashed():
 h=hash_password('SecurePass123');assert h != 'SecurePass123' and verify_password('SecurePass123',h)
def test_jwt_has_identity_and_role():
 d=decode_token(create_token(7,'student'));assert d['sub']=='7' and d['role']=='student'
