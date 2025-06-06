import json
import os
from copy import deepcopy
from random import randint
from getpass import getuser
from typing import Literal, Dict

class CredentialFileNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Credential:
    #path_raiz:str=f"C:\\Users\\{getuser()}\\PATRIMAR ENGENHARIA S A\\RPA - Documentos\\RPA - Dados\\CRD\\.patrimar_rpa\\credenciais\\"
    
    @property
    def path(self):
        return self.__path
    
    def __init__(self, *, path_raiz:str, name_file:str) -> None:
        if not os.path.exists(path_raiz):
            raise FileNotFoundError(f"{path_raiz=} não existe!")
        
        self.path_raiz:str = path_raiz    
        
        
        name:str = str(name_file)
        if not isinstance(self.path_raiz, str):
            raise TypeError("apenas strings")
        if not isinstance(name, str):
            raise TypeError("apenas strings")
        if not name.endswith('.json'):
            name += '.json'
                
        self.__path = os.path.join(self.path_raiz, name)
        
        if not os.path.exists(self.path):
            raise CredentialFileNotFoundError(f"'{self.path=}' não foi encontrado!")
    
    @staticmethod
    def create(*, path_raiz:str,name_file:str):
        if not name_file.endswith('.json'):
            name_file += ".json"
        
        if not os.path.exists(path_raiz):
            try:
                os.makedirs(path_raiz)
            except:
                raise Exception(f"{path_raiz=} não foi possivel ser criado!")
        
        combined_file:str = os.path.join(path_raiz, name_file)
        
        if not os.path.exists(combined_file):
            with open(combined_file, 'w')as _file:
                json.dump({"key": 0},_file)
            print(f"{name_file=} foi criado!")
        else:
            print(f"{name_file=} ja existe!")
        
        
        
    def load(self, *, keys:bool=False) -> dict:
        """crie / ler um arquivo json contendo as credenciais

        Args:
            path (str): caminho do arquivo que será salvo as crendicias

        Raises:
            FileNotFoundError: caso o arquivo não exista irá criar um e vai alertar que foi criado e pedira para iniciar o script novamente

        Returns:
            dict: dicionario com a credenciais salvas
        """
        
            #raise FileNotFoundError(f"{self.path=} não existe! então foi criar uma no repositorio, edite as credenciais e execute o codigo novamente!")

        with open(self.path, 'r')as _file:
            result:dict = json.load(_file)
                
        new_result = deepcopy(result)
        for key,value in new_result.items():
            if key == 'key':
                continue
            
            _value = self.decifrar(value, new_result['key'])
            
            new_result[key] = _value if not keys else len(_value) * "*"
        
        del new_result['key']
             
        return new_result
                            
    def alter(self, **kargs) -> None:
        dados:dict = self.load()
        for key, value in kargs.items():
            for k, v in dados.items():
                if key == k:
                    dados[k] = value
        
        self.save(**dados)
    
    def save(self, **kargs) -> None:
        token = randint(500,6000)
        
        words:Dict[str,object] = {key:self.criar_cifra(value, token) for key,value in kargs.items()}
        words['key'] = token
        
        with open(self.path, 'w')as _file:
            json.dump(
                words,
                _file)
    
    def criar_cifra(self, text:str, key:int=1, response_json:bool=False) -> str:
        """criptografa a string informada orientada pela Key

        Args:
            text (str): texto a ser criptografado
            key (int, optional): chave para criptografia. Defaults to 1.
            response_json (bool, optional): retorna a string em formato json. Defaults to False.

        Returns:
            str: valor criptografado
        """
        if not isinstance(key, int):
            key = int(key)
        result:str = ""
        for letra in text:
            codigo:int = ord(letra) + key
            result += chr(codigo)
        
        if response_json:    
            return json.dumps(result)
        return result
    
    def decifrar(self, text:str, key:int) -> str:
        """descriptografa a string

        Args:
            text (str): texto a ser descriptografado
            key (int): chave para descriptografar

        Returns:
            str: texto descriptografado
        """
        return self.criar_cifra(text, -key)
        
if __name__ == "__main__":
    #crd = Credential('IMOBME_QAS')
    #crd = Credential('Teste')
    #crd = Credential('SAP_QAS-Renan')
    #crd = Credential('SAP_QAS')
    crd = Credential(path_raiz=f"C:\\Users\\{getuser()}\\PATRIMAR ENGENHARIA S A\\RPA - Documentos\\RPA - Dados\\CRD\\.patrimar_rpa\\credenciais\\", name_file='GeminiIA-Token-Default')

    
    print(crd.load(keys=True))
