import streamlit as st
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Librerías del Agente
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Agente SQL Biomédico", page_icon="🤖")

st.title("🤖 Chat con tu Base de Datos")
st.write("Pregunta sobre costos, técnicos, equipos y tickets sin escribir SQL.")

# --- CARGAR CREDENCIALES ---
load_dotenv()

# --- BARRA LATERAL (Estado de Conexión) ---
with st.sidebar:
    st.header("🔌 Estado del Sistema")
    if os.getenv("GROQ_API_KEY"):
        st.success("Cerebro IA (Groq): Conectado")
    else:
        st.error("Falta API Key de Groq")
        
    if os.getenv("DB_HOST"):
        st.success(f"Base de Datos: {os.getenv('DB_NAME')}")
    else:
        st.error("Falta configuración de BD")
    
    st.markdown("---")
    st.caption("Desarrollado por Víctor López")

# --- INICIALIZAR EL AGENTE (Solo una vez) ---
# Usamos @st.cache_resource para que no se reconecte en cada mensaje
@st.cache_resource
def get_agent():
    try:
        api_key = os.getenv("GROQ_API_KEY")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")

        # Conexión
        password_esc = quote_plus(db_password)
        uri = f"mysql+pymysql://{db_user}:{password_esc}@{db_host}/{db_name}"
        db = SQLDatabase.from_uri(uri)

        # LLM
        llm = ChatGroq(
            groq_api_key=api_key, 
            model="llama-3.3-70b-versatile", 
            temperature=0
        )

        # Toolkit y Agente
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="zero-shot-react-description",
            handle_parsing_errors=True
        )
        return agent
    except Exception as e:
        return None

agent = get_agent()

if not agent:
    st.error("Error crítico: No se pudo inicializar el agente. Revisa los logs.")
    st.stop()

# --- INTERFAZ DE CHAT ---

# 1. Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu analista virtual. ¿Qué quieres saber sobre la operación hoy?"}
    ]

# 2. Mostrar mensajes antiguos en cada recarga
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Capturar nueva pregunta del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta del asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 *Pensando y consultando la base de datos...*")
        
        try:
            # ¡AQUÍ OCURRE LA MAGIA!
            response = agent.invoke(prompt)
            respuesta_texto = response['output']
            
            message_placeholder.markdown(respuesta_texto)
            
            # Guardar respuesta en historial
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            message_placeholder.error(f"Ocurrió un error: {str(e)}")