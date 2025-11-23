# Agente de IA para Bases de Datos (Text-to-SQL)

> **Nueva Versión v2.0:** Ahora incluye interfaz web (Streamlit) y soporte para Docker. 🐳

Este proyecto implementa un **Agente de Inteligencia Artificial** capaz de interactuar con una base de datos MySQL utilizando lenguaje natural. El sistema permite a los usuarios hacer preguntas complejas de negocio (ej. "¿Quién es el técnico más costoso?") y obtener respuestas precisas en tiempo real.

## 🧠 Arquitectura de la Solución

1.  **Cerebro (LLM):** Modelo **Llama 3** (vía **Groq**) para inferencia ultra-rápida.
2.  **Orquestador (LangChain):** Gestiona el razonamiento y la ejecución de SQL.
3.  **Interfaz (Streamlit):** Chat web interactivo con historial y configuración visual.
4.  **Memoria (MySQL):** Base de datos operativa con datos biomédicos.

## 🛠️ Tecnologías

* **Core:** Python, LangChain, SQL.
* **Modelos:** Groq API (Llama 3).
* **Frontend:** Streamlit.
* **Infraestructura:** Docker (Containerización).
* **Base de Datos:** MySQL, SQLAlchemy.

## 🚀 Cómo Ejecutar

Tienes dos formas de correr este proyecto:

### Opción A: Ejecución Local (Python)
1.  Clonar el repositorio.
2.  Instalar dependencias: `pip install -r requirements.txt`
3.  Configurar el archivo `.env` con tus credenciales.
4.  Ejecutar la aplicación web:
    ```bash
    streamlit run app.py
    ```

### Opción B: Ejecución con Docker (Recomendada)
Para un entorno aislado y reproducible:

1.  Construir la imagen:
    ```bash
    docker build -t agente-biomed .
    ```
2.  Correr el contenedor (conectado a la BD local):
    ```bash
    docker run -p 8501:8501 --env-file .env agente-biomed
    ```
3.  Abrir en el navegador: `http://localhost:8501`

---
**Desarrollado por Víctor López**