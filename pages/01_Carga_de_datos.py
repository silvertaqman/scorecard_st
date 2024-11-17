# Importar las bibliotecas necesarias
import streamlit as st
from utils.do_df import check_dataframe_columns, check_extension, get_styled_dataframe, get_transformed_dataframe, download_dataframe
import data.db as db
from config.confloader import load_config, get_db_config
import logging

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
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
        # Título de la página
        st.title("Base de datos :card_file_box:")

        # Permite al usuario cargar un archivo
        uploaded_data = st.file_uploader(label="", label_visibility='collapsed')

        if uploaded_data:
            # Verifica la extensión del archivo y las columnas del DataFrame
            check_extension(uploaded_data)
            check_dataframe_columns(uploaded_data)
            
            # Sube el archivo a la base de datos
            with st.spinner('Subiendo archivo a la base de datos'):
                db.create_drive(".", uploaded_data)
            st.toast('Archivo subido correctamente!', icon='✔️')

        # Obtiene la respuesta (archivo Excel) desde la base de datos
        response = db.get_drive(".")

        # si se va a cargar un archivo por primera vez se muestra en la interfaz un mensaje
        if response is None:
            st.info("Por favor, carga un archivo Excel utilizando el botón de arriba.")
            st.stop()  
        st.session_state["data_ready"] = True
        # Crea dos pestañas para mostrar el contenido y permitir la exportación
        tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
        with tab_1:
            # Carga el DataFrame transformado 
            df_transformed = get_transformed_dataframe(response)
            
            # Dataframe para mostrar en la interdaz, solo las 100 primeras filas
            df_transformed = df_transformed.head(100)

            # Aplica estilos al DataFrame transformado 
            df_styled = get_styled_dataframe(df_transformed)
            
            # Muestra el DataFrame con estilos en la aplicación Streamlit, ocultando el índice
            st.dataframe(df_styled, hide_index=True)
        with tab_2:
            # Permite la descarga del DataFrame en formatos CSV y Excel
            download_dataframe(df_transformed, name="base_de_datos")

if __name__ == '__main__':
    main()
