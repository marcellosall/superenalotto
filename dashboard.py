import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configurazione generale della pagina
st.set_page_config(
    page_title="Generatore di Sistemi SuperEnalotto",
    layout="wide"
)

# Stili CSS per migliorare leggibilità anche su smartphone/tablet
st.markdown(
    """
    <style>
        html, body, .stApp {
            background-color: #121212 !important;
            color: #FFFFFF !important;
            font-size: 18px !important;
        }
        
        .title {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
        }
        
        .sub-title {
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            color: #00FF00;
        }

        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #00FF00;
            text-align: left;
        }

        .stButton > button {
            background-color: #008000 !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: #005700 !important;
        }
        
        .stSelectbox, .stMultiselect, .stRadio {
            background-color: #1E1E1E !important;
            border: 1px solid #008000 !important;
            color: #FFFFFF !important;
            font-size: 18px !important;
        }

        .warning {
            background-color: #FFD700;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Layout a due colonne
col1, col2 = st.columns([1, 3])

# 📌 Colonna sinistra - Impostazioni ben visibili
with col1:
    st.markdown("<h2 class='sidebar-title'>🔧 Impostazioni di generazione</h2>", unsafe_allow_html=True)

    num_sistemi = st.number_input("🔢 Quanti sistemi vuoi generare?", min_value=1, max_value=20, value=5, step=1)

    st.markdown("<h4>🎯 Scegli una strategia</h4>", unsafe_allow_html=True)
    strategia = st.radio(
        "",
        ["Frequenti", "Ritardatari", "Bilanciato"],
        horizontal=False
    )

    esclusi = st.multiselect("🚫 Escludi numeri (opzionale)", options=list(range(1, 91)))
    obbligatori = st.multiselect("✅ Numeri obbligatori (opzionale)", options=list(range(1, 91)))

    if st.button("🎲 Genera Sistemi"):
        sistemi = []
        for _ in range(num_sistemi):
            numeri = sorted(pd.Series(range(1, 91)).sample(6).tolist())
            jolly = pd.Series(range(1, 91)).sample(1).iloc[0]
            superstar = pd.Series(range(1, 91)).sample(1).iloc[0]
            sistemi.append(numeri + [jolly, superstar])

        df = pd.DataFrame(sistemi, columns=["Num1", "Num2", "Num3", "Num4", "Num5", "Num6", "Jolly", "SuperStar"])

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_csv = f"sistemi_generati/sistemi_superenalotto_{timestamp}.csv"
        os.makedirs("sistemi_generati", exist_ok=True)
        df.to_csv(file_csv, index=False)

        file_pdf = f"sistemi_generati/sistemi_superenalotto_{timestamp}.pdf"
        df.to_string(buf=open(file_pdf, "w"))

        st.session_state["sistemi_generati"] = df

        st.markdown(f"📂 [Scarica il CSV]({file_csv})", unsafe_allow_html=True)
        st.markdown(f"📄 [Scarica il PDF]({file_pdf})", unsafe_allow_html=True)

    if st.button("🗑️ Reset Storico"):
        os.system("rm -rf sistemi_generati/*")
        st.success("📂 Storico eliminato con successo!")

# 📌 Colonna destra - Risultati generati
with col2:
    st.markdown("<h1 class='title'>🎰 Generatore di Sistemi per il SuperEnalotto</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='sub-title'>📊 Analisi delle estrazioni generate</h3>", unsafe_allow_html=True)

    if "sistemi_generati" in st.session_state and not st.session_state["sistemi_generati"].empty:
        st.dataframe(st.session_state["sistemi_generati"])
    else:
        st.warning("⚠ Nessun sistema trovato. Genera almeno un sistema per visualizzarlo qui.")
