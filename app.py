import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import base64
import io

from sympy import *
from flask import Flask, render_template, request
from PIL import Image

def alg_e(funcion, x0, xN, y0, h, func):
    x = np.arange(x0, xN + h, h)
    n = len(x)
    y = np.zeros(n)
    y[0] = y0
    for i in range(0, n - 1):
        y[i + 1] = y[i] + (funcion(x[i], y[i], func) * h)
    return x, y

def alg_em(funcion, x0, xN, y0, h, func):
    x = np.arange(x0, xN + h, h)
    n = len(x)
    y = np.zeros(n)
    y[0] = y0
    for i in range(0, n - 1):
        k1 = funcion(x[i], y[i], func)
        k2 = funcion(x[i] + h / 2, y[i] + k1 * h / 2, func)
        y[i + 1] = y[i] + (h / 2) * (k1 + k2)
    return x, y

def alg_rk(funcion, x0, xN, y0, h, func):
    x = np.arange(x0, xN + h, h)
    n = len(x)
    y = np.zeros(n)
    y[0] = y0
    for i in range(0, n - 1):
        k1 = funcion(x[i], y[i], func)
        k2 = funcion(x[i] + h / 2, y[i] + k1 * h / 2, func)
        k3 = funcion(x[i] + h / 2, y[i] + k2 * h / 2, func)
        k4 = funcion(x[i] + h, y[i] + k3 * h, func)
        y[i + 1] = y[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return x, y

#Calculo el resultado de la funcion parametro
def funcion(x0, xN, func):
    if 'x' in func and 'y' in func:
      nu = eval(func.replace("x", "("+str(x0)+")").replace("y", "("+str(xN)+")"))
    if 'x' in func and 'y' not in func:
      nu = eval(func.replace("x", "("+str(x0)+")"))
    if 'x' not in func and 'y' in func:
      nu = eval(func.replace("y", "("+str(x0)+")"))
    return nu

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        if(not request.form.get("funcion")):
            print("Error")
        else:
            func = request.form.get("funcion")
            x0 = int(request.form.get("x0"))
            xN = int(request.form.get("xfinal"))
            yo = int(request.form.get("y0"))
            h = float(request.form.get("interval"))
        
            p, r = alg_rk(funcion, x0, xN, yo, h, func)
            d, u = alg_e(funcion, x0, xN, yo, h, func)
            j, k = alg_em(funcion, x0, xN, yo, h, func)

            plt.plot(p, r,'-o')
            plt.plot(d, u, '-o')
            plt.plot(j, k, '-o')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(func)
            plt.legend(('Runge-Kutta', 'euler', 'euler_mejorado'))
            plt.grid(True)
            plt.savefig('graf/Figure_1.jpg')
            plt.close("all")
           
            im = Image.open("graf/Figure_1.jpg")
            data = io.BytesIO()
            im.save(data, "JPEG")
            im.close
            encoded_img_data = base64.b64encode(data.getvalue())

            return render_template("indexWithResponse.html", rtaFunc=func, rtaX0=x0, rtaXfinal=xN, rtaY0=yo, rtaH=h, img_data=encoded_img_data.decode('utf-8')); 

    return render_template("index.html")

plt.close("all")

if __name__=='__main__':
   app.run()




