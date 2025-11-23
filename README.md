# Agente de IA para Bases de Datos (Text-to-SQL) con Llama 3

Este proyecto implementa un **Agente de Inteligencia Artificial** capaz de interactuar con una base de datos MySQL utilizando lenguaje natural. El sistema permite a los usuarios hacer preguntas complejas de negocio (ej. "¿Quién es el técnico más costoso?") y obtener respuestas precisas en tiempo real, sin necesidad de escribir código SQL.

## 🧠 Arquitectura de la Solución

El agente actúa como un puente cognitivo entre el usuario y la base de datos:

1.  **Cerebro (LLM):** Utiliza el modelo **Llama 3** (vía **Groq**) para interpretar la intención del usuario y generar consultas SQL sintácticamente correctas.
2.  **Orquestador (LangChain):** Gestiona el flujo de pensamiento del agente, permitiéndole acceder al esquema de la base de datos, corregir errores y ejecutar consultas.
3.  **Memoria (MySQL):** Se conecta a una base de datos relacional (`biomed_db`) que contiene datos operativos de una empresa biomédica (Clientes, Técnicos, Tickets).

## 🛠️ Tecnologías Utilizadas

* **Python**
* **LangChain:** Framework para el desarrollo de aplicaciones con LLMs.
* **Groq API:** Inferencia de ultra-baja latencia para modelos Llama 3.
* **SQLAlchemy & PyMySQL:** Conectores de base de datos.
* **MySQL:** Motor de base de datos relacional.

## 📊 Capacidades Demostradas

* **Text-to-SQL:** Traducción de preguntas de negocio a consultas SQL complejas (JOINs, Agregaciones, Cálculos).
* **Razonamiento Matemático:** Capacidad para deducir fórmulas (ej. Costo Mano de Obra = Horas * Tarifa) basándose en el esquema.
* **Manejo de Errores:** El agente puede reintentar y corregir su propia query si la base de datos devuelve un error.

## 🚀 Cómo Ejecutar

1.  Clonar el repositorio.
2.  Instalar dependencias: `pip install -r requirements.txt`
3.  Configurar el archivo `.env` con:
    * `GROQ_API_KEY`
    * Credenciales de MySQL (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
4.  Ejecutar el agente:
    ```bash
    python agente_sql.py
    ```