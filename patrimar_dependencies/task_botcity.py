try:
    from .credenciais_botcity import BotCityApi
except:
    from credenciais_botcity import BotCityApi
import base64
import requests
from requests.models import Response
import json

class TaskBotCity(BotCityApi):
    def __init__(self, *, login: str, key: str) -> None:
        super().__init__(login=login, key=key)
        
    @BotCityApi.token
    def start_task(self, *, label:str, params:dict={}):
        reqUrl = f"https://developers.botcity.dev/api/v2/task"

        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
    
        payload = json.dumps({
            "activityLabel": label,
            "parameters" : params
        })
        
        
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

        #if response.status_code != 200:
            #raise Exception(f"erro ao iniciar Tarefa da {label=}: {response.status_code} - {response.reason} - {response.text}") 
        
        return response
    
    @BotCityApi.token
    def get_task_status(self, *, task_id:int):
        reqUrl = f"https://developers.botcity.dev/api/v2/task/{task_id}"

        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
            
        
        response = requests.request("GET", reqUrl, headers=headersList)

        return response
    
    
    @BotCityApi.token
    def get_artifact(self, *, task_id:int):
        reqUrl = f"https://developers.botcity.dev/api/v2/artifact?taskId={task_id}"

        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
            
        
        response = requests.request("GET", reqUrl, headers=headersList)

        return response
    
    @BotCityApi.token
    def get_file_artifact(self, *, task_id:int):
        
        artifact_response = self.get_artifact(task_id=task_id) 
        if artifact_response.status_code != 200:
            print("artefato não encontrado!")
            return artifact_response 
        
        try:
            artifact_content = artifact_response.json().get("content")[0]
            artifact_id:int = artifact_content.get("id")
        except:
            print("artefato não encontrado!")
            artifact_response.status_code = 400
            artifact_response.reason = "Not Found"
            artifact_response._content = b"{}"
            return artifact_response 
        
        reqUrl = f"https://developers.botcity.dev/api/v2/artifact/{artifact_id}/file"

        headersList = {
        "organization": self.organizationLabel,
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
            
        
        response = requests.request("GET", reqUrl, headers=headersList)
        if response.status_code == 200:
            dicio = {
                "file_name": artifact_content.get("fileName"),
                "file": TaskBotCity.encode_file(response.content)
            }
            response._content = json.dumps(dicio).encode('utf-8')
            
            return response

        return response
    
    @BotCityApi.token
    def get_file_artifacts(self, *, task_id:int):
        
        artifact_response = self.get_artifact(task_id=task_id) 
        if artifact_response.status_code != 200:
            print("artefato não encontrado!")
            return artifact_response 
        
        artifact_list = []
        
        for artifact_content in artifact_response.json().get("content"):
            artifact_id:int = artifact_content.get("id")
        
            reqUrl = f"https://developers.botcity.dev/api/v2/artifact/{artifact_id}/file"

            headersList = {
            "organization": self.organizationLabel,
            "Authorization": f"Bearer {self.acessToken}" ,
            "Content-Type": "application/json" 
            }
            
        
            response = requests.request("GET", reqUrl, headers=headersList)
            if response.status_code == 200:
                dicio = {
                    "file_name": artifact_content.get("fileName"),
                    "file": TaskBotCity.encode_file(response.content)
                }
                artifact_list.append(dicio)
        
        
        _response:Response = Response()
        if artifact_list:  
            _response._content = json.dumps(artifact_list).encode('utf-8')
            _response.status_code = 200
            _response.reason = "OK"
        else:
            _response.status_code = 400
            _response.reason = "Not Found"
            _response._content = b"[]"


        return _response
    
    
    @staticmethod
    def encode_file(binary_file:bytes):
        return base64.b64encode(binary_file).decode('utf-8')
    
    @staticmethod
    def decode_file(str_file:str):
        return base64.b64decode(str_file)
    
if __name__ == "__main__":
    pass    
