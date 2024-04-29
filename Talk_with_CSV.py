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
    "VTWEG": "Canal de distribución",
    "SPART": "Sector",
    "ADRNR": "Dirección",
    "ANRED": "Tratamiento",
    "AUFSD": "Bloqueo central de pedido para cliente",
    "BAHNE": "Estación de ferrocarril para envío por expreso",
    "BAHNS": "Estación de tren",
    "BBBNR": "International Location Number (parte 1)",
    "BBSNR": "Número de ubicación internacional (parte 2)",
    "BEGRU": "Grupo autorizaciones",
    "BRSCH": "Clave de ramo industrial",
    "BUBKZ": "Dígito de control para el Nº de empresa internacional",
    "DATLT": "Nº línea transmisión de datos",
    "ERDAT": "Fecha de creación del registro",
    "ERNAM": "Nombre del responsable que ha añadido el objeto",
    "EXABL": "Indicador: Existencia de puestos de descarga",
    "FAKSD": "Bloqueo central de factura para cliente",
    "FISKN": "Número de cta. del reg. maestro con domicilio fiscal",
    "KNAZK": "Calendario del cliente del tiempo de trabajo",
    "KNRZA": "Número de cuenta del pagador alternativo",
    "KONZS": "Clave de grupo",
    "KTOKD": "Grupo de ctas.deudor",
    "KUKLA": "Clasificación de clientes",
    "LAND1": "Clave de país/región",
    "LIFNR": "Número de cuenta del proveedor o acreedor",
    "LIFSD": "Bloqueo central de entrega para cliente",
    "LOCCO": "Coordenadas del lugar",
    "LOEVM": "Indicador de borrado central para registro maestro",
    "NAME1": "Nombre 1",
    "NAME2": "Nombre 2",
    "NAME3": "Nombre 3",
    "NAME4": "Nombre 4",
    "NIELS": "Distrito Nielsen",
    "ORT01": "Población",
    "ORT02": "Distrito",
    "PFACH": "Apartado",
    "PSTL2": "Código postal del apartado",
    "PSTLZ": "Código postal",
    "REGIO": "Región (Estado federal, Estado federado, provincia, condado)",
    "COUNC": "Código de condado",
    "CITYC": "Código de lugar",
    "RPMKR": "Mercado regional",
    "SORTL": "Campo de clasificación",
    "SPERR": "Bloqueo contabilización central",
    "SPRAS": "Clave de idioma",
    "STCD1": "Número de identificación fiscal 1",
    "STCD2": "Número de identificación fiscal suplementario",
    "STKZA": "Indicador: ¿Empresa colaboradora sujeta a recargo equival.?",
    "STKZU": "Sujeto a IVA",
    "STRAS": "Calle y nº",
    "TELBX": "Número de telebox",
    "TELF1": "1º número de teléfono",
    "TELF2": "Nº de teléfono 2",
    "TELFX": "Nº telefax",
    "TELTX": "Número de teletex",
    "TELX1": "Número de télex",
    "LZONE": "Zona de transporte donde se efectúan las entregas",
    "XCPDK": "Indicador: ¿Es cuenta pro diversos (CPD)?",
    "XZEMP": "Indicador: ¿Se permite un pagador alternativo en documento?",
    "VBUND": "Número de sociedad GL asociada",
    "ERNAM_KNVV": "Nombre del responsable que ha añadido el objeto",
    "ERDAT_KNVV": "Fecha de creación del registro",
    "BEGRU_KNVV": "Grupo de autorizaciones",
    "LOEVM_KNVV": "Petición de borrado para cliente (a nivel comercial)",
    "VERSG": "Grupo de estadísticas cliente",
    "AUFSD_KNVV": "Bloqueo de pedido para cliente (área de ventas)",
    "KALKS": "Clasificación cliente para determinar esquema de cálculo",
    "KDGRP": "Grupo de clientes",
    "BZIRK": "Zona de ventas",
    "KONDA": "Grupo de precios de cliente",
    "PLTYP": "Tipo de lista de precios",
    "AWAHR": "Probabilidad de pedido de posición",
    "INCO1": "Incoterms parte 1",
    "INCO2": "Incoterms, parte 2",
    "LIFSD_KNVV": "Bloqueo de entrega para cliente (nivel comercial)",
    "AUTLF": "¿Entrega completa definida para cada pedido de cliente?",
    "ANTLF": "Cantidad máxima de entregas parciales permitidas p/posición",
    "KZTLF": "Entrega parcial a nivel de posición",
    "KZAZU": "Indicador de agrupamiento de pedidos",
    "CHSPL": "Partición de lotes permitida",
    "LPRIO": "Prioridad de entrega",
    "EIKTO": "Nuestra cuenta con el cliente / proveedor",
    "VSBED": "Condición de expedición",
    "FAKSD_KNVV": "Bloqueo de factura para cliente (nivel comercial)",
    "MRNKZ": "Actualización manual de factura",
    "PERFK": "Fechas de facturación (identificación de calendario)",
    "PERRL": "Programa de lista de facturas (identificación de calendario)",
    "KVAKZ": "Indicador de presupuesto estimativo de costes (inactivo)",
    "KVAWT": "Límite de valor p.presupuesto estimativo de costes (inact.)",
    "WAERS": "Moneda",
    "KLABC": "Clasificación de clientes (Análisis ABC)",
    "KTGRD": "Grupo de imputación para este cliente",
    "ZTERM": "Clave de condiciones de pago",
    "VWERK": "Centro suministrador (propio o externo)",
    "VKGRP": "Grupo de vendedores",
    "VKBUR": "Oficina de ventas",
    "VSORT": "Propuesta de posiciones",
    "STCEG": "Número de identificación fiscal comunitario",
    "DEAR1": "Indicador: Competencia",
    "DEAR2": "Indicador: Interlocutor de ventas",
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

