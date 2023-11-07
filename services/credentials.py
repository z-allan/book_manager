import asyncio
import jwt
from extra_streamlit_components import CookieManager
from streamlit import secrets
from services import DatabaseConnection

class Credentials:
    
    @staticmethod
    def criar_cookie(p_value, p_expiration):
        CookieManager(1).set(cookie=secrets.cookie.name, val=p_value, expires_at=p_expiration)
    
    @staticmethod
    async def retornar_cookie():
        cookie = CookieManager(0).get(cookie=secrets.cookie.name)
        await asyncio.sleep(1)
        return cookie

    @staticmethod
    def remover_cookie():
        CookieManager(3).delete(cookie=secrets.cookie.name)
        Credentials.close_db()
    
    @staticmethod
    def close_db():
        DatabaseConnection(close=True)
    
    @staticmethod
    def criar_jwt(p_payload):
        return jwt.encode(p_payload, secrets.jwt.key, algorithm="HS256")
    
    @staticmethod
    def verificar_jwt(p_token):
        try:
            result = jwt.decode(p_token, secrets.jwt.key, algorithms="HS256")
        except Exception as e:
            print(e)
            result = {'user':''}
        finally:
            return result

