<h1 align="center"> ALMG Bot </h1>

Agenda diária da [Assembleia Legislativa de Minas Gerais](https://www.almg.gov.br/comunicacao/agenda/) por meio de um bot do Telegram
-------------------------------------------------------------------------------------------------------------------------------------
# :hammer: Funcionalidades do projeto

- `Funcionalidade 1`: obter a agenda da ALMG todos os dias a partir de um robô do Telegram
- `Funcionalidade 2`: cadastrar a agenda da ALMG todos os dias numa planilha do Google Spreadsheets

Esse repositório é um site que possui:

-   Robô do [Telegram](https://telegram.org/)
-   Integração com o Google Sheets
-   Site em Flask

[](https://github.com/turicas/site-teste/blob/main/README.md#configura%C3%A7%C3%A3o-inicial)Configuração inicial
----------------------------------------------------------------------------------------------------------------

Não se esqueça de:

-   Criar uma *service account* no Google Cloud
-   Criar o *token* do seu robô no Telegram
-   Configurar o `setWebhook` do Telegram

### [](https://github.com/turicas/site-teste/blob/main/README.md#configurando-o-webhook-do-telegram)Configurando o webhook do Telegram

Execute o seguinte código:

```
import requests

token = "SEU TOKEN"
url = "https://meu-site.onrender.com/telegram-bot"
response = requests.post(f"https://api.telegram.org/bot{token}/setWebhook", data={"url": url})
print(response.text)

```

[](https://github.com/turicas/site-teste/blob/main/README.md#pr%C3%B3ximos-passos)Próximos passos
-------------------------------------------------------------------------------------------------

-   [ ]  Implementar Web scraping
    -   [ ]  Criar código para raspar o site da ALMG
    -   [ ]  Alimentar dataFrame do Pandas com resultado da raspagem
    -   [ ]  No Dataframe, não se esquecer de criar uma coluna ["data"] para informar quando aquela raspagem foi feita
    -   [ ] Ainda no DataFrame, transformar a coluna ["Horário"] para `str` para possibilitar a integração à planilha
    -   [ ]  Configurar Pipedream para chamar código 1x por dia
-   [ ]  Implementar robô do Telegram
    -   [ ]  Coletar dados que foram raspados no dataFrame
    -   [ ]  Usar emojis para formatar o texto final
    -   [ ]  Responder o usuário de acordo com a mensagem enviada
-   [ ]  Implementar planilha do Google Spreadsheets
    -   [ ]  Coletar dados que foram raspados no DataFrame e transformá-los em lista com o atributo `values.tolist()`
    -   [ ]  Adicionar as linhas na página da planilha especificada na chave
