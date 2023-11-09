![image](https://github.com/SirRacha/AzureOpenAI-Langchain-Talk-with-CSV/assets/31993629/0ae4c709-ee39-4213-8956-76b8e044396f)


# AzureOpenAI Langchain Talk with a CSV (Tutorial)

The goal of this python app is to incorporate Azure OpenAI GPT4 with Langchain CSV and Pandas agents to allow a user to query the CSV and get answers in in text, linge graphs or bar charts.  It uses Streamlit as the UI.  Well, because everyone wants to see the LLM's at work!

## How it works

The application reads the CSV file and processes the data. It utilizes OpenAI LLMs alongside with Langchain Agents in order to answer your questions. The CSV agent then uses tools to find solutions to your questions and generates an appropriate response with the help of a LLM.

The application employs Streamlit to create the graphical user interface (GUI) and utilizes Langchain to interact with the LLM.

## Installation

To install the repository, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Additionally, you need to obtain an OpenAI API key and add it to the `.env` file.  A sample `.env` is provided.  Change the ending to have it work

## Usage

To use the application, execute the `Talk_with_CSV.py` file using the Streamlit CLI. Make sure you have Streamlit installed before running the application. Run the following command in your terminal:

```
streamlit run main.py
```

![CSV to graph](https://github.com/SirRacha/AzureOpenAI-Langchain-Talk-with-CSV/assets/31993629/64ec2cd5-a214-466d-b29e-34441900fe52)


## Contributing
This repository is intended for educational purposes only and is not designed to accept external contributions. It serves as supplemental material for the YouTube tutorial, demonstrating how to build the project.

For any suggestions or improvements related to the tutorial content, please feel free to reach out through the YouTube channel's comment section.

