# pour installer les packages rendez vous dans votre terminal et écrivez:

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install testresources
# pip install beautifulsoup4
# pip install pandas

"""
-Créez un nouveau dossier (votre bureau par exemple et mettez y ce programme)
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
from os import path
import base64
from bs4 import BeautifulSoup
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import email
from email import policy
from email.parser import BytesParser
import glob
import os
import unittest
from unittest import mock


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
  
def getEmails():
    '''
    Fonction qui permet de récupérer une Series pandas des corpus de mails
    depuis notre adresse mail
    Output: df.series
    '''
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

    count = count_mail(service)
    result = service.users().messages().list(userId='me', maxResults=count).execute()
    
  
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

    df_mails["body"] = df_mails["body"].astype(str)
    df_mails = df_mails.groupby('subject').agg(' '.join)

    return df_mails["body"]


def count_mail(service):
    '''
    Fonction qui compte le nombre de mails disponible dans la boîte mail
    et soustrait le nombre mails disponibles dans la base de données
    Output: 
    int; nombre de mails à récupérer
    '''
    getProfile = service.users().getProfile(userId='me').execute()
    total_mails = getProfile["messagesTotal"]

    if not path.exists('mails_spam_clean.parquet'):
        return 500
    else:
        df = pd.read_parquet('mails_spam_clean.parquet')
        return int(total_mails - len(df.index)//2)
    
  
  
def clean_data(df):
    '''
    Fonction qui nettoie la base de donnée en remplaçant ou en supprimant certains
    mots en fonctions de certains caractères ou chaîne de caractère
    Output:
    pandas df: dataframe nettoyé
    '''
    row = str(df)
    brut = row.replace('\r\n\r\n',' ')
    brut = brut.replace('\r\n',' ')
    brut = brut.split(" ")
    word = 0

    while word <= len(brut)-1:

        if "<p>" in brut[word]:
            brut[word] = brut[word].replace('<p>','')
        if '\\' in brut[word]:
            brut[word] = brut[word].replace('\\',' ')
        if '>' in brut[word]:
            brut[word] = brut[word].replace('>', '')
        if '=' in brut[word]:
            brut[word] = brut[word].replace('=', '')
        if (brut[word].startswith('(h')
            or brut[word].startswith(')')
            or brut[word].startswith('\\')
            or brut[word].startswith(' ')
            or brut[word].startswith('[h')
            or brut[word].startswith('"[h')
            or brut[word].startswith('--')
            or brut[word].startswith('</')
            or brut[word].endswith('--')
            or brut[word].startswith('__')
            or brut[word].endswith('__')
            or '   ' in brut[word]
            or 'http' in brut[word]
            or 'https' in brut[word]
            or brut[word].endswith(')')
            or brut[word].endswith('>')):
            brut.remove(brut[word])

        word += 1

    df_mails = " ".join(brut)

    return df_mails


def get_ham(len_df_mails):
    '''
    Fonction qui récupère et nettoie la base de données de mails non spams
    Output:
    pandas df: df de mails non spams nettoyés
    '''
    path = 'ham/' 
    df_mails = pd.DataFrame(columns = ["body"])
    eml_files = glob.glob(path + '*.eml.txt')

    for eml_file in eml_files:

        with open(eml_file) as email_file:
            email_message = email.message_from_file(email_file).as_string()
        email_file.close()
        email_message = email_message.split("\n")
        email_message = " ".join(email_message)
        df_mail = pd.DataFrame([email_message], columns = ["body"])
        df_mails = df_mails.append(df_mail, ignore_index=True)

    return df_mails.head(len_df_mails)

def main():

    df_mails = getEmails()
    df_mails = pd.DataFrame(df_mails.apply(clean_data))
    df_mails = df_mails.astype(str)
    df_mails['Spam'] = True
    df_mails.to_parquet("mails_spam_raw.parquet")

    if path.exists('mails_spam_raw.parquet'):
        df = pd.read_parquet('mails_spam_raw.parquet')
        df_mails = pd.concat([df_mails, df], ignore_index=True)
    len_df_mails = len(df_mails)

    df_ham = get_ham(len_df_mails)
    df_ham = pd.DataFrame(df_ham["body"].apply(clean_data))
    df_ham['Spam'] = False
    df_final = pd.concat([df_ham, df_mails], ignore_index=True)

    df_final.to_parquet("mails_spam_clean.parquet")

def test_clean_data(df):

    result = clean_data(df)
    assert len(result) > 0

def test_count_mail(service):

    result = count_mail(service)
    assert result.isnumeric()

def test_get_ham(df):

    result = get_ham(df)
    assert len(result) > 0

if __name__ == "__main__":
    
    main()
    unittest.main()
