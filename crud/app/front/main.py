import streamlit as st
import requests


API_URL = 'http://localhost:5001/users'


def add_user(name, email):
    response = requests.post(API_URL, json={"name": name, "email": email})
    if response.status_code == 201:
        st.success(f"Usuário {name} adicionado com sucesso!")
    else:
        st.error("Erro ao adicionar usuário.")


def get_users():
    response = requests.get(API_URL)
    if response.status_code == 200:
        users_data = response.json()
        if users_data:
            st.write("### Lista de Usuários:")
            for user in users_data:
                st.write(f"**{user['name']}** - {user['email']}")
        else:
            st.write("Nenhum usuário encontrado.")
    else:
        st.error("Erro ao buscar usuários.")


st.title("Gerenciamento de Usuários")


st.header("Usuários Cadastrados")

if st.button("Mostrar Usuários"):
    get_users()


with st.expander("Adicionar Novo Usuário", expanded=False):
    name = st.text_input("Nome do Usuário")
    email = st.text_input("E-mail do Usuário")

    if st.button("Adicionar Usuário"):
        if name and email:
            add_user(name, email)
        else:
            st.warning("Por favor, preencha ambos os campos.")

# Estilização
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
