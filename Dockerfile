FROM python:3.10

RUN mkdir ./myapp
WORKDIR ./myapp

COPY Talk_with_CSV.py Talk_with_CSV.py
COPY .env .env
COPY .streamlit/config.toml .streamlit/config.toml
RUN pip install -U pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#CMD streamlit run Talk_with_CSV.py 
# Run
ENTRYPOINT ["streamlit", "run"]
 
CMD ["Talk_with_CSV.py","--theme.base","light"]