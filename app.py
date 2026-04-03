import streamlit as st
import fal_client
import os
import base64

# --- THE APP INTERFACE ---
st.set_page_config(page_title="Design Partner", layout="centered")
st.title("Joseph's Architectural AI")
st.markdown("Upload a SketchUp massing to generate a high-end proposal.")

# 1. Ask for the Fal API Key
api_key = st.text_input("Enter Fal.ai API Key:", type="password")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# 3. Text Input
prompt = st.text_area("Design Style:", value="Modern tropical architecture, dusk lighting, warm wood and concrete, hyperrealistic, high-end residential photography")

# --- THE ENGINE ---
if st.button("Generate Proposal"):
    if not api_key:
        st.warning("Please enter your API key first.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("The cloud is rendering... Your laptop is resting.")
        os.environ["FAL_KEY"] = api_key
        
        # Format the image for the cloud
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # Using .run() instead of .subscribe() for maximum compatibility
            result = fal_client.run(
                "fal-ai/sdxl-controlnet-union/image-to-image",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                    "controlnet_conditioning_scale": 0.8,
                    "strength": 0.95
                }
            )
            
            st.success("Generation Complete!")
            
            # Show the result
            if 'image' in result:
                st.image(result['image']['url'], caption="AI Generated Proposal")
            elif 'images' in result:
                st.image(result['images'][0]['url'], caption="AI Generated Proposal")
            
        except Exception as e:
            st.error(f"Error: {e}")
