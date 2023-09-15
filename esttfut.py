# Importar bibliotecas necessárias
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Definir a URL da API que fornece os dados das partidas de futebol
api_url = "https://api.football-data.org/v2/matches"

# Definir o cabeçalho da requisição com a chave de acesso da API
headers = {"X-Auth-Token": "sua_chave_de_acesso"}

# Definir os parâmetros da requisição com os filtros desejados
# Neste exemplo, vamos filtrar por competições da Europa e partidas concluídas
params = {"competitions": "2001,2002,2003,2014,2015,2016,2017,2019,2021",
          "status": "FINISHED"}

# Fazer a requisição à API e obter a resposta em formato JSON
response = requests.get(api_url, headers=headers, params=params).json()

# Extrair a lista de partidas da resposta
matches = response["matches"]

# Criar um dataframe vazio para armazenar os dados das partidas
df = pd.DataFrame()

# Iterar sobre cada partida e extrair os dados de interesse
for match in matches:
    # Obter o nome da competição
    competition = match["competition"]["name"]
    # Obter o nome dos times e o placar final
    home_team = match["homeTeam"]["name"]
    away_team = match["awayTeam"]["name"]
    home_score = match["score"]["fullTime"]["homeTeam"]
    away_score = match["score"]["fullTime"]["awayTeam"]
    # Obter o número de escanteios e cartões de cada time
    home_corners = match["statistics"]["homeTeam"]["corners"]
    away_corners = match["statistics"]["awayTeam"]["corners"]
    home_cards = match["statistics"]["homeTeam"]["cards"]
    away_cards = match["statistics"]["awayTeam"]["cards"]
    # Adicionar uma linha ao dataframe com os dados da partida
    df = df.append({"competition": competition,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_score": home_score,
                    "away_score": away_score,
                    "home_corners": home_corners,
                    "away_corners": away_corners,
                    "home_cards": home_cards,
                    "away_cards": away_cards}, ignore_index=True)

# Mostrar o dataframe
print(df)

# Criar um gráfico de barras para comparar os escanteios e cartões de cada time
# Agrupar o dataframe por time e calcular a média dos escanteios e cartões
grouped_df = df.groupby(["home_team", "away_team"]).mean()
# Criar uma figura e um eixo para o gráfico
fig, ax = plt.subplots()
# Definir o tamanho da figura
fig.set_size_inches(12, 8)
# Definir o título do gráfico
ax.set_title("Comparação dos escanteios e cartões de cada time")
# Definir os rótulos dos eixos x e y
ax.set_xlabel("Times")
ax.set_ylabel("Média")
# Plotar as barras para os escanteios e cartões de cada time
grouped_df.plot.bar(ax=ax, rot=45)
# Mostrar o gráfico
plt.show()
