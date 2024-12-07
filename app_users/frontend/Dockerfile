FROM python:3.9
WORKDIR /frontend
COPY . /frontend
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit","run", "main.py"]