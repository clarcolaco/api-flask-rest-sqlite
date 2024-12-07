FROM python:3.9-slim
WORKDIR /backend
COPY . /backend
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "main.py"]