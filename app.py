import streamlit as st
import openai
import base64

# 🌙 Streamlit dark-themed custom styles
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stApp {
        background-color: #1e1e1e;
    }
    .stTextInput > div > div > input {
        background-color: #2a2a2a;
        color: white;
    }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 🗝️ Load API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🖼️ App title
st.title("🖼️ Image + Text Q&A with GPT-4o")
st.markdown("#### Upload an image (left) and ask your question (right)")

# 🧱 Split layout into 2 columns
left_col, right_col = st.columns(2)

# 📁 Left column: File upload
with left_col:
    uploaded_file = st.file_uploader("📎 Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
        st.markdown("_Image encoded for GPT-4o processing_ ✅")
    else:
        base64_image = None

# 💬 Right column: Chat input + response
with right_col:
    user_prompt = st.text_input("💬 Ask your question about the image")

    if uploaded_file and user_prompt:
        with st.spinner("Generating answer with GPT-4o..."):
            response = openai.Chatcompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Answer only if it is available in the given images. If data is not available, reply: Not Founded."},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": user_prompt
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            st.markdown("### 📘 GPT-4o's Response:")
            st.write(response.choices[0].message.content)
    elif not uploaded_file:
        st.info("📎 Please upload an image to begin.")
