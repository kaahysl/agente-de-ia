#Importando as bibliotecas
from flask import Flask,jsonify,request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv
from supabase import create_client
import os

#leitura da chave de api
load_dotenv()
#usagndo getenv
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
#Criando a conexão com o banco de dados, passando a URL e a KEY
supabase = create_client(supabase_url,supabase_key)

app=Flask(__name__)
#Criar 
CORS(app)

#Criar um agente
agente = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um agente virtual do Hotel Transilvania, slogan: Aqui até os monstros e humanos podem ter seu melhor descanso."
    "Você pode responder de forma clara e bem humorada, informações sobre os quartos, serviços, reservas e preços"
    "quarto standard ($500), quarto de luxe ($700), quarto suíte master ($1000)"
    "No Hotel Transivania tera café da manhã incluso, academia 24 horas, lavanderia, restaurante e piscina.",
    markdown=True
)

#Criar a rota VAZIA e o metodo GET
@app.route("/", methods=['GET'])
def testar():
    return jsonify({"mensagem":"API funcionando"})
@app.route("/criar", methods=['POST'])
def pergunta():
    dados=request.get_json()
    pergunta= dados ['pergunta']
    resposta= agente.run(pergunta)
    return jsonify({"resposta":resposta.content})
#Criar a rota para reservas
@app.route("/reserva", methods=['POST'])
def reservas():
    dados = request.get_json()
    nova_reserva ={
        "nome":dados["nome"],
        "email":dados["email"],
        "check_in":dados["check_in"],
        "tipo_quarto":dados["tipo_quarto"]
    }
    supabase.table("reservas").insert(nova_reserva).execute()
    return jsonify({"mensagem":"Sua reserva foi realizada com sucesso!"})

if __name__=='__main__':
     app.run(host="0.0.0.0", port=8000)
