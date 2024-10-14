from youtube_transcript_api import YouTubeTranscriptApi                # biblioteca para lidar com a API da Youtube
import ollama


# PARTE 1 - Obtendo a Transcricao

idioma = ['pt','en']

video_url = input ("Qual a url do video que deseja resumir?\n")     # Obtem a URL do vídeo
video_id = video_url.split("v=")[-1]                                    # Obtem o id a partir da URL


# So vai funcionar em videos que tem legenda e permitam a transcricao
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=idioma)    # Obtem a transcrição, primeiro tenta em portugues, depois em ingles.
    transcript_text = " ".join([entry['text'] for entry in transcript])             
    print(transcript_text)

except Exception as e:
    print(f"Erro ao obter a transcrição na função get_transcript: {e}")


# PARTE 2 - Obtendo um resumo

# Modelos a ser utilizados, devem estar instalados no ollama, com o mesmo nome
# Adicione todos os que desejar, por exemplo modelos = ['llama3.2:latest','llama3.1:latest', 'gemma2:27b']
modelos = ['llama3.2:latest']

# o prompt é capaz de mudar completamente o estilo e a resposta, então vamos explicar direitinho pra IA O que é pra ela fazer. 
prompt = "Você está assistindo a um vídeo no youtube. Respire fundo, e faça um esquema organizado e detalhado do seguinte texto, pontuando os itens principais e descrevendo o mais detalhadamente possivel seu conteudo: "

for modelo in modelos: 

    resumo = ollama.chat(model=modelo, messages=[{'role':'user','content': prompt+transcript_text}])
    mensagem_resumo = resumo['message']['content']
    print(f"{modelo}:\n{mensagem_resumo}")

