import pandas as pd

# Caricamento dati
sistemi = pd.read_csv("sistemi_superenalotto.csv")
frequenza = pd.read_csv("frequenza_numeri.csv", index_col=0)
ritardo = pd.read_csv("ritardo_numeri.csv", index_col=0)

# Funzione per calcolare il punteggio di un sistema
def calcola_punteggio(sistema):
    numeri = sistema[:6]  # Seleziona solo i numeri principali (escludendo Jolly e SuperStar)

    # Punteggio frequenza: somma delle frequenze dei numeri selezionati
    punteggio_frequenza = frequenza.loc[numeri, "count"].sum()

    # Punteggio ritardo: somma dei ritardi dei numeri selezionati
    punteggio_ritardo = ritardo.loc[numeri, "ritardo"].sum()

    # Punteggio distribuzione: migliore se i numeri sono distribuiti su diverse decine
    decine = {num // 10 for num in numeri}
    punteggio_distribuzione = len(decine) * 10  # Più decine diverse, punteggio più alto

    # Controllo su numeri consecutivi
    numeri_ordinati = sorted(numeri)
    gruppi_consecutivi = sum(1 for i in range(len(numeri_ordinati) - 1) if numeri_ordinati[i] + 1 == numeri_ordinati[i + 1])
    penalizzazione_consecutivi = gruppi_consecutivi * 30  # Penalizza la presenza di troppi numeri consecutivi

    # Penalizzazione per troppe ripetizioni nella stessa decina
    penalizzazione_decine = (6 - len(decine)) * 20  # Se poche decine diverse, penalizza

    # Calcolo punteggio finale bilanciato
    punteggio_totale = (
        (punteggio_frequenza * 0.3) +  # Ridotto il peso della frequenza
        (punteggio_ritardo * 0.3) +    # Ridotto il peso del ritardo
        (punteggio_distribuzione * 0.4) -  # Aumentato peso della distribuzione
        penalizzazione_consecutivi -
        penalizzazione_decine
    )

    # Motivo del punteggio
    motivazione = []
    if penalizzazione_consecutivi > 0:
        motivazione.append(f"-{penalizzazione_consecutivi} pt (numeri consecutivi)")
    if penalizzazione_decine > 0:
        motivazione.append(f"-{penalizzazione_decine} pt (decine ripetute)")
    motivazione.append(f"+{punteggio_distribuzione} pt (distribuzione)")

    return max(punteggio_totale, 0), ", ".join(motivazione)

# Calcolo punteggio per ogni sistema
sistemi["Punteggio"], sistemi["Motivo Punteggio"] = zip(*sistemi.apply(calcola_punteggio, axis=1))

# Ordinamento sistemi per punteggio decrescente
sistemi = sistemi.sort_values(by="Punteggio", ascending=False)

# Salvataggio dei sistemi analizzati
sistemi.to_csv("sistemi_analizzati.csv", index=False)

print("\n✅ Analisi completata con spiegazione del punteggio! I sistemi sono stati salvati in 'sistemi_analizzati.csv'.")
print(sistemi)
