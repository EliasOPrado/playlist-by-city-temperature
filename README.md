# Weather To Music Service

### Visão Geral
<br>
O projeto é uma aplicação web desenvolvida em Django que fornece recomendações de playlists musicais baseadas na temperatura da cidade informada pelo usuário. A aplicação é implantada usando Docker para garantir consistência entre os ambientes de desenvolvimento e produção, e hospedada no Render.com para aproveitar sua capacidade de escalabilidade e facilidade de uso.

## Componentes Principais ⚙️

1. **Backend - Django**
    * **Framework**: Django foi escolhido como o framework de backend devido à sua robustez, e alem de sua segurança embutida e rica coleção de funcionalidades prontas para uso, como autenticação, administração e ORM, a escolha foi feita pela experiencia de trabalho com a mesma.
    * **Estrutura MVC**: Django segue o padrão MVC (Model-View-Controller), facilitando a separação de responsabilidades e manutenção do código.
    * **REST API**: Implementada usando Django REST Framework, que simplifica a criação de APIs RESTful e fornece suporte para serialização de dados com mais facilidade.
2. **Docker**
    * **Containerização**: Docker é utilizado para empacotar a aplicação e suas dependências em contêineres, garantindo que a aplicação funcione de forma consistente em diferentes ambientes.
    * **Facilidade de Deploy**: Usar Docker simplifica o processo de implantação e escalabilidade no Render.com, além de permitir uma rápida recuperação em caso de falhas.
3. **Render.com**
    * **Hospedagem**: Render.com é utilizado como plataforma de hospedagem devido à sua facilidade de uso, suporte para integração contínua e escalabilidade automática.
    * **Gerenciamento de Ambiente**: Facilita o gerenciamento de variáveis de ambiente e ajustes de configuração sem a necessidade de modificações no código fonte.
