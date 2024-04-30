from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import json
#from langchain.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
#import langchain_experimental.agents.create_csv_agent
from langchain.llms import OpenAI
from langchain.llms import AzureOpenAI
from langchain.agents.agent_types import AgentType
#from langchain.agents import AgentType
from langchain.chat_models.azure_openai import AzureChatOpenAI
#from langchain.tools.python.tool import PythonREPLTool 
#import matplotlib
#import openai
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv() 


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

#openai.chat.completions.create()
def json_tool(json_data):
    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        deployment_name=os.getenv("DEPLOYMENT_NAME"),
        openai_api_version="2023-09-01-preview", temperature=0)
    df = pd.DataFrame(json_data)

    # Renombrar las columnas usando el diccionario de datos
    df.rename(columns=diccionario_datos, inplace=True)

    return create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)


def csv_tool(filename : str):
   
    llm = AzureChatOpenAI(
                openai_api_key = os.getenv("OPENAI_API_KEY"),
                openai_api_base = os.getenv("OPENAI_API_BASE"),
                deployment_name=os.getenv("DEPLOYMENT_NAME"),
                openai_api_version="2023-09-01-preview", temperature=0)
    df = pd.read_csv(filename)

    return create_pandas_dataframe_agent(llm, df, verbose=True,agent_type=AgentType.OPENAI_FUNCTIONS)

#"2023-07-01-preview"  2023-03-15-preview  2023-09-01
def ask_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.
        agent: the tool name which should be "python_repl_ast"
        query = query.replace("```", "")

    Returns:
        The response from the agent as a string.
    """
    # Prepare the prompt with query guidelines and formatting
    prompt = (
        """
        Let's decode the way to respond to the queries. The responses depend on the type of information requested in the query. 

        1. If the query requires a table, format your answer like this:
           {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

        2. For a bar chart, respond like this:
           {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        3. If a line chart is more appropriate, your reply should look like this:
           {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        Note: We only accommodate two types of charts: "bar" and "line".

        4. For a plain question that doesn't need a chart or table, your response should be:
           {"answer": "Your answer goes here"}

        For example:
           {"answer": "The Product with the highest Orders is '15143Exfo'"}

        5. If the answer is not known or available, respond with:
           {"answer": "I do not know."}

        Return all output as a string. Remember to encase all strings in the "columns" list and data list in double quotes. 
        For example: {"columns": ["Products", "Orders"], "data": [["51993Masc", 191], ["49631Foun", 152]]}

        Now, let's tackle the query step by step. Here's the query for you to work on: 
        """
        + query
    )

    response = agent.run(query)
    return response

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    ### ADDED this loop to overcome the false Dictionaries load/loads creates!  ####
    if type(response) == str:
        return json.loads(response)
    else:
        return response


def write_answer(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        try:
            df_data = {
                    col: [x[i] if isinstance(x, list) else x for x in data['data']]
                    for i, col in enumerate(data['columns'])
                }       
            df = pd.DataFrame(df_data)
            #df.set_index("", inplace=True)
            st.bar_chart(df)
        except ValueError:
            print(f"Couldn't create DataFrame from data: {data}")

# Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        try:
            df_data = {col: [x[i] for x in data['data']] for i, col in enumerate(data['columns'])}
            df = pd.DataFrame(df_data)
            df.set_index("Products", inplace=True)
            st.line_chart(df)
        except ValueError:
            print(f"Couldn't create DataFrame from data: {data}")


    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

# Set the primary color to FFF700 and the base to dark
#st.set_theme({'primaryColor': '#FFF700', 'base': 'light'})
st.set_page_config(page_title="👨‍💻 Talk with your JSON Data", layout="wide")
st.title("👨‍💻 Talk with your JSON Data & Pandas DataFrame!")

st.write("Please upload your JSON file below.")
data = st.file_uploader("Upload a JSON", type=["json"])
query = st.text_area("Send a Message")

if st.button("Submit Query"):
    if data is not None:
        file_data = data.getvalue().decode('utf-8')
        json_data = json.loads(file_data)  # Convertir los datos del archivo a JSON
        agent = json_tool(json_data)
        response = ask_agent(agent=agent, query=query)
        decoded_response = decode_response(response)
        write_answer(decoded_response)
    else:
        st.error("Please upload a JSON file to continue.")
