import os
from getpass import getuser
import json

class SharePointFolders(str):
    @property
    def base_path(self):
        return self.__base_path
    
    @property
    def paths_register_json_path(self):
        return self.__paths_register_json_path
    
    @property
    def found_path(self):
        return self.__found_path
    
    @property
    def value(self):
        return self.__value
    
    def __init__(self, 
                 target_path:str,
                 *,
                 base_path:str=f"C:\\Users\\{os.getlogin()}",
                 paths_register_json_path:str = os.path.join(os.getcwd(), "json", 'paths_register.json')
        ) -> None:
        
        if not os.path.exists(base_path):
            raise FileNotFoundError(f"Caminho '{base_path=}' não encontrado!")
        self.__base_path:str = base_path
        
        if not paths_register_json_path.lower().endswith('.json'):
            paths_register_json_path += '.json'
        if not os.path.exists(os.path.dirname(paths_register_json_path)):
            os.makedirs(os.path.dirname(paths_register_json_path))
        self.__paths_register_json_path:str = paths_register_json_path
        
        self.__target_path:str = target_path
        self.__key_target_path:str = os.path.normpath(target_path).replace("\\", "|")
        
        self.__found_path:str

        found_path:str|None = self.__read_registerPaths().get(self.__key_target_path)
        if found_path:
            if os.path.exists(found_path):
                self.__found_path = found_path
            else:
                self.__found_path = self.__search()
                self.__save_registerPath()
        else:
            self.__found_path = self.__search()
            self.__save_registerPath()

        self.__value:str = self.found_path
        
    def __search(self):
        for root, paths, files in os.walk(self.base_path):
            if root.endswith(self.__target_path):
                return root
        raise FileNotFoundError(f"targer '{self.__target_path}' not found")
    
    def __read_registerPaths(self) -> dict:
        try:
            with open(self.paths_register_json_path, 'r', encoding='utf-8') as _file:
                data =  json.load(_file)
            return data
        except:
            return {}
    
    
    def __save_registerPath(self):
        found_path = self.found_path
        if not os.path.exists(found_path):
            found_path = self.__search()
            
        data:dict = self.__read_registerPaths()
        data[self.__key_target_path] = found_path
        with open(self.paths_register_json_path, 'w', encoding="utf-8") as _file:
            json.dump(data, _file, indent=4, ensure_ascii=True)
            
    def __str__(self) -> str:
        return self.found_path
    
    def __repr__(self) -> str:
        return self.found_path
    
if __name__ == "__main__":
    spf = SharePointFolders(r"Status Liquidação")
    
    print(type(spf))
    