import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/teams"

headers = {
    "x-apisports-key": API_KEY
}

def buscar_time():
 
 time = input("Digite o nome do time:")
 return time

time = buscar_time()

params = {
   "search":time
}

resposta = requests.get(url, headers=headers, params=params)

dados = resposta.json()

print("Resultados encontrados:", dados["results"])

if dados["results"]>0:
   for i, item in enumerate(dados["response"],start=1):
      print(
         f"{i} - {item['team']['name']} - ID: {item['team']['id']}"
      )

   escolha = int(input("Escolha o número do time:"))
   time_escolhido= dados["response"][escolha-1]
   id_time = time_escolhido["team"]["id"]
   nome_time = time_escolhido["team"]["name"]
   print("\n Time Selecionado:")
   print(nome_time)
   print("ID:", id_time)
else:
      print("Time não  encontrado.")

url_jogos =  "https://v3.football.api-sports.io/fixtures"
params_jogos = {
   "team":id_time,
   "season": 2023
}

resposta_jogos = requests.get (
   url_jogos,
   headers=headers,
   params=params_jogos
)
dados_jogos = resposta_jogos.json()


print("\nÚltimos jogos encontrados:")

vitorias= 0
empates= 0
derrotas= 0

gols_marcados = 0
gols_sofridos = 0

forma_recente = []

for jogo in dados_jogos["response"]:
 
 mandante=jogo ["teams"]["home"]["name"]
 visitante = jogo["teams"]["away"]["name"]

 gols_mandante = jogo["goals"]["home"]
 gols_visitante = jogo["goals"]["away"]


 print(f"{mandante} {gols_mandante} x {gols_visitante} {visitante}")

 if mandante == nome_time:
   gols_marcados += gols_mandante
   gols_sofridos += gols_visitante


   if gols_mandante > gols_visitante:
      vitorias += 1
      forma_recente.append("V")


   elif gols_mandante == gols_visitante:
      empates +=1
      forma_recente.append("E")
   
   else:
      derrotas +=1
      forma_recente.append("D")

   print(">>> O time está jogando em casa")


 else:
    gols_marcados += gols_visitante
    gols_sofridos +=gols_mandante
      
      
    if gols_visitante > gols_mandante:
         vitorias +=1
         forma_recente.append("V")

    elif gols_visitante == gols_mandante:
         empates += 1
         forma_recente.append("E")
      
    else:
         derrotas +=1
         forma_recente.append("D")

    print(">>>O time está jogando fora")

total_jogos= vitorias + empates + derrotas
pontos = (vitorias * 3) + empates
max_pontos= total_jogos * 3
aproveitamento = (pontos / max_pontos) * 100

media_gols_marcados = gols_marcados / total_jogos
media_gols_sofridos = gols_sofridos / total_jogos

forma_5_jogos= forma_recente[:5]



print("\nResumo")

print("Total de Jogos:", total_jogos)
print("Vitórias:", vitorias)
print("Empates:", empates)
print("Derrotas:", derrotas)

print("Pontos Conquistados:", pontos)
print(f"Aproveitamento: {aproveitamento:.2f}%")


print(f"Média de gols marcados: {media_gols_marcados:.2f}")
print(f"Média de gols sofridos: {media_gols_sofridos:.2f}")

print("Gols Marcados:", gols_marcados)
print("Gols Sofridos:", gols_sofridos)

print("Ultimos 5 jogos:", " ".join(forma_5_jogos))
