import streamlit as st
import requests

st.set_page_config(page_title="ID Verification", page_icon="🪪", layout="centered")

API_URL = st.sidebar.text_input("FastAPI base URL", "http://localhost:8000")
st.sidebar.caption("Change this if your FastAPI server runs on a different host/port.")

st.title("🪪 ID Verification")
st.write("Upload your ID document and take a live selfie. We'll check that the face on the ID matches your live photo.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload ID")
    id_file = st.file_uploader("Upload a photo of your ID", type=["jpg", "jpeg", "png"])
    if id_file:
        st.image(id_file, caption="ID preview", use_container_width=True)

with col2:
    st.subheader("2. Take a live selfie")
    selfie_file = st.camera_input("Look at the camera and take a photo")
    if selfie_file:
        st.image(selfie_file, caption="Selfie preview", use_container_width=True)

st.divider()

ready = bool(id_file and selfie_file)

if st.button("Verify Identity", type="primary", disabled=not ready, use_container_width=True):
    with st.spinner("Verifying, this can take a few seconds..."):
        try:
            files = {
                "id_image": (id_file.name, id_file.getvalue(), id_file.type or "image/jpeg"),
                "selfie": ("selfie.jpg", selfie_file.getvalue(), "image/jpeg"),
            }
            response = requests.post(f"{API_URL}/verify-face", files=files, timeout=60)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the verification API at {API_URL}. Details: {e}")
        else:
            if not result.get("id_detected"):
                st.error("❌ No ID detected in the uploaded image. Try a clearer, well-lit photo of the ID.")
            elif result.get("verified"):
                distance = result.get("face_distance")
                st.success(
                    f"✅ Identity Verified! (match distance: {distance:.4f})"
                    if distance is not None else "✅ Identity Verified!"
                )
            else:
                distance = result.get("face_distance")
                st.warning(
                    f"⚠️ Faces do not appear to match. (match distance: {distance:.4f})"
                    if distance is not None else "⚠️ Faces do not appear to match."
                )

            with st.expander("Raw API response"):
                st.json(result)
elif not ready:
    st.info("Upload an ID image and take a selfie above to enable verification.")