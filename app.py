import streamlit as st
import fal_client
import os
import base64

# --- APP INTERFACE ---
st.set_page_config(page_title="Design Partner", layout="centered")
st.title("Joseph's Architectural AI")
st.markdown("Upload a SketchUp white-box massing to generate a rendered proposal.")

# 1. Input for the API Key
api_key = st.text_input("Enter Fal.ai API Key:", type="password")

# 2. File Uploader for your SketchUp Export
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# 3. Text Input for the Design Style
prompt = st.text_area("Architectural Prompt:", value="Modern tropical residential, dusk lighting, warm wood, concrete, hyperrealistic")

# --- GENERATION ENGINE ---
if st.button("Generate Proposal"):
    if not api_key:
        st.warning("Please enter your API key first.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("Processing in the cloud... Your laptop is resting.")
        
        # Set the environment key
        os.environ["FAL_KEY"] = api_key
        
        # Convert uploaded image to a format the cloud can read
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # Send to Fal.ai using the SDXL ControlNet model
            result = fal_client.subscribe(
                "fal-ai/sdxl-controlnet-union/image-to-image",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                    "controlnet_conditioning_scale": 0.8,
                    "strength": 0.95
                }
            )
            
            # Show the result
            st.success("Generation Complete!")
            st.image(result['image']['url'], caption="AI Generated Proposal")
            
        except Exception as e:
            st.error(f"Error: {e}")