4. **Serviços Externos**
    * [OpenWeatherMap API:](https://openweathermap.org/api) Usada para obter dados meteorológicos baseados na cidade do usuário.
    * [Spotify API:](https://developer.spotify.com/) Utilizada para buscar playlists musicais com base nos critérios definidos pela temperatura.

### Desafios e Considerações Futuras

* **Escalabilidade**: A arquitetura foi projetada para ser escalável, mas monitorar o desempenho e ajustar a infraestrutura será crucial conforme a base de usuários cresce.
* **Segurança**: A segurança das comunicações e do armazenamento de dados é uma prioridade contínua, com planos para implementar autenticação OAuth para acesso às APIs externas.
* **Melhorias na Experiência do Usuário**: Futuras iterações podem incluir recomendações personalizadas baseadas no histórico do usuário e melhorias. Alem do mais, algumas funcionalidades não foram implementadas pelo espaço muito curto de tempo como a implementação de autenticação, cache e integração continua para checar se o deployment sempre estará health e no ar, checando os testes unitarios e/ou lint.

## Processo de deployment 📦

#### Dockerfile

* **Imagem Base**: Utilizamos o Python 3.9 como base, garantindo compatibilidade com as versões das bibliotecas necessárias.
* **Configuração do Diretório de Trabalho**: O diretório de trabalho `/app` foi definido para manter a organização do projeto.
* **Gerenciamento de Dependências**:
    * Foram instaladas as dependências listadas em `requirements.txt`, incluindo `gunicorn` para servir a aplicação em produção.
    * Usamos `--no-cache-dir` para evitar a criação de cache durante a instalação de pacotes, economizando espaço.
* **Comando de Inicialização**:
    * O Gunicorn foi configurado para iniciar o servidor WSGI do Django, vinculando-o a `0.0.0.0:8000` para assegurar que o contêiner aceite conexões externas.

#### docker-compose.yml

* **Serviço Web**: Configurado para construção local da imagem e execução da aplicação via `python manage.py runserver`, simplificando o desenvolvimento e testes locais.
* **Mapeamento de Portas**: A porta 8000 foi mapeada do contêiner para a porta 8000 do host para acessar a aplicação localmente.
* **Volumes**: Utilizamos volumes para sincronizar o diretório de código local com o contêiner, facilitando o desenvolvimento contínuo com mudanças de código refletidas em tempo real.

### Configurações do Django

#### Arquivo settings.py

* **Chave Secreta e Debug**:
    * Foram ultilizados variáveis de ambiente para a `SECRET_KEY` e definimos `DEBUG` como `True` para desenvolvimento. Isso será alterado para `False` em produção por motivos de segurança.
* **Configuração de Middleware**:
    * Foi incluido o `WhiteNoiseMiddleware` para servir arquivos estáticos diretamente através do Django em produção, eliminando a necessidade de um servidor web separado como Nginx para este propósito.
* **Armazenamento de Arquivos Estáticos**:
    * Foi configurado `STATICFILES_STORAGE` para usar `CompressedManifestStaticFilesStorage`, que ajuda no gerenciamento eficiente de cache de arquivos estáticos.
* **Carregamento de Variáveis de Ambiente**:
    * Foi usado `python-dotenv` para carregar variáveis de ambiente sensíveis, como chaves de API para serviços externos.

#### Implantação no Render.com

* **Configuração do Serviço**:
    * Foi criado um serviço web no [Render.com](render.com), configurando-o para construir a partir do repositório conectado e usando o Docker para gerenciar a construção e execução do contêiner.
    * Garantindo que o contêiner esteja ouvindo na porta fornecida pelo ambiente do Render.
* **Gerenciamento de Variáveis de Ambiente**:
    * Foi configurado variáveis de ambiente no painel do Render para gerenciar chaves de API e outras configurações sensíveis.

## Como rodar a aplicação localmente 🚀

Antes de tudo para rodar a aplicação localmente e necessario um arquivo `.env` na raiz do repositorio. E nele será necessario as seguintes variaveis:
<br>
```
WEATHER_API_KEY=<adicionar chave aqui>
SPOTIFY_CLIENT_ID=<adicionar chave aqui>
SPOTIFY_CLIENT_SECRET=<adicionar chave aqui>
DEBUG=True
```

Para conseguir acesso a `WEATHER_API_KEY` sera necessário criar uma conta em [https://home.openweathermap.org/](https://home.openweathermap.org/api_keys) e ir para `My Api Keys` onde voce terá acesso a todas suas chaves de API.

Agora para ter acesso a <span class="colour" style="color:var(--vscode-markdown-wysText)">`SPOTIFY_CLIENT_ID` e </span>`SPOTIFY_CLIENT_SECRET`<span class="colour" style="color:var(--vscode-markdown-wysText)"> será necessario:</span>

1. <span class="colour" style="color:var(--vscode-markdown-wysText)">ir ao link </span>[https://developer.spotify.com/](https://developer.spotify.com/)
2. Criar uma conta se ja não tiver
3. Criar um aplicativo dentro do dashboard
4. E dentro do aplicativo criado, va a settings onde se encontrará as chaves como `client id` e `client secret` .

Com as chaves criadas e com docker instalado na sua maquina, rode o comando:
<br>
```
docker compose up --build
```

Com isso o projeto irá iniciar.
<br>
## Endpoints

Rodando a aplicação localmente você podera seguir o seguinte padrão de url:
<br>
```
http://localhost:8000/api/playlist/<str: city>
```

Você também poderá seguir com o link do projeto que esta na nuvem com a seguinte url de exemplo:
<br>
```
https://playlist-by-city-temperature.onrender.com/api/playlist/london/
```

## Detalhes das funcionalidades 💻

O projeto foi inicializado criando se a consexão com os dois serviços:

* [https://openweathermap.org/api](https://openweathermap.org/api)
* [https://developer.spotify.com/](https://developer.spotify.com/)

Como a funcionalidade do serviço basicamente é retornar uma lista de musica baseando-se na temperatura da cidade escolhida. Foram-se criado dois services para auxiliar nesse trabalho.
<br>
1. Para chamar o endpoint do `openweathermap` onde se terá acesso as cidades e a temperatura da mesma:

``` python
def get_temperature_by_city(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

    if "main" in data and "temp" in data["main"]:
        temp = int(data["main"]["temp"] - 273.15)
        return {"city": data["name"], "temperature": int(temp)}

    else:
        logger.error(f"Unexpected response format: {data}")
        return {"error": "Unexpected response format"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return {"error": "Unexpected response format"}
```

Agora, para fazer as chamadas dos dados de musica duas outras funções foram criadas onde uma serão usada para a obtenção do token e a segunda para o acesso ao endpoint necessario para trazer as listas de musica (baseando-se ja na função `get_temperature_by_city()`):
<br>
``` python
def get_spotify_access_token():
    url = "[https://accounts.spotify.com/api/token](https://accounts.spotify.com/api/token)"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()

        if "access_token" in response_data:
            return response_data["access_token"]
        else:
            logger.error(f"Failed to retrieve access token: {response_data}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving Spotify access token: {e}")
        return None


def get_playlist_by_genre(genre):
    access_token = get_spotify_access_token()
    if not access_token:
        return {"error": "Failed to retrieve Spotify access token"}

    url = f"[https://api.spotify.com/v1/search?q=genre:{genre}&type=album&limit=10](https://api.spotify.com/v1/search?q=genre:{genre}&type=album&limit=10)"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "albums" in data and "items" in data["albums"]:
            albums = [
                {
                    "name": album["name"],
                    "artist": album["artists"][0]["name"],
                    "release_date": album["release_date"],
                    "url": album["external_urls"]["spotify"],
                    "genre": genre,
                }
                for album in data["albums"]["items"]
              ]
            return albums
        else:
            logger.error(f"Unexpected response format: {data}")
            return {"error": "Unexpected response format"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching albums by genre: {e}")
        return JsonResponse(
            {"error": "Failed to fetch albums by genre"},
            status=response.status_code if response else 500,
         )
```

Por ultimo uma APIView chamada <span class="colour" style="color:rgb(139, 233, 253)">`PlaylistByCityTemperatureAPIView`</span> foi criada para gerenciar a logica entre esses dois services, adicionar a logica necessaria para retornar as lista necessaria baseando-se nos critérios do desafio e gerenciar possiveis erros. Usando try e catch exceptions com mensagens de erros intuitivas para futuras manutenções.
<br>
``` python
class PlaylistByCityTemperatureAPIView(APIView):
    def get(self, request, city, format=None):

        temp_data = get_temperature_by_city(city)

        if not temp_data or "temperature" not in temp_data:
            error_message = temp_data.get("error", "No temperature data returned")
            logger.error(f"Temperature service error: {error_message}")
            return Response(
                  {
                      "error": f"Failed to retrieve temperature data for {city}: {error_message}"
                  },
                  status=status.HTTP_500_INTERNAL_SERVER_ERROR,
             )

        temperature = temp_data["temperature"]

        if temperature > 25:
            genre = "pop"
        elif 10 <= temperature <= 25:
            genre = "rock"
        elif temperature < 10:
            genre = "classical"

        playlists = get_playlist_by_genre(genre)

        if not playlists or not isinstance(playlists, list):
            logger.error(
                f"Playlist service error: No playlists data returned or incorrect format"
            )
            return Response(
                  {
                      "error": f"Failed to retrieve playlists for genre {genre}: No playlists data returned or incorrect format"
                  },
                  status=status.HTTP_500_INTERNAL_SERVER_ERROR,
              )

        return Response(
              {
                  "city": city,
                  "temperature": f"{temperature} degree celcius",
                  "genre": genre,
                  "playlists": playlists,
              },
              status=status.HTTP_200_OK,
          )
```

Nos testes foram usando `mock` para não consumir as APIs excessivamente.
<br>
## Controle de versão 🌿

Durante o desenvolvimento deste projeto, acabei fazendo push diretamente para a branch `master`, sem criar branches separadas para cada conjunto de alterações. Embora eu tenha conhecimento da importância de criar branches para cada nova funcionalidade ou tarefa, a pressão do tempo e a necessidade de entregar rapidamente me levaram a seguir esse caminho. Percebi o erro após já ter avançado parte do projeto, e, devido às circunstâncias, optei por manter esse padrão até a conclusão.
