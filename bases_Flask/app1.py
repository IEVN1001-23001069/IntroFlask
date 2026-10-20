import math
from flask import Flask, render_template, request
app=Flask(__name__)

@app.route('/')   # Ruta o decorador
def index():
    titulo="PWA"
    lista=["Pedro","Luis","Pablo"]
    return render_template ("index.html", titulo=titulo,lista=lista)

@app.route("/operasbas", methods=["GET","POST"])
def operasBas():
    n1=0
    n2=0
    res=0
    operacion=''
    signo=''
    if request.method=='POST':
        n1=request.form.get('n1')
        n2=request.form.get('n2')
        if request.form.get('operacion')== 'sumar':
            res=float(n1) + float(n2)
        elif request.form.get('operacion')== 'restar':
            res=float(n1) - float(n2)
        else:
            res=float(n1) * float(n2)
    return render_template("operasBas.html", n1=n1, n2=n2, res=res)

@app.route("/distancia", methods=["GET","POST"])
def distancia():
    n1=0
    n2=0
    n3=0
    n4=0
    res=0
    if request.method=='POST':
        n1=request.form.get('n1')
        n2=request.form.get('n2')
        n3=request.form.get('n3')
        n4=request.form.get('n4')
        res= math.sqrt(
            math.pow((float(n3) - float(n1)), 2) +
            math.pow((float(n4) - float(n2)), 2)
            )
    
    return render_template("distancia.html", n1=n1, n2=n2, n3=n3, n4=n4, res=res)

@app.route("/hola")
def func():
    return "Hola ..."

@app.route("/user/<string:user>") #Se le pasa un parametro llamado user de tipo string 
def user(user):
    return "Hola: " + user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {} nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return "La suma es {}".format(n1+n2)





if __name__ == "__main__":
    app.run(debug=True) #Permite realizar los cambios sin apagar el servidor

#Creación de servidor web y correr un Hola Mundo 