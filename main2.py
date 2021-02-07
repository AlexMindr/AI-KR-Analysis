import copy
import time
import stopit
import sys
import os
import argparse
from pathlib import Path
#nr la solutie in functie de lung drum

if len(sys.argv) > 1:
    timeout = int(sys.argv[1])
    print("Timeout este", timeout)
    nosol = int(sys.argv[2])
    print("Nr de sol este", nosol)
    fin = sys.argv[3]
    if os.path.exists(fin):
        # print ( os.path.basename(fin))
        listaFisiere = os.path.basename(fin)
    folout = sys.argv[4]
    if os.path.exists(folout):
        # print ( os.path.basename(fin))
        foldout = os.path.basename(folout)


else:
    timeout = int(input("Introduceti timeoutul:"))
    nosol = int(input("Introduceti nr de sol:"))
    listaFisiere = os.listdir("inputs")
    foldout="outputs"

if not os.path.exists("outputs"):
    os.mkdir("outputs")




listaFisiere = os.listdir(fin)
'''
for fisier in listaFisiere:
    print(fisier)
    print(type(foldout))
'''
for fisier in listaFisiere:
    euristicax = []
    euristicay = []
    euristicane = []

    numeFisierOutput=foldout+"/output1_"+fisier
    print(fisier, "--->", numeFisierOutput)
    fout=open(numeFisierOutput,"w")

    # informatii despre un nod din arborele de parcurgere (nu din graful initial)
    class NodParcurgere:

        # constructorul clasei
        def __init__(self, info, parinte, cost=0, h=0):
            self.info = info
            self.parinte = parinte  # parintele din arborele de parcurgere
            self.g = cost  # consider cost=1 pentru o mutare
            self.h = h
            self.f = self.g + self.h

        # drumul pana la nodul parametru
        def obtineDrum(self):
            l = [self];
            nod = self
            while nod.parinte is not None:
                l.insert(0, nod.parinte)
                nod = nod.parinte
            return l

        # drumul pana la
        def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
            l = self.obtineDrum()
            for nod in l:
                fout.write(str(nod))
            if afisCost:
                fout.write("\nCost: "+str(self.g)+'\n')
            if afisLung:
                fout.write("Lungime: "+ str(len(l))+'\n')
            return len(l)

        # verificam daca nodul curent contine alt nod in drumul sau
        def contineInDrum(self, infoNodNou):
            nodDrum = self
            while nodDrum is not None:
                if (infoNodNou == nodDrum.info):
                    return True
                nodDrum = nodDrum.parinte

            return False

        # reprezentarea informatiei din nod sub forma de lista
        def __repr__(self):
            sir = ""
            sir += str(self.info)
            return (sir)

        # afisarea in forma ceruta in cerinta, aliniere la baza, trebuie inmultit cu 4 spatii cand este gol, forma elementelor este simbol deschis ('(','[','/') valoare element, simbol inchis
        def __str__(self):
            sir = ""
            maxInalt = max([len(stiva) for stiva in self.info])
            for inalt in range(maxInalt, 0, -1):
                for stiva in self.info:
                    if len(stiva) < inalt:
                        sir += "    "
                    else:
                        sir += stiva[inalt - 1] + " "
                sir += "\n"
            sir += "-" * (2 * len(self.info) - 1)
            sir+="\n"
            return sir


    class Graph:  # graful problemei

        # constructorul grafului
        def __init__(self, nume_fisier):
            # obtinem stiva de inceput, conform fisierului de input, transformam elementele din forma fisier in forma de output ceruta
            def obtineStive(sir):
                stiveSiruri = sir.strip().split("\n")
                listaStive = [sirStiva.strip().split(",") if sirStiva != "#" else [] for sirStiva in stiveSiruri]

                stivaL = []

                for stiva in listaStive:
                    stiva2 = []
                    for el in stiva:
                        if ('cub' in el):
                            el = el.split('(')
                            el = el[1]
                            el = el[:len(el) - 1]
                            x = "".join(("[", el, "]"))
                            # print(x)
                            stiva2.append(x)
                        elif ('sfera' in el):
                            el = el.split('(')
                            el = el[1]
                            el = el[:len(el) - 1]
                            x = "".join(("(", el, ")"))
                            stiva2.append(x)
                        elif ('piramida' in el):
                            el = el.split('(')
                            el = el[1]
                            el = el[:len(el) - 1]
                            x = "".join(("/", el, '\\'))
                            stiva2.append(x)
                        else:
                            stiva2.append(el)
                    stivaL.append(stiva2)

                listaStive = copy.copy(stivaL)

                return listaStive

            # Deschidem fisierul, citim din el, aflam numarul de
            f = open(nume_fisier, 'r')

            continutFisier = f.read()
            # nonempty_lines = [line.strip("\n") for line in continutFisier]
            with open(nume_fisier) as f:
                lines = [line.rstrip() for line in f]
                LiniiFis = len(lines)
            f.close()
            # citim cate stive trebuie sa fie goale, din fisier

            for line in continutFisier:
                self.nrStiveDeEliberat = int(line)
                break

            siruriStari = continutFisier.split(str(self.nrStiveDeEliberat))
            # obtinem stivele din fisier, in formatul bun, in nodul de inceput al grafului
            self.start = obtineStive(siruriStari[1])
            # verificam daca informatia initiala este corecta, altfel exit()
            i = 1
            global initsol
            okFis = "DA"
            initsol= "NU"
            if lines.count('#') == self.nrStiveDeEliberat:
                fout.write("\nStarea initiala este solutie\n")
                initsol="DA"
                return
            for stiva in self.start:
                j = 0
                for el in stiva:
                    if (i == 1 or i == LiniiFis - 1):
                        if "(" in el:
                            okFis = "NU"
                    if (j != len(stiva) - 1):
                        if "/" in el:
                            okFis = "NU"
                    j += 1
                i += 1
            varv=0

            for stiva in self.start:
               if len(stiva)>1:
                if  '/' in stiva[len(stiva)-1] :
                    varv+=1
            if varv >0 :
               if varv+int(lines.count('#'))>=LiniiFis-1:
                fout.write("Fisier fara solutie")
                initsol="DA"
                return
            if (okFis == "NU"):
                print("Fisier incorect")
                initsol="DA"
                return

            print("Stare Initiala:", self.start)
            print("Trebuie eliberate", self.nrStiveDeEliberat, "stive")

        # functia de testare scop, daca numarul de stive de eliberat s-a indeplinit
        def testeaza_scop(self, nodCurent):
            test = []

            if nodCurent.info.count(test) >= self.nrStiveDeEliberat:
                return True;
            else:
                return False;

        # va genera succesorii sub forma de noduri in arborele de parcurgere
        # fiecare element va avea o conditie in functie de ce tip este, la fel si pentru cost
        def genereazaSuccesori(self, nodCurent, tip_euristica="euristica y"):
            listaSuccesori = []
            stive_c = nodCurent.info  # stivele din nodul curent
            nr_stive = len(stive_c)
            for idx in range(nr_stive):
                copie_interm = copy.deepcopy(stive_c)
                if len(copie_interm[idx]) == 0:
                    continue
                bloc = copie_interm[idx].pop()

                for j in range(nr_stive):
                    if idx == j:
                        continue
                    stive_n = copy.deepcopy(copie_interm)  # lista noua de stive
                    if ('[' in bloc):
                        if (len(stive_n[j]) > 0):
                            if ('/' not in stive_n[j][len(stive_n[j]) - 1]):
                                stive_n[j].append(bloc)
                            else:
                                continue
                        else:
                            stive_n[j].append(bloc)
                    elif ('(' in bloc):
                        if (j - 1 >= nr_stive and j + 1 <= nr_stive and '/' not in stive_n[j][len(stive_n[j]) - 1]):
                            auxidx = len(stive_n[j]) + 1
                            if (('[' in stive_n[j - 1][auxidx] or '(' in stive_n[j - 1][auxidx]) and (
                                    '[' in stive_n[j + 1][auxidx] or '(' in stive_n[j + 1][auxidx])):
                                stive_n[j].append(bloc)
                            else:
                                continue
                        else:
                            continue

                    elif ('/' in bloc):
                        if (len(stive_n[j]) > 0):
                            if '/' != stive_n[j][-1][0]:
                                stive_n[j].append(bloc)

                            else:
                                continue
                        else:
                            stive_n[j].append(bloc)

                    if ('[' in bloc):
                        costMutareBloc = 2
                    elif ('(' in bloc):
                        costMutareBloc = 3
                    else:
                        costMutareBloc = 1
                    nod_nou = NodParcurgere(stive_n, nodCurent, cost=nodCurent.g + costMutareBloc,
                                            h=self.calculeaza_h(stive_n, tip_euristica))
                    if not nodCurent.contineInDrum(stive_n):
                        listaSuccesori.append(nod_nou)

            return listaSuccesori

        # calculeaza inaltimea (cand este nevoie de ea, in functie de euristica selectata)
        def calculeaza_h(self, infoNod, tip_euristica="euristica y"):
            if tip_euristica == "euristica y":
                v = []
                for stiva in infoNod:
                    # calculez nr de elemente din cele mai mici k stive
                    cost = len(stiva)
                    v.append(cost)

                v.sort()
                euristica = 0
                for i in range(self.nrStiveDeEliberat):
                    euristica += v[i]
                euristicax.append(euristica)
                return int(euristica);

            elif tip_euristica == "euristica x":

                v = []
                for stiva in infoNod:
                    # calculez nr de elemente din cele mai mici k stive
                    cost = 0
                    for el in stiva:
                        if ('[' in el):
                            cost += 2
                        elif ('(' in el):
                            cost += 3
                        else:
                            cost += 1
                    v.append(cost)
                v.sort()
                euristica = 0
                for i in range(self.nrStiveDeEliberat):
                    euristica += v[i]
                euristicay.append(euristica)
                return euristica;

            elif tip_euristica == "euristica neadmisibila":
                v = []
                for stiva in infoNod:
                    # calculez nr de elemente din cele mai mici k stive
                    cost = len(stiva)
                    v.append(cost * 3)

                euristica = 0
                for i in range(self.nrStiveDeEliberat):
                    euristica += v[i]
                euristicane.append(euristica)
                return int(euristica);

        # reprezentarea informatiilor din graf
        def __repr__(self):
            sir = ""
            for (k, v) in self.__dict__.items():
                sir += "{} = {}\n".format(k, v)
            return (sir)


    @stopit.threading_timeoutable(default="intrat in timeout")
    def breadth_first(gr, nrSolutiiCautate):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = [NodParcurgere(gr.start, None)]
        t1 = time.time()

        nrnod = 0
        while len(c) > 0:
            # print("Coada actuala: " + str(c))
            # input()
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent):
                fout.write("\nSolutie:\n")

                nodCurent.afisDrum(afisCost=True, afisLung=True)
                t2 = time.time()
                fout.write("\na durat: "+ str(round((t2 - t1) * 1000))+ "ms")
                fout.write("\na generat:" + str(nrnod) + "noduri")
                fout.write("\n\n----------------\n\n")

                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent)
            nrnod += len(lSuccesori)
            c.extend(lSuccesori)


    @stopit.threading_timeoutable(default="intrat in timeout")
    def a_star(gr, nrSolutiiCautate, tip_euristica):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica=tip_euristica))]
        t1 = time.time()
        nrnod = 0
        while len(c) > 0:
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent):
                fout.write("\nSolutie:\n")
                nodCurent.afisDrum(afisCost=True, afisLung=True)
                t2 = time.time()
                fout.write("\na durat: " + str(round((t2 - t1) * 1000)) + "ms")
                fout.write("\na generat:" + str(nrnod) + "noduri")
                fout.write("\n----------------\n")

                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
            nrnod += len(lSuccesori)
            for s in lSuccesori:
                i = 0
                gasit_loc = False
                for i in range(len(c)):
                    # diferenta fata de UCS e ca ordonez dupa f
                    if c[i].f >= s.f:
                        gasit_loc = True
                        break;
                if gasit_loc:
                    c.insert(i, s)
                else:
                    c.append(s)


    @stopit.threading_timeoutable(default="intrat in timeout")
    def uniform_cost(gr, nrSolutiiCautate=1):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = [NodParcurgere(gr.start, None, 0, 0)]
        t1 = time.time()
        nrnod = 0
        while len(c) > 0:
            # print("Coada actuala: " + str(c))
            # input()
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent):
                fout.write("\nSolutie:\n")
                nodCurent.afisDrum(afisCost=True, afisLung=True)
                t2 = time.time()
                fout.write("\na durat: " + str(round((t2 - t1) * 1000)) + "ms")
                fout.write("\na generat:" + str(nrnod) + "noduri")
                fout.write("\n----------------\n")

                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent)
            nrnod += len(lSuccesori)
            for s in lSuccesori:
                i = 0
                gasit_loc = False
                for i in range(len(c)):
                    # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                    if c[i].g > s.g:
                        gasit_loc = True
                        break;
                if gasit_loc:
                    c.insert(i, s)
                else:
                    c.append(s)


    @stopit.threading_timeoutable(default="intrat in timeout")
    def greedy(gr, nrSolutiiCautate=1):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = [NodParcurgere(gr.start, None, 0, 0)]
        t1 = time.time()
        nrnod = 0
        while len(c) > 0:
            # print("Coada actuala: " + str(c))
            # input()
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent):
                fout.write("\nSolutie:\n")
                nodCurent.afisDrum(afisCost=True, afisLung=True)
                t2 = time.time()
                fout.write("\na durat: " + str(round((t2 - t1) * 1000)) + "ms")
                fout.write("\na generat:" + str(nrnod) + "noduri")
                fout.write("\n----------------\n")

                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent)
            nrnod += len(lSuccesori)
            for s in lSuccesori:
                i = 0
                gasit_loc = False
                for i in range(len(c)):
                    # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                    if c[i].h > s.h:
                        gasit_loc = True
                        break;
                if gasit_loc:
                    c.insert(i, s)
                else:
                    c.append(s)


    @stopit.threading_timeoutable(default="intrat in timeout")
    def depth_first(gr, nrSolutiiCautate=1):
        # vom simula o stiva prin relatia de parinte a nodului curent
        t1 = time.time()
        nrnod = 0
        df(NodParcurgere(gr.start, None, 0, 0), nrSolutiiCautate, t1, nrnod)



    def df(nodCurent, nrSolutiiCautate, t1, nrnod):
        if nrSolutiiCautate == 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
            return nrSolutiiCautate
        # print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))

        if gr.testeaza_scop(nodCurent):
            fout.write("\nSolutie:\n")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            t2 = time.time()
            fout.write("\na durat: " + str(round((t2 - t1) * 1000)) + "ms")
            fout.write("\na generat:" + str(nrnod) + "noduri")
            fout.write("\n----------------\n")

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return nrSolutiiCautate
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        nrnod += len(lSuccesori)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = df(sc, nrSolutiiCautate, t1, nrnod)
        return nrSolutiiCautate



    def dfi(nodCurent, adancime, nrSolutiiCautate, t1, nrnod):
        # print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))

        if adancime == 1 and gr.testeaza_scop(nodCurent):
            fout.write("\nSolutie:\n")

            nodCurent.afisDrum(afisCost=True, afisLung=True)
            t2 = time.time()
            fout.write("\na durat: " + str(round((t2 - t1) * 1000)) + "ms")
            fout.write("\na generat:" + str(nrnod) + "noduri")
            fout.write("\n----------------\n")

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return nrSolutiiCautate
        if adancime > 1:
            lSuccesori = gr.genereazaSuccesori(nodCurent)
            nrnod += len(lSuccesori)
            for sc in lSuccesori:
                if nrSolutiiCautate != 0:
                    nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate, t1, nrnod)
        return nrSolutiiCautate


    @stopit.threading_timeoutable(default="intrat in timeout")
    def depth_first_iterativ(gr, nrSolutiiCautate=1):
        # c = [NodParcurgere(gr.start, None)]

        # while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        # nodCurent = c.pop(0)
        t1 = time.time()
        nrnod = 0
        for i in range(1, 15):
            if nrSolutiiCautate == 0:
                return
            fout.write("\n**************\nAdancime maxima: "+ str(i)+'\n')
            nrSolutiiCautate = dfi(NodParcurgere(gr.start, None), i, nrSolutiiCautate, t1, nrnod)


    def Average(lst):
        return sum(lst) / len(lst)


    gr = Graph(fin+"/"+fisier)

    if initsol == "NU":
        fout.write("Solutii obtinute cu breadth first:\n")
        x=breadth_first(gr, nrSolutiiCautate=nosol, timeout=timeout)
        if x:
            print("bf: "+x)
            fout.write("bf: "+x)

        fout.write("\n\n##################\nSolutii obtinute cu UCS:\n")
        y=uniform_cost(gr, nrSolutiiCautate=nosol, timeout=timeout)
        if y:
            print("ucs: "+y)
            fout.write("ucs: "+y)

        fout.write("\n\n##################\nSolutii obtinute cu Greedy:\n")
        z=greedy(gr, nrSolutiiCautate=nosol, timeout=timeout)
        if z:
            print("greedy: "+z)
            fout.write("greedy: "+z)

        fout.write("\n\n##################\nSolutii obtinute cu depth first:\n")
        t=depth_first(gr, nrSolutiiCautate=nosol,timeout=timeout)
        if t:
            print("df: "+t)
            fout.write("df: "+t)

        fout.write("\n\n##################\nSolutii obtinute cu depth first iterativ:\n")
        xx=depth_first_iterativ(gr, nrSolutiiCautate=nosol,timeout=timeout)
        if xx:
            print("dfi: "+xx)
            fout.write("dfi: " + xx)

        fout.write("\n\n##################\nSolutii obtinute cu A*1:\n")
        aa1=a_star(gr, nrSolutiiCautate=nosol, tip_euristica="euristica y", timeout=timeout)
        if aa1:
            print("A* e1: "+aa1)
            fout.write("A* e1: " + aa1)

        fout.write("\n\n##################\nSolutii obtinute cu A*2:\n")
        aa2=a_star(gr, nrSolutiiCautate=nosol, tip_euristica="euristica x", timeout=timeout)
        if aa2:
            print("A* e2: "+aa2)
            fout.write("A* e2: " + aa2)
        fout.write("\n\n##################\nSolutii obtinute cu A*3:\n")
        aane = a_star(gr, nrSolutiiCautate=nosol, tip_euristica="euristica neadmisibila", timeout=timeout)
        if aane:
            print("A* eur neadm: " + aane)
            fout.write("A* eur neadm: " + aane)
        fout.close()
        print("eurx",Average(euristicax))
        print("eury",Average(euristicay))
        print("eurne",Average(euristicane))


