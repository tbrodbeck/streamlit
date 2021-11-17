# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

COPY requirements.txt ./requirements.txt

COPY top5.csv ./top5.csv

RUN pip install -r requirements.txt

EXPOSE 8501

COPY . .

ENTRYPOINT ["streamlit", "run"]

CMD ["app_st.py"]
