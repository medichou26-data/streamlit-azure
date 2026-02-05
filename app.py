import streamlit as st

st.title("🌟 Mon Application Streamlit sur Azure 🌟")
st.write("Bienvenue dans cette application simple déployée sur Azure App Service !")

# Interaction utilisateur
name = st.text_input("Quel est ton prénom ?")
if name:
    st.write(f"Salut {name}, heureux de te voir ici !")

# Exemple de calcul simple
number = st.number_input("Choisis un nombre", 0, 100)
st.write(f"Le carré de {number} est {number**2}")
