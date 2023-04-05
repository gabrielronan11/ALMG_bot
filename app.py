import os
import pandas as pd
import json
import gspread
import requests
import emoji
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
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
@app.route("/df)
def dataframe_ALMG():
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
  df_agenda['Data']= datetime.today().strftime('%d-%m-%Y')
  df_agenda['Horário'] = df_agenda['Horário'].astype(str)
  return df_agenda

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  if message == "/start":
    texto_resposta=  emoji.emojize(":robot:") + emoji.emojize(":clapping_hands:") + emoji.emojize(":robot:") + "\n\n" + "Olá! Seja bem-vindo(a)! Esse é um bot no qual você pode ver a agenda da Assembleia Legislativa em Minas Gerais no dia de hoje. \n\n Digite: '<b>Qual a agenda da ALMG hoje?</b>' e confira!"
  elif message == "Qual a agenda da ALMG hoje?":
    texto_resposta = emoji.emojize(":police_car_light:") + "<b>ESSA É A AGENDA DA ALMG HOJE</b>" + emoji.emojize(":police_car_light:") + "\n\n" 
    for i, row in dataframe_ALMG().iterrows():
        texto_resposta += emoji.emojize(":pushpin:") + f"{row['Comissão']}\n" + emoji.emojize(":alarm_clock:") + f"{row['Horário']}\n" + emoji.emojize(":house:") + f"{row['Local']}\n" + emoji.emojize(":link:") + f"Mais informações em: {row['Link da Agenda']}\n\n"
  else:
    texto_resposta = "Não entendi!" + emoji.emojize(":sad_but_relieved_face:") + "\n" + "Se você quer saber a agenda da Assembleia Legislativa de Minas Gerais hoje, pergunte: \n <b>'Qual a agenda da ALMG hoje?'</b>"
  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta, "parse_mode": "html"}
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  print(resposta.text)
  return "Ok!"

@app.route("/planilha-ALMG")
def planilha_ALMG():
  lista_df = dataframe_ALMG().values.tolist()
  sheet.append_rows(lista_df)
  return "Planilha escrita!"
