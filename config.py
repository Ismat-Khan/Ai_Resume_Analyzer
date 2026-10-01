import os
import streamlit as st


def get_groq_api_key() -> str:
    """Read the Groq API key from Streamlit Secrets or an environment variable."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to .streamlit/secrets.toml "
            "for local development or Streamlit Cloud Secrets for deployment."
        )

    return str(api_key).strip()
