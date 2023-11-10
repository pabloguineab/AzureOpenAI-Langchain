![image](https://github.com/SirRacha/AzureOpenAI-Langchain-Talk-with-CSV/assets/31993629/0ae4c709-ee39-4213-8956-76b8e044396f)



# AzureOpenAI + Langchain Agents! + Streamlit ==  *Talk with a CSV* App

The goal of this python app is to incorporate Azure OpenAI GPT4 with Langchain CSV and Pandas agents to allow a user to query the CSV and get answers in in text, linge graphs or bar charts.  It uses Streamlit as the UI.  Well, because everyone wants to see the LLM's at work!

## How it works

The app reads the CSV file and processes the data. It utilizes OpenAI LLMs alongside with Langchain Agents in order to answer your questions. The CSV agent then uses tools to find solutions to your questions and generates an appropriate response with the help of a LLM.

The app uses Streamlit to create the graphical user interface (GUI) and uses Langchain to interact with the LLM.

## Installation

To install the repository, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Additionally, you need to obtain an OpenAI API key and add it to the `.env` file.  A sample `.env` is provided.  Change the ending to have it work

## Run on Local

To use the application, execute the `Talk_with_CSV.py` file using the Streamlit CLI. Make sure you have Streamlit installed before running the application. Run the following command in your terminal:

```
streamlit run Talk_with_CSV.py

```

## Run Using Docker Container

Make sure you have Docker installed. I am using WSL2 on Windows and the global instal for Docker worked fine.  Then start the DOcker Daemon by opening the application.  Next check you Docker on in the linux terminal. 
```
docker images
```
You should see an output. That's a great start!  Next build the Docker container
```
docker build -t talktocsv:latest ./
```
That will take a few minutes to install and should be about 1.2GB. To run the container use either the image name or conatiner ID (which you can find in the output from the build or running hte images command).
```
docker run talktocsv:latest
```
Streamlit defaults to port 8501.  Always use the localhost:8501  url in the browser.  

## Contributing
This repository is intended for educational purposes only and is not designed to accept external contributions. For any suggestions or improvements related to the tutorial content, please feel free to reach out through the YouTube channel's comment section.



## Example of Streamlit app *in Dark Mode!* with a Bar Graph 


<img src="https://github.com/SirRacha/AzureOpenAI-Langchain-Talk-with-CSV/assets/31993629/64ec2cd5-a214-466d-b29e-34441900fe52" width="600" />


## TODO

- Add instructions for using Azure Container Registries and Azure webapps 



