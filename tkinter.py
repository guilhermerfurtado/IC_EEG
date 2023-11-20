from flask import Flask
import webbrowser
import threading

app = Flask(__name__)

# Conteúdo a ser exibido na página
conteudo = "Olá, mundo!"

@app.route('/')
def index():
    return f"<h1>Conteúdo:</h1><p>{conteudo}</p>"

def abrir_navegador():
    webbrowser.open_new_tab('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1, abrir_navegador).start()
    app.run(debug=True)
