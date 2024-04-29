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

#openai.chat.completions.create()

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

    # Run the prompt through the agent and capture the response.
    response = agent.run(prompt)

    # Return the response converted to a string.
    return str(response)

def decode_response(response: str) -> dict:
    """
    This function converts the string response from the model to a dictionary object.
    Handles cases where the response might include multiple JSON objects by parsing only the first one.
    """
    try:
        if response and isinstance(response, str):
            json_objects = response.split('\n')
            return json.loads(json_objects[0])
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        return {}


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
st.set_page_config(page_title="👨‍💻 Talk with your CSV", layout="wide")
st.title("👨‍💻 Talk with your CSV & Pandas dataframe!")
# Temperature and token slider
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.1
)

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV" , type="csv")

query = st.text_area("Send a Message")

if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file.
    agent = csv_tool(data)

    # Query the agent.
    response = ask_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_answer(decoded_response)
