from flask import *
import requests
import re


links = []
title = []

#Faz a requisição pra page de trending do YT, e ser der erro, mostra no prompt
try:
    req = requests.get('https://www.youtube.com/feed/trending')

except Exception as erro:
    print('Não foi possível acessar!\n')

#Se ok, busca em req qualquer ocorrencia que contenha a expressão regular determinada e cria uma lista em search
search = re.findall(r'https://i.ytimg.com/vi/\S+[/]', req.text)

#Busca na lista search por um determinado pedaço de string, e substitui por outro, concatenando
#com o que não foi descartado e cria um vetor de links
for i in range(0, len(search)):
    find = search[i].replace('https://i.ytimg.com/vi/', 'https://www.youtube.com/watch?v=')
    links.append(find)

#Faz a requisição na página do link da lista de links
for i in range(0, 5):
    try:
        req2 = requests.get(links[i])

    except Exception as erro:
        print('Não foi possível acessar!\n')

    #Se ok, busca em req2 qualquer ocorrencia que contenha a expressão regular determinada e cria uma lista em search2
    search2 = re.findall(r'<title>.+</title>', req2.text)

    #converte a lista search 2 em string para poder cortar os caracteres, a modo de  uma leitura mais limpa
    search2 = search2.__str__().replace(' - YouTube</title>', '')
    search2 = search2.__str__().replace('<title>', '')
    search2 = search2.__str__().replace('[', '')
    search2 = search2.__str__().replace(']', '')
    search2 = search2.__str__().replace("'", '')
    title.append(search2)
#Imprime o que foi solicitado
'''for i in range(0, 5):
    print('Vídeo:', i+1, "->", title[i])
    print('Link:', links[i])
    print('\n')'''

app = Flask(__name__)


@app.route('/')
def requestyoutube():
        return render_template('index.html', title=title, links=links)


if __name__ == "__main__":
    app.run(debug=True)

