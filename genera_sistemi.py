import os
import numpy as np
import pandas as pd
from datetime import datetime
from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Creazione directory per i file generati
DIR_SISTEMI = "sistemi_generati"
DIR_STATISTICHE = "statistiche"
os.makedirs(DIR_SISTEMI, exist_ok=True)
os.makedirs(DIR_STATISTICHE, exist_ok=True)

# Definizione numeri SuperEnalotto
NUMERI_TOTALI = set(range(1, 91))

# 📌 Funzione per validare numeri inseriti dall'utente
def valida_numeri(input_str):
    while True:
        try:
            if not input_str:
                return set()
            numeri = set(map(int, input_str.split(',')))
            if not numeri.issubset(NUMERI_TOTALI):
                raise ValueError
            return numeri
        except ValueError:
            input_str = input("❌ Errore: Inserisci solo numeri validi tra 1 e 90, separati da virgola: ")

# 📌 Funzione per calcolare statistiche sui numeri estratti
def calcola_statistiche():
    try:
        df = pd.read_csv("storico_estrazioni.csv")  # Deve esistere un file con le estrazioni storiche
        frequenze = df.iloc[:, :6].values.flatten()  # Prendi solo i primi 6 numeri delle estrazioni
        return Counter(frequenze)
    except FileNotFoundError:
        return Counter()

# 📌 Funzione per generare un singolo sistema con casualità controllata
def genera_sistema(numeri_disponibili, numeri_obbligatori, frequenze):
    numeri_rimanenti = list(numeri_disponibili - numeri_obbligatori)
    casuali_da_scegliere = 6 - len(numeri_obbligatori)

    # Ponderazione: i numeri con meno frequenze avranno più possibilità di essere scelti
    pesi = np.array([1 / (frequenze.get(num, 1) + 1) for num in numeri_rimanenti])
    pesi /= pesi.sum()  # Normalizza i pesi

    # Seleziona i numeri con probabilità pesata
    numeri_casuali = np.random.choice(numeri_rimanenti, casuali_da_scegliere, replace=False, p=pesi)
    
    sestina = sorted(numeri_obbligatori | set(numeri_casuali))
    jolly = np.random.choice(list(NUMERI_TOTALI - set(sestina)))
    superstar = np.random.choice(list(NUMERI_TOTALI - set(sestina) - {jolly}))

    return sestina, jolly, superstar

# 📌 Funzione per valutare il sistema generato
def valuta_sistema(sestina):
    pari = sum(1 for num in sestina if num % 2 == 0)
    dispari = 6 - pari
    alti = sum(1 for num in sestina if num > 45)
    bassi = 6 - alti
    consecutivi = sum(1 for i in range(5) if sestina[i] + 1 == sestina[i + 1])

    # Punteggio migliorato
    punteggio = 500 + (pari * 5) + (alti * 5) - (consecutivi * 10)

    return punteggio, pari, dispari, alti, bassi, consecutivi

# 📌 Funzione per generare sistemi
def genera_sistemi(num_sistemi, strategia, esclusi, obbligatori):
    esclusi = esclusi or set()
    obbligatori = obbligatori or set()
    numeri_disponibili = NUMERI_TOTALI - esclusi
    frequenze = calcola_statistiche()
    
    sistemi = []
    for _ in range(num_sistemi):
        sestina, jolly, superstar = genera_sistema(numeri_disponibili, obbligatori, frequenze)
        punteggio, pari, dispari, alti, bassi, consecutivi = valuta_sistema(sestina)

        sistemi.append({
            "Num1": sestina[0], "Num2": sestina[1], "Num3": sestina[2],
            "Num4": sestina[3], "Num5": sestina[4], "Num6": sestina[5],
            "Jolly": jolly, "SuperStar": superstar,
            "Pari": pari, "Dispari": dispari,
            "Alti": alti, "Bassi": bassi,
            "Consecutivi": consecutivi,
            "Punteggio": round(punteggio, 2),
            "Strategia": strategia
        })

    return sistemi

# 📌 Funzione per salvare i sistemi in CSV e PDF
def salva_sistemi(sistemi):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_csv = os.path.join(DIR_SISTEMI, f"sistemi_superenalotto_{timestamp}.csv")
    file_pdf = os.path.join(DIR_SISTEMI, f"sistemi_superenalotto_{timestamp}.pdf")

    df = pd.DataFrame(sistemi)
    df.to_csv(file_csv, index=False)

    c = canvas.Canvas(file_pdf, pagesize=letter)
    c.drawString(100, 750, "Sistemi SuperEnalotto")
    y = 730
    for sistema in sistemi:
        text = f"{sistema['Num1']}, {sistema['Num2']}, {sistema['Num3']}, {sistema['Num4']}, {sistema['Num5']}, {sistema['Num6']} - Jolly: {sistema['Jolly']} - SuperStar: {sistema['SuperStar']} - Punteggio: {sistema['Punteggio']}"
        c.drawString(100, y, text)
        y -= 20
    c.save()

    print(f"📂 CSV salvato in: {file_csv}")
    print(f"📂 PDF salvato in: {file_pdf}")

# 📌 Funzione principale
def main():
    num_sistemi = int(input("Quanti sistemi vuoi generare? "))
    strategia = input("Scegli una strategia (frequenti, ritardatari, bilanciato): ").lower()

    esclusi = None
    if input("Escludere numeri? (s/n) ").strip().lower() == 's':
        esclusi = valida_numeri(input("Inserisci i numeri da escludere: "))

    obbligatori = None
    if input("Inserire numeri obbligatori? (s/n) ").strip().lower() == 's':
        obbligatori = valida_numeri(input("Inserisci i numeri obbligatori: "))

    sistemi = genera_sistemi(num_sistemi, strategia, esclusi, obbligatori)
    salva_sistemi(sistemi)

if __name__ == "__main__":
    main()
