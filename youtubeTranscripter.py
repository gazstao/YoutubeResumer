import json         # biblioteca para lidar com o Jason
import ollama      # biblioteca para lidar com a API da OLLAMA
from youtube_transcript_api import YouTubeTranscriptApi       # biblioteca para lidar com a API da Youtube
import re           # biblioteca para lidar com expressoes regulares
import webbrowser     # biblioteca para abrir um site
import os           # biblioteca para lidar com arquivos


# Ajuste os modelos, se necessário
# Caso queira somente uma resposta, deixe somente um modelo, caso queira mais respostas, adicione os modelos desejados.
# Esses modelos já devem estar instalados no ollama, e devem constar com o mesmo nome 

modelos = ["llama3.2:latest"]

# o prompt é capaz de mudar completamente o estilo e a resposta, então vamos explicar direito pra IA O que é pra ela fazer. 
prompt_system = "Você é um corretor que vai pontuar corretamente o seguinte texto, colocando toda a pontuação necessária para que tenha sentido e colocando a próxima frase em uma nova linha, sem alterar o conteudo do que está escrito."

# E vamos escolher quais idiomas nos interessam, de acordo com 
idioma = ['pt','en']

# Obtem a transcrição do video escolhido na linguagem pre-definida, une o texto fragmentado e retorna o resultado
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=idioma)
        transcript_text = " ".join([entry['text'] for entry in transcript])

        # Grava transcricao em arquivo de texto 
        with open(".\\data\\transcript_"+video_id+".txt","a") as arquivo:
            arquivo.write(transcript_text)
            arquivo.write("\n\n----------------------------------------\n\n")
            return transcript_text
        
    except Exception as e:
        print(f"Erro ao obter a transcrição na função get_transcript: {e}")
        return None


# Obtem um texto e um ID de arquivo para gravar o resultado, e cria um resumo usando o Ollama
def summarize_with_ollama(prompt_text, modelo): 
    try:
        saida = ollama.chat(model=modelo, messages=[{'role':'system','content': prompt_system},
                                                     {"role": "user", "content": prompt_text}])
        json_bonito_saida = json.dumps(saida,indent=4)
        print(json_bonito_saida)
        return(saida['message']['content'])

    except Exception as e:
        print(f"Erro: {e}")
        return None


# Função principal: solicita a URL do video, obtém a transcrição e cria um arquivo html para visualização 
def main():
    url = input("Insira o URL do vídeo do YouTube: ")
    video_id = url.split("v=")[-1]

    transcript = get_transcript(video_id)
    print("Transcrição: "+transcript)

    if transcript:
        texto_transcricao = filtrar_string(transcript)
        print(texto_transcricao)
        print("Transcrição obtida com sucesso...\nAnalisando o resultado. Aguarde...")
        
        for modelo in modelos:
            # Enviar a transcrição para o Ollama e obter o resumo
            summary = summarize_with_ollama(texto_transcricao, modelo)
            print("Resumo: "+summary)

            # Criar um arquivo HTML com o resumo
            if summary:
                criaHtml(modelo, summary, video_id, url)
            else:
                print("Falha ao gerar o resumo.")

    else:
        print("Não foi possível obter a transcrição.")
    


def filtrar_string(texto):
    texto_filtrado = re.sub(r'[^\w\s]', '', texto)
    return texto_filtrado


def criaHtml(modelo, texto, video_id, url):
    conteudo_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Transcripter</title>
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
        <h1>YouTube Transcripter - {modelo}</h1>
        <p><a href="{url}">{url}</a></p>
        <pre>{texto}</pre>
    </body>
    </html>
    """

    # Nome do arquivo HTML
    arquivo_html = './data/html_resume_'+filtrar_string(modelo)+"_"+video_id+'.html'
    print (f"Iniciando criacao do arquivo {arquivo_html}")

    # Salvando o arquivo HTML
    with open(arquivo_html, 'w', encoding='utf-8') as f:
        f.write(conteudo_html)

    # Abrindo o arquivo HTML no navegador automaticamente
    caminho_absoluto = os.path.abspath(arquivo_html)
    webbrowser.open(f'file://{caminho_absoluto}')

if __name__ == "__main__":
    main()
