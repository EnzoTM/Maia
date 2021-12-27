from math import inf
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import random

from datetime import date, datetime

from bd import database

db = database()

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


lista_horario = ["Aliane", "Denilson", "Enzo", "Gabriela"]

horario = None


def verificar():
    """
    Verifica se ja foi dado comida nesse horario
    """
    habilitacao = ["enabled", "enabled", "enabled"]
    informacoes = [None, None, None]

    #pegar o dia atual
    data = date.today()

    horarios = ["manha", "almoco", "janta"]

    #verificar se os horarios estao habilitados para dar comida ou nao
    for i in range(len(horarios)):
        #pegar os registros do dia atual
        resultado = db.query(f"SELECT * FROM {horarios[i]} WHERE data = '{data}'")

        #se tiver algum registro nesse horario
        if len(resultado) != 0:
            #colocar como desabilitado aquele horario
            habilitacao[i] = "disabled"

            informacoes[i] = [resultado[0][0], resultado[0][1], resultado[0][2]]
    
    return habilitacao, informacoes


@app.route("/")
def index():
    habilitacao, informacoes = verificar()

    return render_template("layout.html", lista_link=["manha", "almoco", "janta"], lista=["Manhã", "Almoço", "Janta"], horario="None", habilitacao=habilitacao, informacoes=informacoes)

@app.route("/result", methods=["GET", "POST"])
def result():
    global horario

    #pegar qual botao foi pressionado
    resultado = request.form["submit"]

    #significa que temos que guardar qual foi o horario e ver quem que esta dando a comida
    if resultado in ["manha", "almoco", "janta"]:
        #pegar o horario
        horario = resultado

        #fazer o sorteio entre Gabriela (90%) e Chata (10%)
        lista_horario[3] = random.choices(["Gabriela", "Chata"], weights=(90, 10), k=1)[0]

        #ir para a devida página
        return render_template(f"layout.html", lista_link=lista_horario, lista=lista_horario, horario=horario, habilitacao=["enabled", "enabled", "enabled", "enabled"], informacoes=[None, None, None, None])
    else:
        pessoa = resultado

        data = date.today()

        #pegar o horario atual
        hora_agora = datetime.now()

        #formatar da maneira certa o horario atual
        hora_agora = hora_agora.strftime("%H:%M:%S")

        db.query(f"INSERT INTO {horario} (data, pessoa, horario) VALUES ('{data}', '{pessoa}', '{hora_agora}')", executar=True)

        habilitacao, informacoes = verificar()

        return render_template("layout.html", lista_link=["manha", "almoco", "janta"], lista=["Manhã", "Almoço", "Janta"], horario="None", habilitacao=habilitacao, informacoes=informacoes)