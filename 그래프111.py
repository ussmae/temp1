from math import *
import numpy as np
import matplotlib.pyplot as plt
import json
from excel_change import input_to_Excel
from mpl_toolkits.mplot3d import Axes3D
from flask import Flask, render_template
import base64
import io
from PIL import Image

###################################################################################################################
# 유일한 변수

NumDiv = 101

###################################################################################################################
# 함수

def var2_max_input(var0,var1):
    try:
        type(eval(var2_MaxInput))
    except:
        return eval(var2_MaxInput)
    return np.full((NumDiv, NumDiv), eval(var2_MaxInput))
def var2_min_input(var0,var1):
    try:
        type(eval(var2_MinInput))
    except:
        return eval(var2_MinInput)
    return np.full((NumDiv, NumDiv), eval(var2_MinInput))
def var0_max_input():
    return eval(var0_MaxInput)
def var0_min_input():
    return eval(var0_MinInput)
def var1_max_input(var0):
    return eval(var1_MaxInput)
def var1_min_input(var0):
    return eval(var1_MinInput)

###################################################################################################################
# 문제 가져오기

Pb = {"Coordinates": "Cartesian xyz", "0var": {"from": "1", "to": "2"}, "1var": {"from": "0", "to": "3"}, "2var": {"from": "0", "to": "1+x**2+3*y"}, "Shade": "True", "AllGraph": "True", "contour": "False"}

###################################################################################################################
# 함수 읽을 수 있는 형태로 고치기

var0 = Pb["Coordinates"][-3]
var1 = Pb["Coordinates"][-2]
var2 = Pb["Coordinates"][-1]

Mod_func = []
all_func = [Pb["0var"]["from"], Pb["0var"]["to"], Pb["1var"]["from"], Pb["1var"]["to"], Pb["2var"]["from"], Pb["2var"]["to"]]
for b in all_func:
    for a in "var0","var1","var2":
        if eval(a) == "x":
            b = b.replace("x", a)
        elif eval(a) == "y":
            b = b.replace("y", a)
        elif eval(a) == "z":
            b = b.replace("z", a)
    Mod_func.append(b)

var2_MaxInput = str(Mod_func[5])
var2_MinInput = str(Mod_func[4])
var1_MaxInput = str(Mod_func[3])
var1_MinInput = str(Mod_func[2])
var0_MaxInput = str(Mod_func[1])
var0_MinInput = str(Mod_func[0])

ReplcWord = ["sin", "cos", "tan", "csc", "sec", "cot", "exp", "sqrt", "log", "abs"]
for NpWord in ReplcWord:
    var2_MaxInput = var2_MaxInput.replace(NpWord, f'np.{NpWord}')
    var2_MinInput = var2_MinInput.replace(NpWord, f'np.{NpWord}')
var2_MaxInput = var2_MaxInput.replace("arcnp.", "np.arc")
var2_MinInput = var2_MinInput.replace("arcnp.", "np.arc")

###################################################################################################################
# 행렬로 만들어 조작하기

var0_domain = np.linspace(var0_min_input(), var0_max_input(), NumDiv)
var1_max_domain = [var1_max_input(var0) for var0 in var0_domain]
var1_min_domain = [var1_min_input(var0) for var0 in var0_domain]

var0_Mtx = np.full((NumDiv,NumDiv), np.nan)
for i in range(NumDiv):
    var0_Mtx[i,:len(var0_domain)] = var0_domain

var1_per_var0 = []
for n in range(NumDiv):
    var1_Boundary = [var1_max_domain[n], var1_min_domain[n]]
    var1_per_var0.append(np.unique(np.linspace(min(var1_Boundary), max(var1_Boundary), NumDiv)))
var1_Mtx = np.full((NumDiv,NumDiv), np.nan)
for i, vpv in enumerate(var1_per_var0):
    var1_Mtx[:len(vpv), i] = vpv

var2_max = var2_max_input(var0_Mtx, var1_Mtx)
var2_min = var2_min_input(var0_Mtx, var1_Mtx)

###################################################################################################################
# 함수 그릴 때 필요한 변수

var2_max_Math = all_func[5].replace("**","^")
var2_min_Math = all_func[4].replace("**","^")
var1_max_Math = all_func[3].replace("**","^")
var1_min_Math = all_func[2].replace("**","^")

var1_max_sort, var1_min_sort = sorted(var1_max_domain), sorted(var1_min_domain)

box1 = {'boxstyle' : 'square', 'ec' : (1,0.36,0.28), 'fc' : (1,0.60,0.52)}
box2 = {'boxstyle' : 'square', 'ec' : (0.12,0.56,1), 'fc' : (0.36,0.8,1)}

###################################################################################################################
# 3차원 그래프

fig1, ax1 = plt.subplots(subplot_kw={'projection': '3d'})
ax1.plot_surface(var0_Mtx, var1_Mtx, var2_max, linewidth=0.1, color = 'tan', shade = eval(Pb["Shade"]))
ax1.plot_surface(var0_Mtx, var1_Mtx, var2_min, linewidth=0.1, color = 'tan', shade = eval(Pb["Shade"]))
if eval(Pb["contour"]):
    ax1.contourf(var0_Mtx, var1_Mtx, abs(var2_max-var2_min), offset = 0, cmap = "summer")
ax1.plot(var0_domain, var1_max_domain, color = 'tomato', linewidth = 3)
ax1.plot(var0_domain, var1_min_domain, color = 'dodgerblue', linewidth = 3)
ax1.view_init(40, -110)
ax1.set_xlabel(f'{var0}-Axis')
ax1.set_ylabel(f'{var1}-Axis')
ax1.set_zlabel(f'{var2}-Axis')
plt.title(f"3D Graph of Function ${var2}={var2_max_Math}$ & ${var2}={var2_min_Math}$", fontsize = 16)

###################################################################################################################
# 2차원 그래프

fig2, ax2 = plt.subplots()
ax2.plot(var0_domain, var1_max_domain, color = 'tomato')
ax2.plot(var0_domain, var1_min_domain, color = 'dodgerblue')
plt.fill_between(var0_domain, var1_max_domain, var1_min_domain, alpha=0.2, color = 'tan')
plt.text(var0_domain[5], var1_max_sort[-10],rf'${var1}={var1_max_Math}$', bbox = box1, color = 'black')
plt.text(var0_domain[10], var1_min_sort[10], rf'${var1}={var1_min_Math}$', bbox=box2, color='black')
ax2.set_xlabel(f'{var0}-Axis')
ax2.set_ylabel(f'{var1}-Axis')
ax2.set_title("Domain of Function")

###################################################################################################################

# 3차원 그래프 이미지를 BytesIO에 저장
img_data_3d = io.BytesIO()
fig1.savefig(img_data_3d, format='png')
img_data_3d.seek(0)

# Pillow Image를 Base64로 인코딩
img_base64_3d = base64.b64encode(img_data_3d.read()).decode('utf-8')

# 2차원 그래프 이미지를 BytesIO에 저장
img_data_2d = io.BytesIO()
fig2.savefig(img_data_2d, format='png')
img_data_2d.seek(0)

# Pillow Image를 Base64로 인코딩
img_base64_2d = base64.b64encode(img_data_2d.read()).decode('utf-8')

app = Flask(__name__)

@app.route('/그래프111')
def index():
    # Matplotlib로 그린 그래프를 이미지로 변환
    graph_image1, graph_image2 = img_data_3d, img_data_2d

    # 그래프 이미지를 웹페이지에 전달
    return render_template('index.html', graph_image1=graph_image1)

if __name__ == '__main__':
    app.run(debug=True)