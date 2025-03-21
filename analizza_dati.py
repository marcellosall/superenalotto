import pandas as pd

# Caricare i dati delle estrazioni
df = pd.read_csv("dati_superenalotto_corretto.csv", parse_dates=["Data"])

# Convertire i numeri in formato intero
colonne_numeri = ["Num1", "Num2", "Num3", "Num4", "Num5", "Num6", "Jolly", "SuperStar"]
df[colonne_numeri] = df[colonne_numeri].astype(int)

# Creare una lista con tutti i numeri da 1 a 90
tutti_i_numeri = list(range(1, 91))

# Calcolare il ritardo per ogni numero
ritardi = {}
ultima_estrazione = df["Data"].max()

for numero in tutti_i_numeri:
    # Trova l'ultima estrazione in cui è uscito il numero
    ultime_uscite = df[df[colonne_numeri].isin([numero]).any(axis=1)]
    
    if not ultime_uscite.empty:
        ultima_uscita = ultime_uscite["Data"].max()
        ritardo = (ultima_estrazione - ultima_uscita).days
    else:
        ritardo = (ultima_estrazione - df["Data"].min()).days  # Se il numero non è mai uscito
    
    ritardi[numero] = ritardo

# Creare DataFrame e salvare il file
df_ritardi = pd.DataFrame.from_dict(ritardi, orient="index", columns=["ritardo"])
df_ritardi.index.name = "Numero"
df_ritardi.to_csv("ritardo_numeri.csv")

print("✅ Ritardi calcolati e salvati in ritardo_numeri.csv!")
