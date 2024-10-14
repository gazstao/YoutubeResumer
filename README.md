# YoutubeResumer
Resume vídeos do youtube usando Python e Ollama

Você já imaginou poder resumir vídeos longos do YouTube em poucos minutos, extraindo apenas as informações mais importantes? Às vezes recebo algum link ou vejo um título de vídeo e fico pensando se vale à pena assistir. A ideia de transformar vídeos extensos em resumos curtos me pareceu sensacional! 

Neste tutorial vamos criar  um resumidor de vídeos do YouTube usando **Python** e **inteligência artificial** local (ollama). Você descobrirá como extrair a transcrição de um vídeo, processar a linguagem natural com técnicas de IA e gerar resumos concisos, tudo isso de maneira automatizada.
## O que você vai aprender?

Ao longo deste tutorial, vamos explorar:

1. **Como baixar as legendas de vídeos do YouTube**: Utilizando APIs e ferramentas Python para capturar as legendas de maneira simples e eficiente.
2. **Processamento de linguagem natural (NLP)**: Usando bibliotecas de IA para analisar e entender as legendas e identificar as informações mais relevantes.
3. **Gerar resumos inteligentes**: Criar um algoritmo que compila as ideias principais do vídeo em uma versão curta e objetiva.
4. **Dicas e truques para melhorar a precisão** do resumo e customizar os resultados para atender às suas necessidades.

# 1. Instalando os programas

Basicamente precisamos ter instalado no computador o [Ollama](https://ollama.com/) e o Python.

### 1.1 - Ollama

- Para instalar o Ollama, vá até o site www.ollama.com, baixe o programa para sua plataforma e execute-o. 
- Em seguida, abra o shell (terminal) ou prompt de comando e digite:
- ollama run llama3.2

caso tudo tenha dado certo, você já está o modelo instalado localmente. 

![[imagens/Pasted image 20241014162130.png]]

### 1.2 - Python

e o python pode ser instalado da seguinte forma

Windows: você pode escolher a versão diretamente da Microsoft Store, ou em [Download Python | Python.org](https://www.python.org/downloads/)
Linux: utilize o comando de instalação para sua versão, por exemplo no Debian:

	sudo apt install python3.11-full python3-pip

teste sua instalação digitando no shell (ou no prompt de comando) **python3**

![[imagens/Pasted image 20241014163228.png]]

### 1.3 - Instalando as dependências necessárias

Utilize o comando abaixo para instalar as dependências necessárias desse projeto, a api para transcrever o vídeo e a que conectará ao ollama: 

	pip install  youtube_transcript_api ollama


# 2. Obtendo a transcrição

Use o editor de sua preferência (vscode, notepad, vim... ) para criar o seguinte programa:

**get_transcript.py**

from youtube_transcript_api import YouTubeTranscriptApi                # biblioteca para lidar com a API da Youtube
idioma = ['pt','en']

video_url = input ("Qual a url do video que deseja transcrever?\n")     # Obtem a URL do vídeo
video_id = video_url.split("v=")[-1]                                    # Obtem o id a partir da URL

try:
	transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=idioma)    
	transcript_text = " ".join([entry['text'] for entry in transcript])            
	print(transcript_text)

except Exception as e:
	print(f"Erro ao obter a transcrição na função get_transcript: {e}")