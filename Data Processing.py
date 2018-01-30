import pandas as pd

# ouverture des données
bookings = pd.read_csv("data_bookings_250118.csv", sep=";", index_col="Id")
schedule = pd.read_csv("data_schedule_250118.csv", sep=";", index_col="Aircraft")

# définition des caractéristiques des palettes
MDP_volume = 18
MDP_weight = 7870
LDP_volume = 10
LDP_weight = 5100
LDC_volume = 4.3
LDC_weight = 1587

# gestion des critères périssables et radioactives
bookings["Perishable"] = [int((bookings["Type"][i]=="PER")) for i in range(len(bookings))]
bookings["Radioactive"] = [int((bookings["Type"][i]=="RAD")) for i in range(len(bookings))]

# remplissage des données manquantes par 0
bookings = bookings.fillna(0)

# remplacement du volume de l'objet par le volume réservé
for c in range(len(bookings)):
    if bookings['MDP'][c] + bookings['LDP'][c] + bookings['LDC'][c] != 0.0:
        bookings['Volume'][c] = MDP_volume*bookings['MDP'][c] + LDP_volume*bookings['LDP'][c] + LDC_volume*bookings['LDC'][c]

# calcul du volume et poids totaux
schedule["Volume"] = MDP_volume*schedule["MDP (# palets available)"]+LDP_volume*schedule["LDP (# palets available)"]+LDC_volume*schedule["LDC (# palets available)"]+schedule["Bulk (volume available)"]
schedule["Weight"] = MDP_weight*schedule["MDP (# palets available)"]+LDP_weight*schedule["LDP (# palets available)"]+LDC_weight*schedule["LDC (# palets available)"]+schedule["Bulk (max weight)"]

# ECRITURE DES PARAMÈTRES DU PL

inp = open('input.dat','w')

inp.write("param cardN := "+str(len(bookings))+";\n")

inp.write("param cardV := "+str(len(schedule))+";\n")

inp.write("param cardK := 3;\n")

inp.write("param V := "+"\n")
for c in range(len(bookings)):
    inp.write(str(c+1)+" "+str(bookings["Volume"][c])+"\n")
inp.write(";\n")

inp.write("param W := "+"\n")
for c in range(len(bookings)):
    inp.write(str(c + 1) + " " + str(bookings["Weight"][c])+"\n")
inp.write(";\n")

inp.write("param V_max := "+"\n")
for c in range(len(schedule)):
    inp.write(str(c+1)+" "+str(schedule["Volume"][c])+"\n")
inp.write(";\n")

inp.write("param W_max := "+"\n")
for c in range(len(schedule)):
    inp.write(str(c+1)+" "+str(schedule["Weight"][c])+"\n")
inp.write(";\n")

inp.write("param p := "+"\n")
for c in range(len(bookings)):
    inp.write(str(c+1)+" "+str(bookings["Perishable"][c])+"\n")
inp.write(";\n")

inp.write("param r := "+"\n")
for c in range(len(bookings)):
    inp.write(str(c+1)+" "+str(bookings["Radioactive"][c])+"\n")
inp.write(";\n")

inp.write("param s := "+"\n")
for c in range(len(bookings)):
    inp.write(str(c+1)+" 1 "+str(bookings["MDP"][c])+"\n")
    inp.write(str(c+1) + " 2 " + str(bookings["LDP"][c]) + "\n")
    inp.write(str(c + 1) + " 3 " + str(bookings["LDC"][c]) + "\n")
inp.write(";\n")

inp.write("param S_max := "+"\n")
for c in range(len(schedule)):
    inp.write(str(c + 1) + " 1 " + str(schedule["MDP (# palets available)"][c]) + "\n")
    inp.write(str(c + 1) + " 2 " + str(schedule["LDP (# palets available)"][c]) + "\n")
    inp.write(str(c + 1) + " 3 " + str(schedule["LDC (# palets available)"][c]) + "\n")
inp.write(";\n")

inp.close()