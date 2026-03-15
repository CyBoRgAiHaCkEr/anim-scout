import streamlit as st
from groq import Groq

# --- CONFIG ---
st.set_page_config(page_title="Vihaan's UE5 Shot-Gen", page_icon="🏎️")
st.title("🎬 UE5 Cinematic Transform Engine")
st.write("Get exact XYZ and Rotation data for Vihaan's Car Chase.")

# --- SIDEBAR ---
with st.sidebar:
    api_key = st.text_input("Groq API Key:", type="password")
    car_model = st.selectbox("Target Car", ["Sports Car", "SUV", "Formula 1"])
    shot_type = st.selectbox("Shot Composition", [
        "Low-Angle Wheel Tracking", 
        "Hood-Mounted Interior", 
        "Dynamic Chase Follow", 
        "Bird's Eye / Drone",
        "Dutch Angle Drift"
    ])

# --- MAIN LOGIC ---
if not api_key:
    st.info("Enter your Groq API Key to generate coordinates.")
    st.stop()

client = Groq(api_key=api_key)

if st.button("Calculate Transform Data"):
    # Instructing the AI to act as a UE5 Technical Director
    prompt = f"""
    Provide the exact Unreal Engine 5 transform and camera settings for a '{shot_type}' on a '{car_model}'.
    Assume the car is at world origin (0,0,0) for reference.
    
    Format the output as:
    1. LOCATION (X, Y, Z)
    2. ROTATION (Roll, Pitch, Yaw)
    3. LENS (Focal Length, Aperture)
    4. PRO TIP: How to attach this camera to the car's 'Spring Arm' or 'Socket'.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b", # Using Groq's high-speed Llama 3
        )
        
        result = chat_completion.choices[0].message.content
        
        st.subheader(f"📍 Coordinates for: {shot_type}")
        st.markdown(result)
        
    except Exception as e:
        st.error(f"Error: {e}")

# --- QUICK REFERENCE FOR VIHAAN ---
st.divider()
st.info("💡 **Vihaan's Workflow:** Copy the XYZ values into the 'Transform' section of your CineCameraActor in the UE5 Details Panel.")
