#SALMA MEKAOUI N131173645
import librosa
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import math
from numpy import array,argmin
import numpy as np



#ces deux variables je vais les declarer vide et les appeler a chaque fonction pour entrer 
#les audios d'une maniere global ils vont jouer le role d'une variable global
audio1=''
audio2=''

def AUDIO_SAISIE1():
    #dans cette etape et a l appel de la fonction on vas offre a l'utilisateur la possibilite de choisir un audio n importe quelle qui se trouve dans son ordinateur
    fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Choisir audio",filetypes=(("fichier Son",'*.wav'),("tout les fichiers","*.*")))
    label1.set("audio 1 importé avec succes")
    #le module librosa.load il vas lire l audio choisi et retourner un tableau d element de l audio avec le taux d echantionnage
    tableau, tauxEchantionnage = librosa.load(fln)
    #ici on vas transmettre au variable global les element de l'auodio pour les utiliser dans les autre fct
    global audio1
    audio1= librosa.feature.mfcc(tableau, tauxEchantionnage)

def AUDIO_SAISIE2():
    #dans cette etape et a l appel de la fonction on vas offre a l'utilisateur la possibilite de choisir un audio n importe quelle qui se trouve dans son ordinateur
    fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Choisir audio",filetypes=(("fichier Son",'*.wav'),("tout les fichiers","*.*")))
    label2.set("audio 2 importé avec succes")
    #le module librosa.load il vas lire l audio choisi et retourner un tableau d element de l audio avec le taux d echantionnage
    tableau, tauxEchantionnage = librosa.load(fln)
    #ici on vas transmettre au variable global les element de l'auodio pour les utiliser dans les autre fct
    global audio2
    #la mfcc fais le fenetrage
    audio2= librosa.feature.mfcc(tableau, tauxEchantionnage)

#dans cette etape vient l'importance des variables global en vas les utiliser dans notre fonction comme des parametres pour calculer la distance entre eux     
def DTW(audio1,audio2):
    #la taille des deux audio
    X, Y = len(audio1), len(audio2)
    
    #creation d'une matrice qui vas contenir les resultat a la direction de x audio 1 et selon la direction de y audio2
    resultat = np.zeros((X+1, Y+1))
    
    for i in range(X+1):
        for j in range(Y+1):
            resultat[i, j] = np.inf
    resultat[0, 0] = 0
   
    for i in range(1, X+1):
        for j in range(1, Y+1):
            A= abs(audio1[i-1,0] - audio2[j-1,0])
            resultatMIN = np.min([resultat[i-1, j], resultat[i, j-1], resultat[i-1, j-1]])
            #remplire les elements de la matrice resultante par le min entre une case et ces voisins 
            resultat[i, j] = A+resultatMIN
    C=CHEMIN(resultat)
    return resultat,C,resultat[-1, -1] / sum(resultat.shape)    


#fonction puor tracer chemin 
def CHEMIN(D):
    l, c = array(D.shape) - 2
    p, q = [l], [c]
    while ((l > 0) or (c > 0)):
        tb = argmin((D[l, c], D[l, c+1], D[l+1, c]))
        if (tb == 0):
            l -= 1
            c -= 1
        elif (tb == 1):
            l -= 1
        else: # (tb == 2):
            c -= 1
        p.insert(0, l)
        q.insert(0, c)
    return array(p), array(q)


#cette fonction il vas nous permettre de afficher la distance et de creer le graphe dans la deuxieme frame
def tracer():
    global audio1,audio2
    can=Figure(figsize = (4,4),dpi=70)
    M,path,distance=DTW(audio1,audio2)
    label3.set(distance)
    label4.set("La distance resultante avec la dtw")
    plot1=can.add_subplot(111)
    plot1.plot(path[0],path[1])
    canvas=FigureCanvasTkAgg(can,master =partition12)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar=NavigationToolbar2Tk(canvas, partition12)
    toolbar.update()
    canvas.get_tk_widget().pack()


def donothing():
    A=0


window=Tk()

#ici j'ai fait la partition de la fenetre en deux
partition11 = LabelFrame(window,text="les elements a comparer")
partition11.pack(side=LEFT,fill="both",expand="yes",padx=10,pady=10)

partition12 = LabelFrame(window,text="le resultat*graphe de dtw*")
partition12.pack(side=RIGHT,fill="both",expand="yes",padx=10,pady=10)


label1=StringVar();
label2=StringVar();
label3=StringVar()
label4=StringVar()

label1.set("selectionner un audio")
label2.set("selectionner un audio")

#les boutton pour importer les audios a comparer
boutton1=Button(partition11,text="le premier audio",command=AUDIO_SAISIE1)
boutton1.pack(side=tk.TOP)
text1=Label(partition11,textvariable=label1)
text1.pack()

btn2=Button(partition11,text="le deuxieme audio",command=AUDIO_SAISIE2)
btn2.pack(side=tk.TOP)
text2=Label(partition11,textvariable=label2)
text2.pack()

btn3=Button(partition11,text="traiter mes information",command=tracer)
btn3.pack()


#les resultats obtenue qui vont etre appliquer sur la deuxieme fenetre
text31=Label(partition12,textvariable=label4)
text31.pack()
text41=Label(partition12,textvariable=label3)
text41.pack()


window.title("comparaison avec DTW")
window.geometry("700x700")
window.resizable(False,False)
window.mainloop()










