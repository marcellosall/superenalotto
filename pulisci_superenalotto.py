import pandas as pd

# Leggiamo il file cercando di individuare automaticamente il delimitatore
with open("dati_superenalotto.csv", "r", encoding="utf-8") as file:
    first_line = file.readline()
    print(f"🔍 Prima riga del file: {first_line}")

# Proviamo a rilevare il separatore automaticamente
df_superenalotto = pd.read_csv("dati_superenalotto.csv", sep=None, engine="python")

# Controlliamo se il file è stato letto con una sola colonna
if df_superenalotto.shape[1] == 1:
    print("⚠️ Il file è ancora in una sola colonna! Provo a correggere manualmente...")
    
    # Proviamo a separare i dati manualmente usando la virgola
    df_superenalotto = df_superenalotto.iloc[:, 0].str.split(",", expand=True)

# Rinominiamo le colonne correttamente
df_superenalotto.columns = ["Data", "Concorso", "Num1", "Num2", "Num3", "Num4", "Num5", "Num6", "Jolly", "SuperStar"]

# Convertiamo la colonna "Data" in formato datetime
df_superenalotto["Data"] = pd.to_datetime(df_superenalotto["Data"], errors="coerce")

# Convertiamo i numeri in formato numerico
colonne_numeriche = ["Concorso", "Num1", "Num2", "Num3", "Num4", "Num5", "Num6", "Jolly", "SuperStar"]
df_superenalotto[colonne_numeriche] = df_superenalotto[colonne_numeriche].apply(pd.to_numeric, errors="coerce", downcast="integer")

# Salviamo il file pulito
df_superenalotto.to_csv("dati_superenalotto_pulito.csv", index=False)

print("✅ File superenalotto pulito e salvato come 'dati_superenalotto_pulito.csv'.")
print(df_superenalotto.head())
