import ollama       # biblioteca para lidar com a API da OLLAMA
import re           # biblioteca para lidar com expressões regulares
import webbrowser   # biblioteca para abrir um site
import os           # biblioteca para lidar com arquivos
import get_transcript   # seu script de transcrição

# Modelos já instalados no Ollama
modelos = ["gpt-oss:20b"]

# Prompt de instrução
prompt = (
    "Você está assistindo a um vídeo no YouTube. "
    "Respire fundo e faça um esquema organizado e detalhado do seguinte texto, "
    "pontuando os itens principais e descrevendo o mais detalhadamente possível seu conteúdo:\n\n"
)

def summarize_with_ollama(text, modelo): 
    """Envia o texto para o modelo do Ollama e retorna o resumo"""
    try:
        saida = ollama.chat(model=modelo, messages=[{'role':'user','content': prompt + text}])
        return saida
    except Exception as e:
        print(f"APP ERROR! {e}")
        return None

def filtrar_string(texto):
    """Remove tags entre colchetes e espaços extras"""
    texto_filtrado = re.sub(r'\[.*?\]', '', texto).strip()
    return texto_filtrado

def criaHtml(modelo, resumo):
    """Cria um arquivo HTML com o resumo"""
    conteudo_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Resumer</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #222;
                color: #cde
            }}
            pre {{
                padding: 15px;
                text-align: justify;
                color: #abc;
                background-color: #222;
                border: 2px solid #568ea6;
                margin: auto;
                white-space: pre-wrap;
                word-wrap: break-word; 
                border-radius: 7px;
                font-size: 16px;
            }}   
        </style>
    </head>
    <body>
        <h1>YouTube Resumer - {modelo}</h1>
        <pre>{resumo}</pre>
    </body>
    </html>
    """

    os.makedirs("data", exist_ok=True)
    arquivo_html = f'./data/html_resume_{re.sub(r"[^a-zA-Z0-9]", "_", modelo)}.html'
    print(f"Iniciando criação do arquivo {arquivo_html}")

    with open(arquivo_html, 'w', encoding='utf-8') as f:
        f.write(conteudo_html)

    caminho_absoluto = os.path.abspath(arquivo_html)
    webbrowser.open(f'file://{caminho_absoluto}')

def main():
    # Solicita a URL do vídeo
    url = input("Qual a URL do vídeo que deseja transcrever?\n").strip()
    
    try:
        # Obtém a transcrição
        transcript = get_transcript.get_transcript(url)
        if not transcript:
            print("Não foi possível obter a transcrição.")
            return
        
        print("\nTranscrição obtida com sucesso. Preparando resumo...\n")
        texto_transcricao = filtrar_string(transcript)

        for modelo in modelos:
            summary = summarize_with_ollama(texto_transcricao, modelo)
            if summary and "message" in summary:
                resumo = summary["message"]["content"]
                print(f"\nResumo gerado pelo modelo {modelo}:\n")
                print(resumo)
                criaHtml(modelo, resumo)
            else:
                print(f"Falha ao gerar o resumo com o modelo {modelo}.")

    except Exception as e:
        print(f"Erro no processo: {e}")

if __name__ == "__main__":
    main()
