import streamlit as st
from config.confloader import load_config, get_db_config
import logging
from users import verify_user

st.title("ScoreCard Software")
st.write(
    "Bienvenido. Esta herramienta le ayudará a gestionar su inventario. "
)

# Cargar toda la configuración
try:
    env_settings = load_config()
    #print(f"Configuración cargada: {env_settings}")
except Exception as e:
    logging.error(f"Error al cargar la configuración: {e}")
    raise

# Obtener la configuración específica de PostgreSQL
db_config = get_db_config(env_settings)

def main():
    st.title("Sistema de Autenticación")
    st.subheader("Iniciar sesión")

    # Verificar si ya existe un estado de autenticación
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
        st.session_state["username"] = None

    if st.session_state["authentication_status"] is None:
        # Mostrar formulario de inicio de sesión
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        login_button = st.button("Iniciar sesión")

        if login_button:
            if verify_user(username, password):
                st.session_state["authentication_status"] = True
                st.session_state["username"] = username
                st.success("Inicio de sesión exitoso")
            else:
                st.session_state["authentication_status"] = False
                st.error("Usuario o contraseña incorrectos")
    elif st.session_state["authentication_status"]:
        # Mostrar contenido principal para usuarios autenticados
        st.write(f"Bienvenido, {st.session_state['username']}!")
        if st.button("Cerrar sesión"):
            st.session_state["authentication_status"] = None
            st.session_state["username"] = None
    else:
        st.error("Error de autenticación. Por favor, intenta nuevamente.")
