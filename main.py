from dotenv import load_dotenv
from openai import OpenAI
import os

# Cargar API Key desde .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

# ---- 1) TRANSCRIPCIÓN ----
def transcribir(ruta_audio):
    with open(ruta_audio, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f
        )
    return transcript.text
    
# ---- 2) RESUMEN Y TAREAS ----
def generar_resumen(texto):
    prompt = f"""
    Transcripción de la reunión:

    {texto}

    Necesito:
    - Un resumen claro en 5 puntos.
    - Una lista de tareas accionables.
    - Formato tipo acta.

    Responde en Markdown.
    """

    resp = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content

# ---- EJECUCIÓN ----
def main():
    audio = r"C:\Users\pablo\Proyect\audio\audio.mp3"  

    print("🔊 Transcribiendo...")
    texto = transcribir(audio)

    print("📝 Generando resumen...")
    resumen = generar_resumen(texto)

    print("\n===== RESULTADO =====\n")
    print(resumen)

if __name__ == "__main__":
    main()