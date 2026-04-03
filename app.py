import streamlit as st
import fal_client
import os
import base64

# --- APP INTERFACE ---
st.set_page_config(page_title="Joseph's Design Partner", layout="centered")
st.title("Architectural AI Partner")
st.markdown("Upload a SketchUp massing to generate a signature render.")

# 1. Inputs
api_key = st.text_input("Enter Fal.ai API Key:", type="password")
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# 2. PROMPT: Notice we added "JosephStyle" at the start
prompt = st.text_area("Design Style:", value="JosephStyle modern tropical architecture, dusk lighting, warm wood and concrete, hyperrealistic")

# --- THE ENGINE ---
if st.button("Generate Signature Proposal"):
    if not api_key:
        st.warning("Please enter your API key.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("Applying your signature style... Rendering in the cloud.")
        os.environ["FAL_KEY"] = api_key
        
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # INTEGRATING YOUR LORA HERE
            result = fal_client.subscribe(
                "fal-ai/flux-lora-canny",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                    "loras": [
                        {
                            "path": "https://v3b.fal.media/files/b/0a94bf17/4SJKv1NIWG5OC7FNP5p_q_pytorch_lora_weights.safetensors",
                            "scale": 1.0
                        }
                    ]
                }
            )
            
            if 'image' in result:
                st.success("Your Signature Design is Ready!")
                st.image(result['image']['url'])
            
        except Exception as e:
            st.error(f"Engine Error: {e}")
