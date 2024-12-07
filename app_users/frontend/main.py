
import streamlit as st
import requests
import os


IS_DOCKER = os.getenv("IS_DOCKER", "false").lower() == "true"
API_URL = "http://backend:5001/users" if IS_DOCKER else "http://localhost:5001/users"


def add_user(name, email):
    response = requests.post(API_URL, json={"name": name, "email": email})
    if response.status_code == 200:
        st.success(f"Usuário {name} adicionado com sucesso!")
    elif response.status_code == 400:
        st.error(f"Falha no cadastro, email {email} ja esta associado a outro usuário")
    else:
        st.error("Erro ao adicionar usuário.")


def get_users():
    response = requests.get(API_URL)
    if response.status_code == 200:
        users_data = response.json()
        if users_data:
            return users_data
        else:
            return []
    else:
        st.error("Erro ao buscar usuários.")
        return []


def delete_user(user_id):
    response = requests.delete(f"{API_URL}/{user_id}")
    if response.status_code == 200:
        st.success(f"Usuário com ID {user_id} deletado com sucesso!")
    else:
        st.error(f"Erro ao deletar usuário com ID {user_id}.")



def update_user(user_id, name, email):
    if name and email:
        payload={"name": name, "email":email}
    elif name:
        payload={"name": name}
    if email:
        payload={"email":email}

    response = requests.put(f"{API_URL}/{user_id}",json=payload)
    if response.status_code == 200:
        st.success(f"Modificado com sucesso!")
    elif response.status_code == 400:
        st.error(f"Email ja utilizado em outro usuario")
    else:
        st.error("Erro ao modificar o usuário.")


st.set_page_config(
    page_title="Gerenciamento de Usuários - Cadastro",
    page_icon="🌟", 
)
st.title("🌟 Gerenciamento de Usuários")

with st.expander("Lista de Usuários", expanded=False):
    st.header("Usuários Cadastrados")

    if st.button("Mostrar Usuários"):
        users_data = get_users()
        if users_data:
            st.write("### Lista de Usuários:")
            for user in users_data:
                st.write(f"**{user['name']}** - {user['email']} (ID: {user['id']})")


with st.expander("Adicionar Novo Usuário", expanded=True):
    name = st.text_input("Nome do Usuário")
    email = st.text_input("E-mail do Usuário")

    if st.button("Adicionar Usuário"):
        if name and email:
            add_user(name, email)
        else:
            st.warning("Por favor, preencha ambos os campos.")

with st.expander("Deletar Usuário", expanded=False):
    user_id = st.text_input("ID do Usuário para Deletar")

    if user_id:
        users_data = get_users()  
        user = next((user for user in users_data if str(user['id']) == user_id), None)
        
        if user:

            st.write(f"**Nome**: {user['name']}")
            st.write(f"**E-mail**: {user['email']}")

            confirm_delete = st.button("Confirmar Exclusão")
            if confirm_delete:
                delete_user(str(user_id))
        else:
            st.warning("Usuário não encontrado com o ID informado.")
    else:
        st.warning("Digite o ID do usuário para deletar.")


with st.expander("Modificar Usuário", expanded=False):
    user_id = st.text_input("ID do Usuário para Modificar")

    if user_id:
        users_data = get_users()  
        user = next((user for user in users_data if str(user['id']) == user_id), None)
        
        if user:
            st.write(f"**Nome**: {user['name']}")
            st.write(f"**E-mail**: {user['email']}")
            
            name_input = st.text_input("Nome do Usuário Modificado")
            email_input = st.text_input("E-mail do Usuário Modificado")
            submit_update = st.button("Confirmar Edição")
            if submit_update:
                update_user(user_id=str(user_id), name=name_input, email=email_input)
        else:
            st.warning("Usuário não encontrado com o ID informado.")
    else:
        st.warning("Digite o ID do usuário para deletar.")


st.markdown("[By @clarcolaco - 2024](https://github.com/clarcolaco)")

st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)