import streamlit as st
import fal_client
import os
import base64

# --- APP INTERFACE ---
st.set_page_config(page_title="Design Partner", layout="centered")
st.title("Joseph's Architectural AI")
st.markdown("Upload a SketchUp white-box massing to generate a high-end proposal.")

# 1. API Key Input
api_key = st.text_input("Enter Fal.ai API Key:", type="password")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# 3. Design Prompt
prompt = st.text_area("Design Style:", value="Modern tropical residential, dusk lighting, warm wood, concrete, hyperrealistic")

# --- ENGINE ---
if st.button("Generate Proposal"):
    if not api_key:
        st.warning("Please enter your API key first.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("The cloud is rendering... Your laptop is safe.")
        os.environ["FAL_KEY"] = api_key
        
        # Convert image for the cloud
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # We are using the "Union" model—the best for architectural lines
            result = fal_client.subscribe(
                "fal-ai/sdxl-controlnet-union/image-to-image",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                    "strength": 0.95
                }
            )
            
            # --- THE SELF-HEALING IMAGE CHECK ---
            image_url = None
            if 'image' in result:
                image_url = result['image']['url']
            elif 'images' in result and len(result['images']) > 0:
                image_url = result['images'][0]['url']
                
            if image_url:
                st.success("Generation Complete!")
                st.image(image_url, caption="AI Generated Proposal")
            else:
                st.error("The AI generated the data, but no image was found. Possible Safety Filter trigger.")
                with st.expander("Debug Report (Show this to Gemini)"):
                    st.write(result)
            
        except Exception as e:
            st.error(f"Engine Error: {e}")
