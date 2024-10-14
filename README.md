# YoutubeResumer
![OIG1](https://github.com/user-attachments/assets/c4eab0b7-4504-4782-991b-81a2601fd0f7)


Você já quis resumir vídeos longos do YouTube em poucos minutos, extraindo apenas as informações mais importantes para saber se vale à pena assistir? 

Pra isso eu pensei no "Resumidor de Vídeos do Youtube". Mas como queria um nome mais chique e criativo🙄, ficou YoutubeResumer =)

Neste tutorial vamos criar  um resumidor de vídeos do YouTube usando **Python** e **inteligência artificial** local com o ollama. 

Objetivos:

- Descobrir como extrair a transcrição de um vídeo,
- processar a linguagem natural com técnicas de IA e
- gerar resumos concisos,

tudo isso de maneira automatizada e rodando suave.


-----------------------


# 1. Instalando os programas


Os requisitos para que o programa funcione são:

- Instalação do Python e das bibliotecas (uma para transcrição do vídeo e uma para a IA)
- Instalação do Ollama


### 1.1 - Instalando o ollama


Caso ainda não tenha o ollama instalado, faça-o agora mesmo! Quem sabe algum dia sem internet você quer conversar com uma IA, ou no caso de algum evento imprevisto (apocalipse zumbi), ou para manter sua privacidade, ou para realizar testes... Eu realmente recomendo ter o ollama, é simples de instalar e muito poderoso. 

- Para rodar o Ollama, vá até o site www.ollama.com, escolha sua plataforma e instale o programa.
- Em seguida, abra o shell (terminal) ou prompt de comando e digite:

	ollama run llama3.2

caso tudo tenha dado certo, você já está o modelo instalado localmente. 

![Pasted image 20241014162130](https://github.com/user-attachments/assets/905a5842-10e2-4cf6-ba94-75657329f991)


Caso deseje obter um resumo por mais de um modelo, instale quais desejar.
Dependendo da capacidade de seu hardware, especialmente da placa de vídeo (GPU), poderá instalar modelos maiores. 

Se sua máquina tiver que usar a CPU ao invés da GPU o tempo de processamento será maior, mas alguns modelos tem uma eficiência tão boa que permitem um tempo de resposta relativamente baixo. 

Para computadores comuns, o melhor custo-benefício na minha (modesta e imperfeita) opinião, está em:


[**Phi 3.5**](https://ollama.com/library/phi3.5)

O  modelo da Microsoft, com 3.8 bilhões de parâmetros, deve rodar bem mesmo em desktops comuns. Para instalá-lo digite:

	ollama pull phi3.5


[**Llama 3.2**](https://ollama.com/library/llama3.2)

Com uma capacidade também incrível com seus 3.21 bilhões de parâmetros, o llama 3.2 da Meta é uma opção funcional e leve para máquinas desktop. Também disponível na versão de 1 bilhão de parâmetros, para maior velocidade e alta capacidade em dispositivos simples. 

	ollama pull llama3.2               # para o modelo de 3 bilhões de parâmetros
	ollama pull llama3.2:1b            # para o modelo de 1 bilhão de parâmetros
	ollama pull llama3.2:27b           # para o modelo de 27 bilhões de parâmetros


[Llama 3.1]([llama3.1 (ollama.com)](https://ollama.com/library/llama3.1))

Também da Meta, o Llama 3.1 é um pouco mais pesado que seu sucessor, mas extremamente poderoso. Com seus 8 bilhões de parâmetros, é até o momento um dos melhores modelos abertos disponíveis. 

	ollama pull llama3.1              # para o modelo com 8 bilhões de parâmetros
	ollama pull llama3.1:70b          # para o modelo com 70 bilhões de parâmetros
	ollama pull llama3.1:405b         # para o modelo com 405 bilhões de parâmetros


[Gemma2](https://ollama.com/library/gemma2)

Diretamente dos laboratórios do Google, o Gemma 2 é um modelo de alta performance e disponível em 2b, 7b e 29b.

	ollama pull gemma2              # para o modelo com 7 bilhões de parâmetros
	ollama pull gemma2:2b           # para o modelo com 2 bilhões de parâmetros
	ollama pull gemma:27b           # para o modelo com 27 bilhões de parâmetros


[Mistral-Nemo](https://ollama.com/library/mistral-nemo)

O modelo de 12b desenvolvido pela Nvidia, com 128k de contexto (pode lidar com uma grande quantidade de tokens na entrada). 

	ollama pull mistral-nemo



***Caso queira saber quanto um modelo está usando de memória, ou se ele está totalmente carregado em sua GPU ou CPU, ou se está em ambas, utilize o comando***

	ollama ps

![image](https://github.com/user-attachments/assets/a0b01cc6-c71c-473f-ada9-d8163b369efc)



### 1.2 - Python


**Windows:** 

- você pode escolher a versão diretamente da Microsoft Store, ou em [Download Python | Python.org](https://www.python.org/downloads/)

**Linux:** 

- utilize o comando de instalação para sua versão, por exemplo no Debian:

	sudo apt install python3.11-full python3-pip


![Pasted image 20241014163228](https://github.com/user-attachments/assets/80cfe662-f0a0-41e2-8c2f-932bbb67b7bf)



### 1.3 - Instalando as dependências necessárias



Utilize o comando abaixo para instalar as dependências necessárias desse projeto, a api para transcrever o vídeo e a que conectará ao ollama: 

	pip install  youtube_transcript_api ollama


------------------------------------------

# 2. Funcionalidades


### 2.1 Obtendo a transcrição


O programa [**get_transcript.py**](https://github.com/gazstao/YoutubeResumer/blob/main/get_transcript.py) faz a transcrição de um vídeo. 


	#biblioteca para lidar com a API da Youtube
	from youtube_transcript_api import YouTubeTranscriptApi                
	idioma = ['pt','en']
	
	# Obtem a URL do vídeo
	video_url = input ("Qual a url do video que deseja transcrever?\n")     
	
	# Obtem o id a partir da URL
	video_id = video_url.split("v=")[-1]                                    
	
	try:
		transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=idioma)    
		transcript_text = " ".join([entry['text'] for entry in transcript])            
		print(transcript_text)
	
	except Exception as e:
		print(f"Erro ao obter a transcrição na função get_transcript: {e}")



### 2.2 Solicitando o resumo

