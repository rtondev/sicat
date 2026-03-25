import requests
from typing import Optional, Dict
from app.database import settings

class SUAPClient:
    def __init__(self):
        self.base_url = settings.suap_api_url
        self.api_url = f"{self.base_url}/api"
    
    def validar_credenciais(self, matricula: str, senha_suap: str) -> Optional[Dict]:
        try:
            token_response = requests.post(
                f"{self.api_url}/token/pair",
                json={
                    "username": matricula,
                    "password": senha_suap
                },
                timeout=10
            )
            
            if token_response.status_code != 200:
                return {"error": "Credenciais do SUAP inválidas"}
            
            token_data = token_response.json()
            access_token = token_data.get("access")
            
            if not access_token:
                return {"error": "Erro ao obter token do SUAP"}
            
            user_response = requests.get(
                f"{self.api_url}/rh/eu/",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                timeout=10
            )
            
            if user_response.status_code != 200:
                return {"error": "Erro ao buscar dados do usuário no SUAP"}
            
            user_data = user_response.json()
            
            return {
                "cpf": user_data.get("cpf", ""),
                "matricula": matricula,
                "nome_completo": user_data.get("nome_registro") or user_data.get("nome", ""),
                "email": user_data.get("email_preferencial") or user_data.get("email", ""),
                "campus": user_data.get("campus", ""),
                "curso": user_data.get("curso", ""),
                "tipo_usuario": user_data.get("tipo_usuario", "")
            }
            
        except requests.exceptions.Timeout:
            return {"error": "Timeout ao conectar com o SUAP"}
        except requests.exceptions.ConnectionError:
            return {"error": "Erro de conexão com o SUAP"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro ao conectar com o SUAP: {str(e)}"}
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}

