import streamlit as st
from openai import OpenAI
import base64

# Get API key securely from Streamlit secrets or directly (not recommended for public apps)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # <- Make sure your secrets are set

st.title("🧠 Image Q&A using GPT-4o")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
user_prompt = st.text_input("💬 Ask a question about the image")

if uploaded_file and user_prompt:
    with st.spinner("Generating answer with GPT-4o..."):
        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Answer only based on the image. If not possible, say 'Data insufficient'."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

        st.markdown("### 🧠 GPT-4o Response:")
        st.write(response.choices[0].message.content)
