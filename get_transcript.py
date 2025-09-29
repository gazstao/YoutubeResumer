from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
import re
import os

idioma = ['pt', 'en']

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]  # Remove a barra inicial
    elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None

def get_transcript(video_url: str, save: bool = False) -> str:
    """Retorna a transcrição limpa de um vídeo do YouTube (em pt ou en)."""
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("URL inválida ou ID do vídeo não encontrado.")

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(idioma)
        fetched_transcript = transcript.fetch()

        transcript_text = " ".join(
            re.sub(r'\[.*?\]', '', entry.text).strip()
            for entry in fetched_transcript
            if entry.text.strip() and not re.fullmatch(r'\[.*?\]', entry.text.strip())
        )

        if not transcript_text:
            raise ValueError("Nenhum texto válido encontrado na transcrição.")

        if save:
            os.makedirs("data", exist_ok=True)
            with open(f"data/{video_id}.txt", "w", encoding="utf-8") as arquivo:
                arquivo.write(transcript_text)

        return transcript_text

    except NoTranscriptFound:
        raise RuntimeError("Nenhuma transcrição disponível nos idiomas especificados (pt, en).")
    except TranscriptsDisabled:
        raise RuntimeError("As transcrições estão desabilitadas para este vídeo pelo criador do conteúdo.")
    except Exception as e:
        raise RuntimeError(f"Erro ao obter a transcrição: {e}")

# Se rodar diretamente: pede URL e imprime
if __name__ == "__main__":
    url = input("Qual a URL do vídeo que deseja transcrever?\n")
    try:
        texto = get_transcript(url, save=True)
        print("\nTranscrição limpa:\n")
        print(texto)
    except Exception as e:
        print(e)
