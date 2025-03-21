import pandas as pd

# 📌 Caricamento del dataset
file_path = "dati_superenalotto_pulito.csv"  # Assicurati che il file esista
df = pd.read_csv(file_path)

# 📊 Verifica delle prime righe
print("✅ Dati caricati con successo!\n")
print("📊 Prime righe del dataset:")
print(df.head())

# 📊 Controllo informazioni sulle colonne
print("\n📊 Informazioni sulle colonne:")
print(df.info())

# 📊 Controllo valori mancanti prima della conversione
print("\n📊 Valori mancanti prima della conversione:")
print(df.isnull().sum())

# 📌 Conversione tipi di dati
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")  # Convertiamo la data

# 🔍 Conversione di Jolly e SuperStar, rimuovendo valori non numerici
df["Jolly"] = pd.to_numeric(df["Jolly"], errors="coerce").astype("Int64")
df["SuperStar"] = pd.to_numeric(df["SuperStar"], errors="coerce").astype("Int64")

# 📌 Conversione delle colonne dei numeri estratti
cols_numeri = ["Num1", "Num2", "Num3", "Num4", "Num5", "Num6"]
df[cols_numeri] = df[cols_numeri].apply(pd.to_numeric, errors="coerce").astype("Int64")

# 📊 Controllo dati dopo la conversione
print("\n📊 Controllo dati dopo la conversione:")
print(df.dtypes)

# 📊 Controllo valori mancanti dopo la conversione
print("\n📊 Valori mancanti dopo la conversione:")
print(df.isnull().sum())

# 📌 Riempimento valori mancanti
df["Data"] = df["Data"].ffill()  # Metodo alternativo senza warning
df["Jolly"] = df["Jolly"].fillna(df["Jolly"].mode()[0])  # Riempie i valori mancanti con la moda
df["SuperStar"] = df["SuperStar"].fillna(df["SuperStar"].mode()[0])  # Riempie i valori mancanti con la moda

# 📊 Controllo finale per assicurarsi che non ci siano più valori mancanti
print("\n📊 Valori mancanti dopo la correzione:")
print(df.isnull().sum())

# 📌 Salvataggio del dataset corretto
df.to_csv("dati_superenalotto_corretto.csv", index=False)
print("\n✅ Dati corretti e salvati in dati_superenalotto_corretto.csv!")
