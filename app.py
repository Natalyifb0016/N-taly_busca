from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', endereco=None)

@app.route('/buscarcep', methods=['POST'])
def buscarcep():
    cep = request.form.get('cep', '')

    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    endereco = None
    
    if len(cep_limpo) == 8:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url)
        
        if response.status_code == 200:
            dados = response.json()
            if 'erro' not in dados:
                endereco = dados
            else:
                endereco = {"erro": "CEP não encontrado."}
        else:
            endereco = {"erro": "Erro ao consultar o serviço de CEP."}
    else:
        endereco = {"erro": "CEP inválido. Digite 8 números."}

    return render_template('index.html', endereco=endereco)

if __name__ == '__main__':
    app.run(debug=True)