import google.generativeai as gemini
from typing import Literal
import json
import os
import traceback
class Historico:
    path = os.path.join(f'C:\\Users\\{os.getlogin()}', '.historico_gemini.json')
    
    @staticmethod
    def get_historico() -> list:
        try:
            with open(Historico.path, "r", encoding='utf-8') as _file:
                historico = json.loads(_file.read())
            return historico
        except:
            return []
    
    @staticmethod
    def set_historico(historico:list):
        with open(Historico.path, "w", encoding='utf-8') as _file:
            json.dump(historico, _file, indent=4)
    
    @staticmethod  
    def clear_historico():
        with open(Historico.path, "w", encoding='utf-8') as _file:
            json.dump([], _file, indent=4)

class GeminiIA:
    @property
    def safety_settings(self):
        return [
                {
                                "category": "HARM_CATEGORY_HARASSMENT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_HATE_SPEECH",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                "threshold": "BLOCK_NONE"
                            },            
                    ]
    
    @property
    def model(self):
        return self.__model
        
    def __init__(self, *,
                token:str,
                instructions:str = "voce é um assistente virual prestavito e educado!",
                model:Literal["gemini-2.0-flash", "gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-preview-05-06", "gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro"] = "gemini-2.0-flash-lite",
                    temperature: float = 0.5,
                    max_output_tokens: int = 300,
                    top_p: float = 0.9,
                    top_k: int = 40,
                 ):
        
        self.__model = gemini.GenerativeModel(#type: ignore
            model_name = model,
            generation_config={
                "temperature": temperature, #type: ignore
                "max_output_tokens": max_output_tokens,
                "top_p": top_p,
                "top_k": top_k,
            },
            system_instruction = f"{instructions}\n Adicional: seu nome e Orion e quem esta te programando é o Renan Oliveira usando api da google generative ai",
            safety_settings=self.safety_settings        
        )
        
        gemini.configure(api_key=token)#type: ignore
        
    def clear_historico(self, *, path:str):
        Historico.clear_historico()
    
    def perguntar(self, pergunta:str, *, save_history:bool=False):
        if save_history:
            history = Historico.get_historico()
            
            formated_history = []
            for interacao in history:
                for mensagem in interacao:
                    formated_history.append({
                        "role": mensagem["role"],  # Certifique-se de que a chave é 'author'
                        "parts": mensagem["parts"]    # 'parts' deve ser uma lista de strings
            }) 
                    
            history = formated_history
        else:
            history = []
        
        
        response = self.model.start_chat(history=history).send_message(pergunta)
        
        if save_history:
            historico_temp = []
            historico_temp.append({"role": "user", "parts": [pergunta]})
            historico_temp.append({"role": "model", "parts": [response.text]})

            history.append(historico_temp)
            Historico.set_historico(historico=history)
            
        return response
    
class ErrorIA(GeminiIA):
    @staticmethod
    def error_message(*, token:str, message:str) -> str:
            if token:
                try:
                    ia = GeminiIA(token=token,
                                instructions="""
    Você receberá um traceback de erro em Python.
    Sua tarefa é dividida em duas partes:

    1. Análise:
    Identifique e descreva de forma objetiva e direta qual é o erro apresentado no traceback. Foque na causa principal do problema.

    2. Resolução:
    Sugira uma correção breve e prática para resolver o erro identificado. A sugestão deve ser clara, aplicável e sem explicações adicionais.

    Não se apresente, não explique o que está fazendo e não adicione comentários extras. Apenas forneça a análise e a resolução, de forma direta e concisa.
                                """,
                                temperature=0.2,
                                top_p=0.8,
                                top_k=40,
                                )
                    resposta = ia.perguntar(pergunta=message).text
                    return resposta
                except Exception as e:
                    return ""
            
            return ""
        
        
        
if __name__ == "__main__":
    with open(r"token.txt", "r") as _file:
        api_token = _file.read().strip()
    
    try:
        raise Exception("Erro de teste para Gemini IA")
    except Exception as error:
        resposta = ErrorIA.error_message(token=api_token, message=traceback.format_exc())
        if resposta:
            print("Resposta da IA:", resposta)
        else:
            print("Não foi possível obter uma resposta da IA.")