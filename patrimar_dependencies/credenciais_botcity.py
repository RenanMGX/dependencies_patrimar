import requests
import json

class CredentialNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BotCityApi:
    @staticmethod
    def token(f):
        def wraps(*args, **kwargs):
            self:BotCityApi = args[0]
            self.get_token()
            result = f(*args, **kwargs)
            return result
        return wraps
    
    
    def __init__(self, *, login:str, key:str) -> None:
        self.login:str = login
        self.key:str = key
        
        self.acessToken:str = ""
        self.organizationLabel:str = ""
        self.refreshToken:str = ""
        
    def get_token(self) -> bool:
        reqUrl:str = "https://developers.botcity.dev/api/v2/workspace/login"
        
        headersList = {
            "Content-Type": "application/json" 
        }        
        
        payload = json.dumps({
            "login": self.login,
            "key": self.key
        })
        
        response = requests.request("POST", reqUrl, data=payload, headers=headersList)
        
        if response.status_code != 200:
            raise Exception(f"erro ao gerar token: {response.status_code} - {response.reason} - {response.text}") 
        
        self.acessToken = response.json().get("accessToken")
        self.organizationLabel = response.json().get("organizationLabel")
        self.refreshToken = response.json().get("refreshToken")

        return True


class CredentialBotCity(BotCityApi):    
    def __init__(self, *, login: str, key: str) -> None:
        super().__init__(login=login, key=key)
        
    
    @BotCityApi.token
    def get_credential(self, label:str) -> dict:
        reqUrl:str = "https://developers.botcity.dev/api/v2/credential"
        
        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

        if response.status_code != 200:
            Exception(f"Erro ao obter credencial: {response.status_code} - {response.reason} - {response.text}")   
            
        credentials_list:list = response.json()
        
        for credentials in credentials_list:
            if credentials['label'] == label:
                mount_credential:dict = {}
                for secrets in credentials['secrets']:
                    mount_credential[secrets['key']] = secrets['value']
                return mount_credential
        
        raise CredentialNotFound(f"O {label=} não foi encontrado nas credenciais salvas!")
    
    @BotCityApi.token
    def alter_credential(self, *, label:str, key:str, value:str) -> bool:
        reqUrl = f"https://developers.botcity.dev/api/v2/credential/{label}"

        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }

        mount = []
        try:
            lista = self.get_credential(label)
        except CredentialNotFound:
            self._create_crendential(label=label, key=key, value=value)
            lista = self.get_credential(label)
        
                
        for old_key, old_value in lista.items():
            if old_key == key:
                continue
            mount.append({"key": old_key, "value": old_value})
        
        
        
        mount.append({"key": key, "value": value})
                        
        payload = json.dumps({
        "label": label,
        "secrets" : mount
        })

        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

        if response.status_code != 200:
            raise Exception(f"erro ao alterar credencial da {label=}: {response.status_code} - {response.reason} - {response.text}") 
        
        return True
    
    @BotCityApi.token
    def _create_crendential(self, *, label:str, key:str, value:str):
        reqUrl = f"https://developers.botcity.dev/api/v2/credential"

        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }

        payload = json.dumps({
        "label": label,
        "secrets" : [
            {
                "key": key,
                "value": value
            }
        ]
        })

        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

        if response.status_code != 200:
            raise Exception(f"erro ao criar credencial da {label=}: {response.status_code} - {response.reason} - {response.text}") 
        
        return True
    
    @BotCityApi.token
    def teste(self):
        return
        
if __name__ == "__main__":
    pass
        
        