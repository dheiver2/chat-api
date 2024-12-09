import gradio as gr
from typing import List, Dict
from gradio_client import Client

def create_chat_app():
    TRANSLATIONS = {
        "en": {
            "title": "🤖 Chat with Llama 3.3 70B",
            "description": """
            This is a chatbot based on the Llama 3.3 70B model. To use:
            1. Type your message in the field below
            2. Adjust parameters as needed
            3. Click Send or press Enter
            """,
            "system_message": "You are a helpful and friendly assistant based on the Llama 3.3 70B model.",
            "system_message_label": "System Message",
            "max_tokens_label": "Maximum Tokens",
            "temperature_label": "Temperature",
            "top_p_label": "Top-p (Nucleus Sampling)",
            "message_placeholder": "Type your message here...",
            "send_button": "Send",
            "clear_button": "Clear Chat",
            "info_section": """
            ### ℹ️ Information
            - Model: Llama 3.3 70B Instruct
            - Language: English/Portuguese
            - Hosting: Hugging Face Spaces
            """,
            "error_message": "Sorry, an error occurred: {}\nPlease check your connection and settings.",
            "examples": [
                "Hello! How are you?",
                "Can you explain what artificial intelligence is?",
                "What is the capital of Brazil?",
                "Help me write a Python code to calculate Fibonacci."
            ]
        },
        "pt": {
            "title": "🤖 Chat com Llama 3.3 70B em Português",
            "description": """
            Este é um chatbot baseado no modelo Llama 3.3 70B. Para usar:
            1. Digite sua mensagem no campo abaixo
            2. Ajuste os parâmetros conforme necessário
            3. Clique em Enviar ou pressione Enter
            """,
            "system_message": "Você é um assistente amigável e prestativo que responde em português. Você é baseado no modelo Llama 3.3 70B.",
            "system_message_label": "Mensagem do Sistema",
            "max_tokens_label": "Máximo de Tokens",
            "temperature_label": "Temperatura",
            "top_p_label": "Top-p (Amostragem Nucleus)",
            "message_placeholder": "Digite sua mensagem aqui...",
            "send_button": "Enviar",
            "clear_button": "Limpar Chat",
            "info_section": """
            ### ℹ️ Informações
            - Modelo: Llama 3.3 70B Instruct
            - Idioma: Português/Inglês
            - Hospedagem: Hugging Face Spaces
            """,
            "error_message": "Desculpe, ocorreu um erro: {}\nPor favor, verifique sua conexão e configurações.",
            "examples": [
                "Olá! Como você está?",
                "Pode me explicar o que é inteligência artificial?",
                "Qual é a capital do Brasil?",
                "Me ajude a escrever um código em Python para calcular fibonacci."
            ]
        }
    }

    def respond(
        message: str,
        chat_history: List[Dict],
        system_message: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        language: str,
    ):
        if not message.strip():  # Não processa mensagens vazias
            return chat_history, ""
            
        try:
            client = Client("aifeifei798/feifei-chat")
            
            formatted_message = f"{system_message}\n\nConversation history:\n"
            for msg in chat_history:
                formatted_message += f"{msg['role']}: {msg['content']}\n"
            
            formatted_message += f"User: {message}"
            
            message_payload = {
                "text": formatted_message,
                "files": []
            }
            
            response = client.predict(
                message=message_payload,
                feifei_select=True,
                additional_dropdown="meta-llama/Llama-3.3-70B-Instruct",
                image_mod="pixtral",
                api_name="/chat"
            )
            
            chat_history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ])
            
            return chat_history, ""
            
        except Exception as e:
            error_msg = TRANSLATIONS[language]["error_message"].format(str(e))
            chat_history.append({"role": "assistant", "content": error_msg})
            return chat_history, ""

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        current_language = gr.State("en")
        
        gr.Markdown(TRANSLATIONS["en"]["title"])
        gr.Markdown(TRANSLATIONS["en"]["description"])
        
        with gr.Group():
            chatbot = gr.Chatbot(
                value=[],
                height=400,
                type="messages"
            )
            
            with gr.Row():
                message = gr.Textbox(
                    placeholder=TRANSLATIONS["en"]["message_placeholder"],
                    lines=3,
                    scale=9  # Ocupa 90% do espaço
                )
                send_btn = gr.Button(
                    TRANSLATIONS["en"]["send_button"], 
                    variant="primary",
                    scale=1  # Ocupa 10% do espaço
                )
            
            with gr.Accordion("Settings/Configurações", open=False):
                system_message = gr.Textbox(
                    value=TRANSLATIONS["en"]["system_message"],
                    label=TRANSLATIONS["en"]["system_message_label"]
                )
                
                with gr.Row():
                    max_tokens = gr.Slider(
                        minimum=1,
                        maximum=4096,
                        value=2048,
                        step=1,
                        label=TRANSLATIONS["en"]["max_tokens_label"]
                    )
                    temperature = gr.Slider(
                        minimum=0.1,
                        maximum=2.0,
                        value=0.7,
                        step=0.1,
                        label=TRANSLATIONS["en"]["temperature_label"]
                    )
                    top_p = gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        value=0.95,
                        step=0.05,
                        label=TRANSLATIONS["en"]["top_p_label"]
                    )
            
            with gr.Row():
                language_selector = gr.Radio(
                    choices=["en", "pt"],
                    value="en",
                    label="Language/Idioma",
                    interactive=True
                )
                
                clear_btn = gr.Button(TRANSLATIONS["en"]["clear_button"])
        
        gr.Markdown(TRANSLATIONS["en"]["info_section"])
        
        gr.Examples(
            examples=TRANSLATIONS["en"]["examples"],
            inputs=message
        )
        
        # Event handlers
        send_btn.click(
            respond,
            [message, chatbot, system_message, max_tokens, temperature, top_p, language_selector],
            [chatbot, message]
        )
        
        message.submit(  # Permite também enviar com Enter
            respond,
            [message, chatbot, system_message, max_tokens, temperature, top_p, language_selector],
            [chatbot, message]
        )
        
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, message])
        
        def update_language(lang):
            trans = TRANSLATIONS[lang]
            return (
                trans["message_placeholder"],
                trans["system_message"],
                trans["system_message_label"],
                trans["max_tokens_label"],
                trans["temperature_label"],
                trans["top_p_label"],
                trans["send_button"],
                trans["clear_button"]
            )
        
        language_selector.change(
            update_language,
            inputs=[language_selector],
            outputs=[
                message,
                system_message,
                system_message,
                max_tokens,
                temperature,
                top_p,
                send_btn,
                clear_btn
            ]
        )

    return demo

if __name__ == "__main__":
    demo = create_chat_app()
    demo.launch(share=False)