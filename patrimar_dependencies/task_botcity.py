try:
    from .credenciais_botcity import BotCityApi
except:
    from credenciais_botcity import BotCityApi
import base64
import requests
from requests.models import Response
import json
from typing import List, Dict
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
    
    @BotCityApi.token
    def get_task_alerts(self, task_id:int):
        reqUrl = f"https://developers.botcity.dev/api/v2/alerts?taskId={task_id}"

        headersList = {
        "organization": self.organizationLabel,
        "accept" : "*/*",
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
        response = requests.request("GET", reqUrl, headers=headersList)

        return response
    
    def get_task_alerts_messages(self, task_id:int) -> list:
        alerts_response = self.get_task_alerts(task_id=task_id)
        if alerts_response.status_code != 200:
            print("alertas não encontrados!")
            return [] 
        
        try:
            alerts_content:List[dict] = alerts_response.json().get("content")
            messages = []
            for alert in alerts_content:
                try:
                    date = datetime.fromisoformat(str(alert.get("date")))
                    date = date - relativedelta(hours=3)
                    date = date.strftime("[%d/%m/%Y - %H:%M:%S]")
                except:
                    date = "[ data desconhecida ]"
                
                _type = ""
                if alert.get("type") == "INFO":
                    _type = "<django:green>"
                elif alert.get("type") == "ERROR":
                    _type = "<django:red>"
                elif _type == "WARN":
                    _type = "<django:yellow>"
                    
                messages.append(f"{date} - {alert.get('message')} {_type}")
            
            return messages
        except:
            print("alertas não encontrados!")
            return []
    
    @BotCityApi.token
    def get_task_logs(self, logLabel:str, *, days:int=1, json_response:bool=False, raise_exception:bool=False):
        reqUrl = f"https://developers.botcity.dev/api/v2/log/{logLabel}/export?days={days}"

        headersList = {
        "organization": self.organizationLabel,
        "accept" : "*/*",
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
        
        response = requests.request("GET", reqUrl, headers=headersList)
        if response.status_code == 200:
            if json_response:
                return response.json()
            return response

        if raise_exception:
            raise Exception(f"erro ao obter logs do {logLabel=}: {response.status_code} - {response.reason} - {response.text}")
        return response
  
    @BotCityApi.token
    def delete_task_logs(self, logLabel:str, *, raise_exception:bool=False):
        reqUrl = f"https://developers.botcity.dev/api/v2/log/{logLabel}"

        headersList = {
        "organization": self.organizationLabel,
        "accept" : "*/*",
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
        
        response = requests.request("DELETE", reqUrl, headers=headersList)
        if response.status_code == 200:
            return response

        if raise_exception:
            raise Exception(f"erro ao deletar logs do {logLabel=}: {response.status_code} - {response.reason} - {response.text}")
        return response
    
    @BotCityApi.token
    def create_task_logs(self, *, logLabel:str, columns:List[dict]=[{"name": "Column 1", "label": "col1"},], force:bool=False, raise_exception:bool=False):
        """
        Creates task logs by sending a POST request to the BotCity API.
        This method validates the columns parameter, constructs an API request with
        the provided organization label, activity label, and columns, then sends it
        to the BotCity log endpoint.
        Args:
            logLabel (str): The label/name of the activity or log to be created.
            columns (List[dict], optional): A list of dictionaries representing table columns.
                Each dictionary should contain column metadata such as 'name', 'label'.
                Defaults to [{"name": "Column 1", "label": "col1"}].
            json_response (bool, optional): If True, returns the response as JSON format.
                If False, returns the raw response object. Defaults to False.
        Returns:
            Retorna a resposta da API como dicionário JSON se
                json_response for True, caso contrário retorna o objeto requests.Response.
        
        Raises:
            Exception: Se columns não for uma lista ou contiver elementos que não são
                dicionários, com mensagem descrevendo o formato esperado.
            Exception: Se a requisição da API falhar (status code != 200), com detalhes
                do erro incluindo código de status, razão e texto da resposta.
        
        Exemplos de construção das colunas:
            columns = [
                {"name": "ID", "label": "id"},
                {"name": "Nome", "label": "nome"},
                {"name": "Status", "label": "status"}
            ]
            
            Onde:
            - name: Nome exibido da coluna
            - label: Identificador único da coluna (sem espaços)
            dict or requests.Response: Returns the API response as a JSON dictionary if
                json_response is True, otherwise returns the requests.Response object.
        Raises:
            Exception: If columns is not a list or contains non-dictionary elements,
                with a message describing the expected format.
            Exception: If the API request fails (status code != 200), with details about
                the error including status code, reason, and response text.
        """
        if not isinstance(columns, list):
            raise Exception("O parâmetro columns deve ser uma lista de dicionários no formato [{'key': 'nome_da_coluna', 'value': 'valor_da_coluna'}, ...]")
        for column in columns:
            if not isinstance(column, dict):
                raise Exception("O parâmetro columns deve ser uma lista de dicionários no formato [{'key': 'nome_da_coluna', 'value': 'valor_da_coluna'}, ...]")
            if 'name' not in column or 'label' not in column:
                raise Exception("Cada dicionário em columns deve conter as chaves 'name' e 'label'. Exemplo: {'name': 'Nome da Coluna', 'label': 'nome_coluna'}")
            
        reqUrl = f"https://developers.botcity.dev/api/v2/log"

        headersList = {
        "organization": self.organizationLabel,
        "accept" : "*/*",
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
                
        payload = json.dumps({
            "organizationLabel": self.organizationLabel,
            "activityLabel" : logLabel,
            "columns": columns
        })
        
        for _ in range(2):
            response = requests.request("POST", reqUrl, headers=headersList, data=payload)
            if response.status_code == 200:
                return response
            
            if force:
                if response.status_code == 400:
                    if response.json()['details'] == "Label already exists":
                        self.delete_task_logs(logLabel=logLabel, raise_exception=False)
                        continue

            if raise_exception:
                raise Exception(f"erro ao criar log do {logLabel=}: {response.status_code} - {response.reason} - {response.text}")
            return response

    @BotCityApi.token
    def input_task_logs(self, *, logLabel:str, entry:dict={"col1": "Record 'XYZ' has been processed"}, raise_exception:bool=False):
        if not isinstance(entry, dict):
            raise Exception("O parâmetro entry deve ser um dicionário representando os dados a serem inseridos no log. Exemplo: {'col1': 'Valor da Coluna 1', 'col2': 'Valor da Coluna 2'}")
            
        reqUrl = f"https://developers.botcity.dev/api/v2/log/{logLabel}/entry"

        headersList = {
        "organization": self.organizationLabel,
        "accept" : "*/*",
        "Authorization": f"Bearer {self.acessToken}" ,
        "Content-Type": "application/json" 
        }
                
        payload = json.dumps(entry)
        
        for _ in range(2):
            response = requests.request("POST", reqUrl, headers=headersList, data=payload)
            if response.status_code == 200:
                return response
            

            if raise_exception:
                raise Exception(f"erro ao inserir entrada no log do {logLabel=}: {response.status_code} - {response.reason} - {response.text}")
            return response
    
if __name__ == "__main__":
    pass    
