import streamlit as st
Enter "help" below or click "Help" above for more information.
>>> import streamlit as st
... import fal_client
... import os
... import base64
... 
... # --- THE APP INTERFACE ---
... st.set_page_config(page_title="Design Partner", layout="centered")
... st.title("Joseph's Architectural AI")
... st.markdown("Upload a SketchUp white-box massing to generate a rendered proposal.")
... 
... # 1. Ask for the Fal API Key (So you can use it on your phone)
... api_key = st.text_input("Enter Fal.ai API Key:", type="password")
... 
... # 2. File Uploader for your SketchUp Export
... uploaded_file = st.file_uploader("Upload 3D Massing (ControlNet Baseline)", type=["jpg", "jpeg", "png"])
... 
... # 3. Text Input for the Design Style
... prompt = st.text_area("Architectural Prompt:", value="Modern tropical, dusk lighting, warm wood, concrete, highly detailed architectural photography")
... 
... # --- THE ENGINE ---
... if st.button("Generate Proposal"):
...     if not api_key:
...         st.warning("Please enter your API key first.")
...     elif uploaded_file is None:
...         st.warning("Please upload a SketchUp massing image.")
...     else:
...         st.info("Sending to Fal.ai... Your hardware is resting.")
...         
...         # Tell the app to use your key
...         os.environ["FAL_KEY"] = api_key
...         
...         # Convert the uploaded SketchUp image into a readable format for the cloud
...         bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        file_extension = uploaded_file.name.split('.')[-1].lower()
        # Fix extension for jpg
        if file_extension == 'jpg': file_extension = 'jpeg'
        image_uri = f"data:image/{file_extension};base64,{base64_str}"
        
        try:
            # Send the image and prompt to Fal's ControlNet
            result = fal_client.subscribe(
                "fal-ai/fast-sdxl/controlnet",
                arguments={
                    "prompt": prompt,
                    "control_image_url": image_uri,
                    "controlnet_type": "canny" # 'Canny' tells AI to look at the hard edges/lines of your SketchUp model
                }
            )
            
            # Display the resulting image
            st.success("Generation Complete!")
            output_image_url = result['images'][0]['url']
            st.image(output_image_url, caption="AI Generated Proposal")
            
        except Exception as e:
