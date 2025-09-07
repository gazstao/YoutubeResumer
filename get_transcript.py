from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id):
    try:
        # Instancie a API
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch da transcrição (use languages=['pt'] para português, se quiser)
        transcript_list = ytt_api.fetch(video_id)  # Tente PT primeiro, fallback para EN
        
        # Junte todos os textos em uma string única
        transcript_text = ' '.join([entry['text'] for entry in transcript_list])
        
        return transcript_text  # Retorna a string da transcrição
    
    except (TranscriptsDisabled, NoTranscriptFound):
        print("Erro: Transcrição não disponível para este vídeo.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao obter transcrição: {e}")
        return None
    
video_id = input ("Link do vídeo para obter transcrição: ")
video_id = video_id.split("v=")[-1]   
get_transcript(video_id)