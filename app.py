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
prompt = st.text_area("Design Style:", value="JosephStyle modern tropical residential at dusk. Maintain strict architectural fidelity to the uploaded 3D massing. Render with hyper-realistic concrete textures and warm timber accents.")

# --- THE ENGINE ---
if st.button("Generate Signature Proposal"):
    if not api_key:
        st.warning("Please enter your API key.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("Applying JosephStyle... This usually takes 2-4 minutes for high-quality Flux renders. Please don't refresh.")
        os.environ["FAL_KEY"] = api_key
        
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # We use 'subscribe' but with an explicit check
            # This 'logs=True' helps keep the connection alive
            handler = fal_client.submit(
                "fal-ai/flux-lora-canny",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                    "loras": [
                        {
                            "path": "https://v3b.fal.media/files/b/0a94bf17/4SJKv1NIWG5OC7FNP5p_q_pytorch_lora_weights.safetensors",
    "file_name": "pytorch_lora_weights.safetensors",
                            "scale": 1.0
                        }
                    ]
                }
            )
            
            # This loop waits for the result specifically
            result = handler.get()
            
            if 'image' in result:
                st.success("Your Signature Design is Ready!")
                st.image(result['image']['url'], use_container_width=True)
            elif 'images' in result:
                st.success("Your Signature Design is Ready!")
                st.image(result['images'][0]['url'], use_container_width=True)
            else:
                st.error("AI finished, but no image was found in the data.")
                st.json(result) # Shows you the "raw" data if it fails
            
        except Exception as e:
            st.error(f"Handshake Error: {e}")
            st.info("The render likely finished on Fal.ai, but the connection timed out. Check your Fal dashboard!")
