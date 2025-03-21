import pandas as pd

# 📌 Nome del file con i dati originali
file_path = "dati_superenalotto_pulito.csv"

# 📌 Nome del file in cui salveremo i dati corretti
output_path = "dati_superenalotto_corretto.csv"

# 📌 Caricamento dei dati
df = pd.read_csv(file_path)

# 🔹 Conversione dei numeri in interi
numeri_colonne = ["Num1", "Num2", "Num3", "Num4", "Num5", "Num6", "Jolly", "SuperStar"]
df[numeri_colonne] = df[numeri_colonne].apply(pd.to_numeric, errors="coerce").astype("Int64")

# 🔹 Conversione della colonna Data in formato data
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

# 🔍 Controlliamo se ci sono errori dopo la conversione
print("\n📊 Controllo dati dopo la conversione:")
print(df.dtypes)

# ❌ Controlliamo se ci sono valori mancanti
print("\n📊 Valori mancanti dopo la conversione:")
print(df.isnull().sum())

# 💾 Salviamo il dataset corretto
df.to_csv(output_path, index=False)
print(f"\n✅ Dati corretti e salvati in {output_path}!")
