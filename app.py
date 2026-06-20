#Importando as bibliotecas
from flask import Flask,jsonify,request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv

#leitura da chave de api
load_dotenv()
app=Flask(__name__)
#Criar 
CORS(app)

#Criar um agente
agente = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um agente virtual do Hotel Transilvania, slogan: aqui todos os monstros e humanos podem descansar"
    "Você pode responder de forma clara e bem humorada, informações sobre os quartos, serviços, reservas e preços"
    "quarto standard ($500), quarto de luxe ($700), quarto suíte master ($1000)",
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

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8000)
