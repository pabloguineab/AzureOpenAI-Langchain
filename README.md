

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

Make sure you have Docker installed. I am using WSL2 on Windows and the global instal for Docker worked fine.  Then start the Docker Daemon by opening the application.  Next check you Docker on in the linux terminal. 
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
