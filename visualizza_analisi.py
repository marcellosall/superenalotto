import pandas as pd
import matplotlib.pyplot as plt

# Carica i sistemi analizzati
sistemi = pd.read_csv("sistemi_analizzati.csv")

# Carica le statistiche dei numeri (frequenza e ritardi)
frequenze = pd.read_csv("frequenza_numeri.csv", index_col=0)
ritardi = pd.read_csv("ritardo_numeri.csv", index_col=0)

# 📊 Istogramma delle frequenze dei numeri nel dataset
plt.figure(figsize=(10, 5))
plt.bar(frequenze.index, frequenze["count"], alpha=0.7, color="blue", label="Frequenza")
plt.xlabel("Numero")
plt.ylabel("Frequenza")
plt.title("Frequenza dei numeri nel SuperEnalotto")
plt.legend()
plt.show()

# 📊 Istogramma dei ritardi dei numeri
plt.figure(figsize=(10, 5))
plt.bar(ritardi.index, ritardi["ritardo"], alpha=0.7, color="red", label="Ritardo")
plt.xlabel("Numero")
plt.ylabel("Ritardo")
plt.title("Ritardo dei numeri nel SuperEnalotto")
plt.legend()
plt.show()

# 📊 Analisi dei punteggi dei sistemi generati
plt.figure(figsize=(10, 5))
plt.hist(sistemi["Punteggio"], bins=10, color="green", alpha=0.7)
plt.xlabel("Punteggio")
plt.ylabel("Numero di Sistemi")
plt.title("Distribuzione dei punteggi dei sistemi generati")
plt.show()

# Mostra la tabella dei migliori sistemi generati
top_sistemi = sistemi.sort_values(by="Punteggio", ascending=False).head(10)
print("\n📊 Migliori Sistemi Generati:\n")
print(top_sistemi)
