import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="TaxiFareModel Front", layout="centered")

st.title("🚖 Estimation du prix d'une course de taxi")

# 1) Choix de la date et de l'heure
pickup_date = st.date_input("Date de prise en charge", value=datetime.today().date())
pickup_time = st.time_input("Heure de prise en charge", value=datetime.now().time())

# On formate en string ISO
pickup_datetime = datetime.combine(pickup_date, pickup_time).strftime("%Y-%m-%d %H:%M:%S")

# 2) Coordonnées
col1, col2 = st.columns(2)
with col1:
    pickup_lat  = st.number_input("Latitude de prise en charge",  -90.0, 90.0, 40.7614327,  format="%.6f")
    pickup_lon  = st.number_input("Longitude de prise en charge", -180.0, 180.0, -73.9798156, format="%.6f")
with col2:
    dropoff_lat = st.number_input("Latitude de dépose",            -90.0, 90.0, 40.6413111,  format="%.6f")
    dropoff_lon = st.number_input("Longitude de dépose",           -180.0, 180.0, -73.7803331, format="%.6f")

# 3) Nombre de passagers
passenger_count = st.slider("Nombre de passagers", 1, 6, 1)

# 4) Bouton d'estimation
if st.button("Estimer le prix"):
    # 4.1) Construire le payload
    payload = {
        "pickup_datetime":    pickup_datetime,
        "pickup_latitude":    pickup_lat,
        "pickup_longitude":   pickup_lon,
        "dropoff_latitude":   dropoff_lat,
        "dropoff_longitude":  dropoff_lon,
        "passenger_count":    passenger_count
    }

    # 4.2) Appel à l’API
    url = "https://taxifare.lewagon.ai/predict"  # ou ton URL locale
    try:
        res = requests.get(url, params=payload)
        res.raise_for_status()
        fare = res.json().get("fare")
        # 4.3) Affichage du résultat
        st.success(f"💰 Prix estimé : {fare:.2f} $")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur lors de l’appel à l’API : {e}")
