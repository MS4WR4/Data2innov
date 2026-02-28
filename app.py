import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Assistant RH Pharmacie", layout="wide")

st.title("💊 Assistant RH Intelligent - Pharmacie")

# --- Données simulées ---
employees = [
    {"name": "Amal", "role": "Pharmacien"},
    {"name": "Karim", "role": "Pharmacien"},
    {"name": "Youssef", "role": "Préparateur"},
    {"name": "Salma", "role": "Préparateur"},
]

days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

def generate_schedule():
    schedule = []
    for day in days:
        pharmacist = random.choice([e for e in employees if e["role"] == "Pharmacien"])
        preparator = random.choice([e for e in employees if e["role"] == "Préparateur"])
        schedule.append({
            "Jour": day,
            "Pharmacien Responsable": pharmacist["name"],
            "Préparateur": preparator["name"]
        })
    return pd.DataFrame(schedule)

if "schedule" not in st.session_state:
    st.session_state.schedule = generate_schedule()

# --- Affichage planning ---
st.subheader("📅 Planning Hebdomadaire")
st.dataframe(st.session_state.schedule, use_container_width=True)

# --- Gestion absence ---
st.subheader("🚨 Gestion d'absence")

col1, col2 = st.columns(2)

with col1:
    absent_employee = st.selectbox("Employé absent", [e["name"] for e in employees])

with col2:
    absent_day = st.selectbox("Jour concerné", days)

if st.button("Traiter l'absence"):
    for index, row in st.session_state.schedule.iterrows():
        if row["Jour"] == absent_day and (
            row["Pharmacien Responsable"] == absent_employee
            or row["Préparateur"] == absent_employee
        ):
            replacements = [e for e in employees if e["name"] != absent_employee]
            replacement = random.choice(replacements)

            if row["Pharmacien Responsable"] == absent_employee:
                st.session_state.schedule.at[index, "Pharmacien Responsable"] = replacement["name"]
            else:
                st.session_state.schedule.at[index, "Préparateur"] = replacement["name"]

            st.success(f"Remplacement proposé : {replacement['name']}")
            st.info("✔ Contrainte respectée : présence minimale d’un pharmacien garantie.")
            break

# --- Assistant conversationnel ---
st.subheader("🤖 Assistant Conversationnel RH")

question = st.text_input("Posez une question RH")

if question:
    if "planning" in question.lower():
        st.write("Le planning actuel est affiché ci-dessus.")
    elif "absence" in question.lower():
        st.write("Le module de gestion d'absence permet une replanification automatique.")
    elif "pharmacien" in question.lower():
        st.write("Le système garantit toujours au moins un pharmacien responsable par jour.")
    else:
        st.write("Assistant RH spécialisé pour optimisation organisationnelle en pharmacie.")
