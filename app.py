import streamlit as st
import fal_client
import os
import base64

# --- THE APP INTERFACE ---
st.set_page_config(page_title="Design Partner", layout="centered")
st.title("Joseph's Architectural AI")
st.markdown("Upload a SketchUp massing to generate a signature render.")

# 1. Ask for the Fal API Key
api_key = st.text_input("Enter Fal.ai API Key:", type="password")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# 3. Design Prompt
prompt = st.text_area("Design Style:", value="Modern tropical architecture, dusk lighting, warm wood and concrete, hyperrealistic, professional architectural photography")

# --- THE ENGINE ---
if st.button("Generate Proposal"):
    if not api_key:
        st.warning("Please enter your API key first.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("The cloud is rendering... Your Acer is resting.")
        os.environ["FAL_KEY"] = api_key
        
        # Format the image for the cloud
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # Using the absolute latest stable Canny model
            result = fal_client.subscribe(
                "fal-ai/flux/canny",
                arguments={
                    "prompt": prompt,
                    "control_image_url": image_uri,
                    "image_size": "landscape_4_3",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5
                }
            )
            
            if 'image' in result:
                st.success("Generation Complete!")
                st.image(result['image']['url'], caption="AI Generated Proposal")
            else:
                st.error("No image found. Check the output below.")
                st.write(result)
            
        except Exception as e:
            st.error(f"Engine Error: {e}")
