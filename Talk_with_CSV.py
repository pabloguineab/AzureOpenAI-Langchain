import streamlit as st
import pandas as pd
import json
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.llms import AzureChatOpenAI
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os

# Carga las variables de entorno
load_dotenv()

# Diccionario completo de datos
diccionario_datos = {
    "MANDT": "Mandante",
    "KUNNR": "Número de cliente",
    "VKORG": "Organización de ventas",
    # ...incluye aquí todos los campos que proporcionaste...
}

# Convertir el diccionario en un DataFrame de pandas para su uso
df_diccionario = pd.DataFrame(list(diccionario_datos.items()), columns=['Campo', 'Descripcion'])

# Función para crear el agente de LLM
def create_agent(df):
    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        deployment_name=os.getenv("DEPLOYMENT_NAME"),
        openai_api_version="2023-09-01-preview",
        temperature=0
    )
    return create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)

# Función para consultar al agente
def ask_agent(agent, query):
    # Suponemos que la función agent.run() está definida y puede manejar las consultas
    response = agent.run(query)
    return response

# Configuración de la página de Streamlit
st.set_page_config(page_title="Consulta de Datos", layout="wide")
st.title("Consulta de Datos Basada en JSON y Diccionario Integrado")

# Subida de archivo JSON
uploaded_json = st.file_uploader("Subir archivo JSON con detalles adicionales", type="json")

# Entrada de consulta
query = st.text_area("Ingresa tu pregunta")

if st.button("Consultar"):
    if uploaded_json:
        # Cargar datos JSON
        details = json.loads(uploaded_json.getvalue().decode("utf-8"))
        
        # Combina los detalles del JSON con el DataFrame del diccionario si es necesario
        # Por ejemplo, si quieres agregar información adicional al DataFrame

        # Crear el agente con el DataFrame que incluye el diccionario de datos
        agent = create_agent(df_diccionario)
        
        # Realizar la consulta al agente
        response = ask_agent(agent, query)
        
        # Mostrar respuesta
        st.write("Respuesta:", response)
    else:
        st.error("Por favor, sube un archivo JSON para proceder con la consulta.")

