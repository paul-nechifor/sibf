#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# This code is so bad, I should be shot.

import xml.dom.minidom, os

inceput = [
    '<!DOCTYPE html>',
    '<html lang="ro">',
    '<head>',
    '<meta charset="utf-8"/>',
    "<meta name='viewport' content='width=device-width, initial-scale=1, minimum-scale=0.25'/>",
    '<title>%s</title>',
    '<link rel="stylesheet" href="includes/style.css"/>',
    '</head>',
    '<body>'
]
sfarsit = "</body></html>"
inceput = "".join(inceput)

date = {}

def handleCarte(carte):
    info = carte.getElementsByTagName("info")[0]

    date["carte"] = carte
    date["tip"] = info.getAttribute("tip")
    date["titlu"] = info.getAttribute("titlu")
    date["autor"] = info.getAttribute("autor")
    date["cod"] = info.getAttribute("cod")

    os.system("rm -fr " + date["cod"])
    os.mkdir(date["cod"])

    handlePrimaPagina()
    el = carte.getElementsByTagName("capitol")
    for i, capitol in enumerate(el):
        care = "altul"
        if i == 0:
            care = "primul"
        if i == len(el) - 1:
            care = "ultimul"
        handleCapitol(i, capitol, care)

    os.system("cp -r includes %s" % date["cod"])

def handleCapitol(i, capitol, care):
    p = open("%s/%d.html" % (date["cod"], i + 1), "w")
    p.write((inceput % (date["titlu"] + ": " + capitol.getAttribute("titlu"))).encode('utf-8'))
    p.write('<div id="info">')
    p.write(('<h3><span class="titlu">%s</span> <span class="de">de</span> <span class="autor">%s</span></h3>' % (date['titlu'], date['autor'])).encode('utf-8'))
    p.write('</div>')
    p.write('<div id="continut">')
    if date["pentruCap"][i] != '':
        p.write(('<h2 class="titluparte">%s</h2>' % date["pentruCap"][i]).encode('utf-8'))
    p.write(("<h2>%s</h2>" % capitol.getAttribute("titlu")).encode('utf-8'))

    p.write("<".join(">".join(capitol.toxml().split(">")[1:]).split("<")[:-1]).encode('utf-8'))
    p.write('</div>')
    p.write('<div id="navigare">')
    p.write('<ul>')

    if care == "primul":
        p.write('<li class="inapoi"><span class="fara">Înapoi</span></li>')
    else:
        p.write('<li class="inapoi"><a href="%d.html">Înapoi</a></li>' % (i))

    p.write('<li class="cuprins"><a href="index.html">Cuprins</a></li>')

    if care == "ultimul":
        p.write('<li class="inainte"><span class="fara">Înainte</span></li>')
    else:
        p.write('<li class="inainte"><a href="%d.html">Înainte</a></li>' % (i + 2))

    p.write('</ul>')
    p.write('</div>')

    p.write(sfarsit)
    p.close()

def handlePrimaPagina():
    p = open("%s/index.html" % date["cod"], "w")
 
    p.write((inceput % (date["titlu"] + " de " + date["autor"])).encode('utf-8'))
    p.write('<div id="chenartitlu">')
    p.write(('<h1>%s</h1>' % date["titlu"]).encode('utf-8'))
    p.write('<h3 id="de">de</h3>')
    p.write(('<h2 id="autor">%s</h2>' % date["autor"]).encode('utf-8'))
    p.write('</div>')
    p.write('<h2>Cuprins</h2>')

    date["pentruCap"] = []

    if date["tip"] == "capitole":
        titluri = []
        for cap in date["carte"].getElementsByTagName("capitol"):
            titlu = cap.getAttribute("titlu")
            titluri.append(titlu)
        p.write('<ol>')
        for i, titlu in enumerate(titluri):
            p.write('<li><a href="%d.html">%s</a></li>' % (i + 1, titlu.encode('utf-8')))
            date["pentruCap"].append('')
        p.write('</ol>')

    elif date["tip"] == "parti":
        parti = []
        for par in date["carte"].getElementsByTagName("parte"):
            titluParte = par.getAttribute("titlu")
            titluri = []
            for cap in par.getElementsByTagName("capitol"):
                titlu = cap.getAttribute("titlu")
                titluri.append(titlu)
            parti.append((titluParte, titluri))

        i = 0
        for numeParte, titluri in parti:
            p.write(('<h3 class="titluparte">%s</h3>' % numeParte).encode('utf-8'))
            p.write('<ol>')
            date["pentruCap"].append(numeParte)
            for titlu in titluri:
                p.write('<li><a href="%d.html">%s</a></li>' % (i + 1, titlu.encode('utf-8')))
                date["pentruCap"].append('')
                i += 1
            date["pentruCap"].pop()
            p.write('</ol>')

    else:
        print "Nu am"
        exit()

    pref = date['carte'].getElementsByTagName('prefata')
    if len(pref) > 0:
        pref = pref[0]
        pref = pref.toxml()[len('<prefata>'):-len('</prefata>')]
        pref = '<div class="prefata">' + pref + '</div>'
        p.write(pref.encode('utf-8'))

    p.write(sfarsit)

    p.close()

dom = xml.dom.minidom.parse("../books/povesti.xml")
handleCarte(dom)

dom = xml.dom.minidom.parse("../books/moara.xml")
handleCarte(dom)

dom = xml.dom.minidom.parse("../books/morometii.xml")
handleCarte(dom)
