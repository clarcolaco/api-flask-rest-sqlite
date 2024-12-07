# [Eng] api-flask-rest-sqllite
- Repository with CRUD for users using Flask API and Streamlit for frontend
## How to run
### Local
#### backend
create python env:
- cd app_users/backend
- pip install -r requirements.txt
- python3 main.py

#### frontend
- cd app_users/frontend
- pip install -r requirements.txt
- streamlit run main.py

### Local Docker
- cd app_users
- docker-compose up --build --no-deps

### Usando docker com imagem em nuvem
Create a file with docker-composer.yaml name
Copy and past:
```python
version: '3.8'
services:
  backend:
    image: clar1703/backend_flask_crud
    build:
      context: backend  
    ports: 
      - "5001:5001"
    networks:
      - app_network
    environment:
      - IS_DOCKER=true 

  frontend:
    image: clar1703/frontend_streamlit_crud
    build:
      context: frontend  
    ports:
      - "8501:8501"  
    networks:
      - app_network
    environment:
      - IS_DOCKER=true 

networks:
  app_network:
    driver: bridge
```

- then run - docker-compose up 

##############################################################################
# [Pt] api-flask-rest-sqllite
- Repositório com CRUD para usuários que usam Flask API e Streamlit para frontend
## Como testar:
### Local
#### backend
create python env:
- cd app_users/backend
- pip install -r requirements.txt
- python3 main.py

#### frontend
- cd app_users/frontend
- pip install -r requirements.txt
- streamlit run main.py

### Docker local
- cd app_users
- docker-compose up --build --no-deps

### Usando docker com imagem em nuvem
crie um arquivo docker-composer.yaml
cole isso:
```python
version: '3.8'
services:
  backend:
    image: clar1703/backend_flask_crud
    build:
      context: backend  
    ports: 
      - "5001:5001"
    networks:
      - app_network
    environment:
      - IS_DOCKER=true 

  frontend:
    image: clar1703/frontend_streamlit_crud
    build:
      context: frontend  
    ports:
      - "8501:8501"  
    networks:
      - app_network
    environment:
      - IS_DOCKER=true 

networks:
  app_network:
    driver: bridge
```

- e rode - docker-compose up 



@clarcolaco 2024
