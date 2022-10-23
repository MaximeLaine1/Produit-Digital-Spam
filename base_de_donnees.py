
# pour installer les packages rendez vous dans votre terminal et écrivez:

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install testresources
# pip install beautifulsoup4
# pip install pandas

"""
-Créez un nouveau dossier (votre bureau par exemple et foutez y ce programme)
-Récupérez le fichier credentials.json et mettez le dans le dossier où vous avez ce programme
-La première fois que vous allez lancer le programme il va automatiquement vous envoyer vers une page web
-Connectez vous avec l'adresse spam.sep.2022.2023@gmail.com (mdp: hafhoumaxsim) et faites ce qui est écrit
 (acceptez même ce n'est pas sécurisé)
-Cela va créer un nouveau fichier token.pickle dans le dossier où vous avez enregistré ce programme Python
-Si par malheur vous vous êtes connectés à votre adresse mail perso (et pas spam.sep.2022.2023@gmail.com) il
 faut supprimer token.pickle et recommencer
-A la fin un nouveau fichier mails_spam au format parquet va se créer dans le dossier où vous avez ce programme
 (parquet c'est bien; illisible pour l'humain mais facile à traiter pour l'ordi contrairement au csv ou xlsx)
-Lancer le programme alors que vous avez déjà un fichier mails_spam devrait supprimer l'ancien, renommez
 l'ancien mails_spam avant de lancer le programme si vous voulez garder l'ancien

-En cas de problème persistant veuillez contacter Simon, votre demande sera traitée dans les plus brefs délais
"""

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
  
def getEmails():
    creds = None

    if os.path.exists('token.pickle'):
  
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
  
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
  
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  
    service = build('gmail', 'v1', credentials=creds)
  
    result = service.users().messages().list(userId='me').execute()
  
    messages = result.get('messages')

    df_mails = pd.DataFrame(columns = ["subject", "from", "body"])

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
  
        try:
            payload = txt['payload']
            headers = payload['headers']
  
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
  
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
  
            soup = BeautifulSoup(decoded_data , "lxml")
            body = soup.body()
  
            print("Subject: ", subject)
            print("From: ", sender)
            print("Message: ", body)
            print('\n')
            print("---------------------------------------------------------------------------")

            data = {
                "subject": subject,
                "from": sender,
                "body": body 
                }

            df_mail = pd.DataFrame(data, columns = ["subject", "from", "body"])

            df_mails = df_mails.append(df_mail, ignore_index=True)
            print(len(df_mails))


        except:
            pass
    
    return df_mails
  
  
def clean_data(df):
    row = str(df)
    brut = row.replace('\r\n\r\n',' ')
    brut = brut.replace('\r\n',' ')
    brut = brut.split(" ")
    word = 0
    while word <= len(brut)-1:
        print(str(word) + "   " + str(len(brut)))
        if "<p>" in brut[word]:
            brut[word] = brut[word].replace('<p>','')
        elif (brut[word].startswith('(h')
            or brut[word].startswith(')')
            or brut[word].startswith('\\')
            or brut[word].startswith(' ')
            or brut[word].startswith('[h')
            or 'http' in brut[word]
            or 'https' in brut[word]
            or brut[word].endswith(')')
            or brut[word].endswith('>')):
            brut.remove(brut[word])
        word += 1
        
    df_mails = " ".join(brut)
    return df_mails



df_mails = getEmails()
df_mails = pd.DataFrame(df_mails["body"].apply(clean_data))
df_mails = df_mails.astype(str)
df_mails.to_parquet("mails_spam_raw.parquet")
