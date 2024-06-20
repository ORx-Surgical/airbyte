from base64 import b64encode
import hashlib
import base64
import os
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup

import requests


class OscarProAuthentication:
    def __init__(self, config):
        self.config = config
        self.code_challenge_pair = self.generate_code_challenge_pair()

    def get_access_token(self) -> str:
        code = self.get_authorization_code()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': self.basic_auth(),
        }
        
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.config['clinic_redirect_uri'],
            'code_verifier': self.code_challenge_pair[0],
        }
        response = requests.post(self.config['oscar_pro_token_url'], data=data, headers=headers)

        return response.json()


    def get_authorization_code(self) -> str:
        session_token = self.get_session_token()

        scopes = [
            'offline_access',

            'user/Patient.read',
            'user/AllergyIntolerance.read',
            'user/Observation.read',
            'user/Condition.read',
            'user/DiagnosticReport.read',
            'user/DocumentReference.read',
            'user/Medication.read',
            'user/Procedure.read'
        ]

        params = {
            'sessionToken': session_token,
            'response_type': 'code',
            'response_mode': 'form_post',
            'client_id': self.config['clinic_id'],
            'redirect_uri': self.config['clinic_redirect_uri'],
            'scope': ' '.join(scopes),
            'aud': self.config['oscar_pro_aud'],
            'access_type': 'offline',
            'code_challenge': self.code_challenge_pair[1],
            'code_challenge_method': 'S256',
            'state': '{}'
        }

        url = self.config['oscar_pro_authorization_url'] + urlencode(params)
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        code = soup.find('input', {'name': 'code'}).get('value')

        if not code:
            return f'Invalid Code <{code}>'

        return code


    def get_session_token(self) -> str:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        data = {'username': self.config["username"], 'password': self.config["password"]}
        response = requests.post(self.config['session_token_url'], json=data, headers=headers)
        data = response.json()
        session_token = data['sessionToken']
        return session_token or ''


    
    def base64UrlEncode(self, array_buffer):
        bytes_data = bytearray(array_buffer)
        base64_str = base64.b64decode(bytes_data).decode('utf-8')
        url_safe_base64_str = base64_str.replace('+', '-').replace('/', '_').rstrip('=')
        return url_safe_base64_str
    
    def generate_code_challenge_pair(self) -> tuple:      
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)

        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')
        return (code_verifier, code_challenge)

    
    def basic_auth(self):
        token = b64encode(
            f"{self.config['clinic_id']}:{self.config['clinic_secret']}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'
