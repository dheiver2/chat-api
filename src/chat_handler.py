from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from gradio_client import Client

# Modelo de requisição com Pydantic
class ChatRequest(BaseModel):
    message: str
    system_message: str = "Você é um assistente útil."
    language: str = "pt"

# Variáveis de tradução (simplificado para o exemplo)
TRANSLATIONS = {
    "pt": {
        "error_message": "Desculpe, ocorreu um erro: {}. Por favor, verifique sua conexão e configurações."
    }
}

# Armazena o histórico das conversas
chat_history = []

# Função para responder
def respond(request: ChatRequest):
    message = request.message
    system_message = request.system_message
    language = request.language
    
    # Verifica se a mensagem não está vazia
    if not message.strip():
        return {"response": "Mensagem vazia, por favor, envie uma mensagem válida."}
    
    try:
        # Inicializa o cliente do modelo (ajuste conforme necessário)
        client = Client("aifeifei798/feifei-chat")
        
        # Formatação da mensagem para incluir o histórico
        formatted_message = f"{system_message}\n\nHistórico de conversa:\n"
        
        # Adiciona o histórico anterior à mensagem formatada
        for msg in chat_history:
            formatted_message += f"{msg['role']}: {msg['content']}\n"
        
        formatted_message += f"Usuário: {message}"
        
        message_payload = {
            "text": formatted_message,
            "files": []
        }
        
        # Envia a requisição para o modelo sem os parâmetros inválidos
        response = client.predict(
            message=message_payload,
            feifei_select=True,
            additional_dropdown="meta-llama/Llama-3.3-70B-Instruct",
            image_mod="pixtral",
            api_name="/chat"
        )
        
        # Atualiza o histórico com a nova mensagem e a resposta do assistente
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": response})
        
        # Retorna apenas a resposta do assistente
        return {"response": response}
        
    except Exception as e:
        error_msg = TRANSLATIONS[language]["error_message"].format(str(e))
        return {"response": error_msg}

# Função para obter o histórico de conversas
def get_chat_history():
    return {"history": chat_history}

# FastAPI App
app = FastAPI()

@app.post("/respond")
def chat_respond(request: ChatRequest):
    return respond(request)

@app.get("/history")
def history():
    return get_chat_history()
