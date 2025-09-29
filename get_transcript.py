from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
import re
import os

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]  # Remove a barra inicial
    elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None

idioma = ['pt', 'en']

video_url = input("Qual a URL do vídeo que deseja transcrever?\n")
video_id = extract_video_id(video_url)

if not video_id:
    print("URL inválida ou ID do vídeo não encontrado.")
    exit()

try:
    # Instancie a API
    api = YouTubeTranscriptApi()
    
    # Lista as transcrições disponíveis
    transcript_list = api.list(video_id)
    
    # Encontra uma transcrição nos idiomas desejados
    transcript = transcript_list.find_transcript(idioma)
    
    # Obtém a transcrição
    fetched_transcript = transcript.fetch()
    
    # Transforma em texto puro
    transcript_text = " ".join(
        re.sub(r'\[.*?\]', '', entry.text).strip()
        for entry in fetched_transcript
        if entry.text.strip() and not re.fullmatch(r'\[.*?\]', entry.text.strip())
    )

    if not transcript_text:
        print("Nenhum texto válido encontrado na transcrição.")
        exit()
    
    print("\nTranscrição limpa:\n")
    print(transcript_text)

    gravar = input("\nDeseja gravar? (s/n) ").lower()
    if gravar and gravar[0] == 's':
        os.makedirs("data", exist_ok=True)
        with open(f"data/{video_id}.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(transcript_text)
        print("Gravado com sucesso em data/{}.txt".format(video_id))

except NoTranscriptFound:
    print("Nenhuma transcrição disponível nos idiomas especificados (pt, en). Tente outro vídeo com legendas.")
except TranscriptsDisabled:
    print("As transcrições estão desabilitadas para este vídeo pelo criador do conteúdo.")
except Exception as e:
    print(f"Erro ao obter a transcrição: {e}")
    import traceback
    traceback.print_exc()  # Exibe o traceback completo para depuração
