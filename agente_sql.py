import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Librerías de LangChain (El Orquestador)
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent


# 1. Cargar Variables de Entorno
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

if not api_key:
    print("❌ Error: Falta la GROQ_API_KEY en el archivo .env")
    exit()

# 2. Conectar a la Base de Datos (MySQL)
print("🔌 Conectando a la base de datos 'biomed_db'...")

# Escapamos la contraseña (por si tiene @)
password_esc = quote_plus(db_password)
uri = f"mysql+pymysql://{db_user}:{password_esc}@{db_host}/{db_name}"

# Creamos el objeto base de datos de LangChain
db = SQLDatabase.from_uri(uri)

print("✅ Conexión exitosa.")

# 3. Configurar el Cerebro (LLM)
# Usamos Llama 3 (versión 70B o 8B) a través de Groq. Es rapidísimo.
llm = ChatGroq(
    groq_api_key=api_key, 
    model="llama-3.3-70b-versatile",       # <--- ASÍ DEBE SER
    temperature=0
)

# 4. Crear el Kit de Herramientas (Toolkit)
# Esto le da al LLM "permiso" para ver las tablas y ejecutar SQL
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 5. Crear el Agente
# Este es el robot que recibe tu pregunta y decide qué SQL ejecutar
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True, # 'verbose=True' nos dejará ver qué está "pensando" el agente
    agent_type="zero-shot-react-description",
    handle_parsing_errors=True
)

# --- INTERACCIÓN ---
print("\n🤖 ¡Hola! Soy tu Agente de Datos Biomédicos.")
print("Puedo responder preguntas sobre técnicos, equipos, costos y tickets.")
print("Escribe 'salir' para terminar.\n")

while True:
    pregunta = input("❓ Haz tu pregunta: ")
    
    if pregunta.lower() in ["salir", "exit", "chau"]:
        print("👋 ¡Hasta luego!")
        break
    
    try:
        # Le pedimos al agente que "invoque" (ejecute) la respuesta
        respuesta = agent_executor.invoke(pregunta)
        
        # La respuesta viene en un diccionario, extraemos el texto final
        print(f"\n💡 Respuesta: {respuesta['output']}\n")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")