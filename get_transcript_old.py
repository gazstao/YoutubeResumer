from youtube_transcript_api import YouTubeTranscriptApi                # biblioteca para lidar com a API da Youtube

idioma = ['br','pt','en']

video_url = input ("Qual a url do video que deseja transcrever?\n")     # Obtem a URL do vídeo
video_id = video_url.split("v=")[-1]                                    # Obtem o id a partir da URL

# So vai funcionar em videos que tem legenda e permitam a transcricao
try:
    transcript = YouTubeTranscriptApi.fetch(video_id, languages=idioma)    # Obtem a transcrição, primeiro tenta em portugues, depois em ingles.
    transcript_text = " ".join([entry['text'] for entry in transcript])             
    print(transcript_text)
    gravar = input("Deseja gravar? (s/n)").lower()
    if gravar[0]=='s':
        with open("data/"+video_id+".txt","w") as arquivo:
            arquivo.write(transcript_text)
        print("gravado com sucesso...")

except Exception as e:
    print(f"Erro ao obter a transcrição na função get_transcript: {e}")