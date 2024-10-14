from youtube_transcript_api import YouTubeTranscriptApi                # biblioteca para lidar com a API da Youtube
import ollama


# PARTE 1 - Obtendo a Transcricao

idioma = ['pt','en']

video_url = input ("Qual a url do video que deseja transcrever?\n")     # Obtem a URL do vídeo
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
# Adicione todos os que desejar
modelos = ['llama3.2:latest','phi3.']

for modelo in modelos: 
    