#!/usr/bin/env python
# coding: utf-8

# Frank Reyes.

import os, sys, csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""
(0, u'"Timestamp"')
(1, u'"\xbfEst\xe1s en Reddit?"')
(2, u'"\xbfEst\xe1s buscando trabajo?"')
(3, u'"\xbfTen\xe9s trabajo?"')
(4, u'"Carga horaria"')
(5, u'"Espacio/lugar de trabajo"')
(6, u'"Nivel de estudios"')
(7, u'"\xbfTrabaj\xe1s de lo que estudias(te)?"')
(8, u'"\xbfSector de trabajo?"')
(9, u'"\xbfDe qu\xe9 trabaj\xe1s?"')
(10, u'"\xbfD\xf3nde viv\xeds?"')
(11, u'"Edad"')
(12, u'"Comentarios"')
"""

"""
import csv,pprint
with open("encuesta.csv", 'rb') as csvfile:
    r = csv.reader(csvfile)
    L = dict([(x, {}) for x in [4, 5]])
    for line in r:
        for k in L:
            L[k][line[k]] = line[k]
    pprint.pprint(L)
"""

SHORTNAME = {
    4: {
         'Independiente (la cantidad de horas diarias es variable y/o las elijo yo)': 'Independiente',
         'Jornada completa (8+ horas por d\xc3\xada)': 'Jornada completa',
         'Media jornada (menos de 8 horas por d\xc3\xada pero fijo y peri\xc3\xb3dico)': 'Media jornada',
         'NO CORRESPONDE': 'NO CORRESPONDE'},
    5: {'Desde mi casa': 'Desde mi casa',
         'En la calle': 'En la calle',
         'En oficina, comercio, f\xc3\xa1brica, en un lugar fijo (que no sea donde viv\xc3\xads).': 'En oficina',
         'NO CORRESPONDE': 'NO CORRESPONDE'},
    6: {
        'Empec\xc3\xa9 la Universidad (Carrera de 5 a\xc3\xb1os)': 'Empec\xc3\xa9 Uni',
        'Empec\xc3\xa9 un Posgrado (Carrera de 5 a\xc3\xb1os + Posgrado de 2  a\xc3\xb1os)': 'Empec\xc3\xa9 Posgrado',
        'Empec\xc3\xa9 un Terciario (Carrera de 3 a\xc3\xb1os o menos)': 'Empec\xc3\xa9 Terciario',
        'No termin\xc3\xa9 el secundario': 'No secundario',
        'OTRO': 'OTRO',
        'Secundario completo': 'Secundario completo',
        'Termin\xc3\xa9 la Universidad (Carrera de 5 a\xc3\xb1os)': 'Termin\xc3\xa9 Uni',
        'Termin\xc3\xa9 un Posgrado (Carrera de 5 a\xc3\xb1os + Posgrado de 2  a\xc3\xb1os)': 'Termin\xc3\xa9 Posgrado',
        'Termin\xc3\xa9 un Terciario (Carrera de 3 a\xc3\xb1os o menos)': 'Termin\xc3\xa9 Terciario'
    }
}

column_names = None

def pie_plot(data, labels, title, file_name):
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']    
    colors2 = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]

    patches, texts, autotexts = plt.pie(data, autopct='%1.1f%%', labels=labels, colors=colors2, shadow=True, startangle=90)
    plt.axis('equal')
    # plt.legend(patches, labels, loc="best")
    # plt.tight_layout()
    plt.title(title, y = 1.07)

    plt.savefig(file_name)
    plt.cla()
    plt.clf()

def hist_plot(data, title, file_name):

    plt.hist(data, 50, facecolor='green', alpha=0.75, range=(1,99))
    plt.title(title, y = 1.07)
    plt.xlabel(title)
    plt.ylabel('Cantidad de respuestas')

    plt.savefig(file_name)
    plt.cla()
    plt.clf()

def build_plots(L, file_name_prefix, title_prefix):
    Q = dict([(x, {}) for x in [1,2,3,4,5,6,7,8,10]])
    H = dict([(x, []) for x in [11]])

    for line in L:
        for k in Q:
            Q[k][line[k]] = Q[k].get(line[k], 0) + 1

        for k in H:
            H[k].append(int(line[k]))

    for k in Q:
        Qitems = sorted(Q[k].items())

        if k in SHORTNAME:
            labels = [SHORTNAME[k][x[0]].decode('utf8') for x in Qitems]
        else:
            labels = [x[0].decode('utf8') for x in Qitems]

        pie_plot([x[1] for x in Qitems], labels, title_prefix + column_names[k].decode('utf8'), file_name_prefix + 'Q{}.png'.format(k))

    for k in H:
        hist_plot(H[k], title_prefix + column_names[k].decode('utf8'), file_name_prefix + 'H{}.png'.format(k))

def main():
    global column_names

    file_name = "encuesta.csv"

    L = []

    with open(file_name, 'rb') as csvfile:
        r = csv.reader(csvfile)
        for i, line in enumerate(r):
            if i > 0:
                L.append(line)
            else:
                column_names = line

    build_plots(L, "W0", "")

    build_plots([x for x in L if x[3] == "No"], "W1", "Personas sin trabajo: ")

    build_plots([x for x in L if x[3] != "No"], "W2", "Personas con trabajo: ")

    build_plots([x for x in L if x[2] != "No" and x[3] == "No"], "W3", "Personas buscando pero sin trabajo: ")

    build_plots([x for x in L if x[2] == "No" and x[3] != "No"], "W4", "Personas buscando pero con trabajo: ")

if __name__ == "__main__":
    main()
