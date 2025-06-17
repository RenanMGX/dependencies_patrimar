import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
from typing import Literal
import os
import re
from .functions import P

class SendEmail:
    def __init__(self, *,
                 email:str,
                 password:str,
                 smtp_server:Literal['smtp-mail.outlook.com']|str,
                 smtp_port:Literal[587]|int, 
                                 
                ) -> None:
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        
        self.__username = email
        self.__password = password
        
        
    def mensagem(
                self, *,
                Destino:str|list,
                CC:str|list="",
                Assunto:str= "",
                Corpo_email:str,
                _type:Literal['plain', 'html']='plain'
            ):
        
        msg = MIMEMultipart()
        msg['From'] = self.__username
        msg['To'] = Destino if isinstance(Destino, str) else ','.join(Destino)
        if CC:
            msg['CC'] = CC if isinstance(CC, str) else ','.join(CC)
        msg['Subject'] = Assunto
        
        msg.attach(MIMEText(Corpo_email, _type, 'utf-8'))

        self.__msg = msg
        return self
        
    def Anexo(self, Attachment_path:str):
        try:
            self.__msg
            if not os.path.exists(Attachment_path):
                raise FileNotFoundError(f"Arquivo não encontrado '{Attachment_path}'")
            
            filename = os.path.basename(Attachment_path)
            with open(Attachment_path, 'rb') as _file:
                part = MIMEApplication(_file.read(), Name=filename)
                # part = MIMEBase('application', 'octet-stream')
                # part.set_payload(_file.read())
                # encoders.encode_base64(part)
                # part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            
            part['Content-Disposition'] = f'attachment; filename="{filename}"'        
            self.__msg.attach(part)
            
            return self
        except KeyError:
            raise Exception(f"Crie um corpo de email primeiro usando '.mensagem'")
    
    def addImagemCid(self, *, Attachment_path:str, tag:str):
        try:
            self.__msg
            if not os.path.exists(Attachment_path):
                raise FileNotFoundError(f"Arquivo não encontrado '{Attachment_path}'")
                
            filename = os.path.basename(Attachment_path)
            with open(Attachment_path, 'rb') as _file:
                img_data = _file.read()
            
            imagem = MIMEImage(img_data)
            imagem.add_header('Content-ID', f'<{tag}>')
            
            self.__msg.attach(imagem)
            return self
        except KeyError:
            raise Exception(f"Crie um corpo de email primeiro usando '.mensagem'")
          
    
    def send(self):
        try:
            self.__msg
        except KeyError:
            print(P("Crie um corpo para o email primeiro usando '.mensagem'", color='red'))
        
        destinatarios = []
        for campo in ['To', 'CC']:
            emails = self.__msg.get(campo, '')
            if emails:
                # Separa os endereços por vírgula ou ponto e vírgula e remove espaços em branco
                enderecos = re.split(r'[;,]', emails)
                destinatarios += [email.strip() for email in enderecos if email.strip()]

        with smtplib.SMTP(self.__smtp_server, self.__smtp_port) as server:
            server.starttls()
            server.login(self.__username, self.__password)
            server.sendmail(self.__msg['From'], destinatarios, self.__msg.as_string())
            

        print(P("Emai enviado", color='green'))
            
        del self.__msg


if __name__ == "__main__":
    email = SendEmail(
        email="email",
        password="Senha",
        smtp_server='smtp-mail.outlook.com',
        smtp_port=587 
    )
    
    email.mensagem(
        Destino="Email destino",
        Corpo_email="Corpo Email",
    )
    
    email.send()
