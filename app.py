import os
import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pandas as pd
import json
from bs4 import BeautifulSoup

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1mOd6Muax8S58sSTbH68e-i8rQm8JEyYbDZnZowDrEzY")
sheet = planilha.worksheet("Página1")
app = Flask(__name__)
df_agenda = None
@app.route("/dataframe_ALMG")
def dataframe_ALMG():
  global df_agenda
  site_almg = requests.get('https://www.almg.gov.br/')
  bs = BeautifulSoup(site_almg.content)
  agenda_items = bs.findAll('div', {'class': 'almg-css_eventoDescTit'})
  agenda_dia = []
  for i, agenda in enumerate(agenda_items):
    comissão = agenda.get_text(strip=True)
    link = "https://www.almg.gov.br/"+agenda.find('a').get('href')
    horario = bs.findAll('span', {"class": "almg-css_dataHourSingle text-dark"})[i].text
    local = bs.findAll('p', {"class": "m-0 mt-2 text-gray-550"})[i].text
    agenda_dia.append([comissão, link, horario, local])
  df_agenda = pd.DataFrame(agenda_dia, columns=['Comissão', 'Link da Agenda', 'Horário', 'Local'])
  return "Ok!"
  
@app.route("/planilha_ALMG")
def planilha_ALMG():
  global df_agenda
  df_agenda['Horário'] = df_agenda['Horário'].astype(str)
  lista_df = df_agenda.values.tolist()
  planilha.append_rows(lista_df)
  return "Planilha escrita!"
