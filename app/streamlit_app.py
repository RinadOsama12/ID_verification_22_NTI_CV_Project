import streamlit as st
import requests

st.set_page_config(
    page_title="ID Verification",
    page_icon="🪪",
    layout="centered"
)

API_URL = st.sidebar.text_input(
    "FastAPI base URL",
    "https://earmuff-spotter-shaft.ngrok-free.dev"
)

st.sidebar.caption(
    "Change this if your FastAPI server runs on a different host/port."
)

# Store API result so it remains available when switching tabs
if "result" not in st.session_state:
    st.session_state.result = None


tab1, tab2 = st.tabs([
    "🔐 Identity Verification",
    "📄 Extracted ID Information"
])


# =========================================================
# TAB 1 — ID VERIFICATION
# =========================================================

with tab1:

    st.title("🪪 ID Verification")

    st.write(
        "Upload your **ID document** and take a **live selfie**. "
        "The system will detect the ID information and verify "
        "whether the selfie matches the ID face."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Upload ID")

        id_file = st.file_uploader(
            "Upload a photo of your ID",
            type=["jpg", "jpeg", "png"]
        )

        if id_file:
            st.image(
                id_file,
                caption="ID preview",
                use_container_width=True
            )

    with col2:
        st.subheader("2. Take a live selfie")

        selfie_file = st.camera_input(
            "Look at the camera and take a photo"
        )

        if selfie_file:
            st.image(
                selfie_file,
                caption="Selfie preview",
                use_container_width=True
            )

    st.divider()

    ready = bool(id_file and selfie_file)

    if st.button(
        "Verify Identity",
        type="primary",
        disabled=not ready,
        use_container_width=True
    ):

        with st.spinner(
            "Detecting ID information and verifying identity..."
        ):

            try:

                files = {
                    "id_image": (
                        id_file.name,
                        id_file.getvalue(),
                        id_file.type or "image/jpeg"
                    ),

                    "selfie": (
                        "selfie.jpg",
                        selfie_file.getvalue(),
                        "image/jpeg"
                    ),
                }

                response = requests.post(
                    f"{API_URL}/verify-face",
                    files=files,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                # Save result
                st.session_state.result = result

            except requests.exceptions.ConnectionError:

                st.error(
                    f"❌ Could not connect to FastAPI at {API_URL}"
                )

            except requests.exceptions.HTTPError:

                st.error(
                    f"❌ FastAPI returned an error: "
                    f"{response.status_code}"
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.code(response.text)

            except requests.exceptions.RequestException as e:

                st.error(f"❌ Request failed: {e}")

    # Display verification result
    result = st.session_state.result

    if result:

        st.divider()

        if not result.get("id_detected", False):

            st.error(
                "❌ No face detected on the uploaded ID."
            )

        elif result.get("verified"):

            st.success("## 😊 Identity Verified!")

            st.markdown(
                "**The selfie matches the face detected on the ID.**"
            )

            distance = result.get("face_distance")

            if distance is not None:
                st.info(
                    f"Face match distance: `{distance:.4f}`"
                )

        else:

            st.warning("## ⚠️ Identity Not Verified")

            st.markdown(
                "**The selfie does not appear to match "
                "the face on the ID.**"
            )

            distance = result.get("face_distance")

            if distance is not None:
                st.info(
                    f"Face match distance: `{distance:.4f}`"
                )

        with st.expander("🔍 Raw API response"):
            st.json(result)


# =========================================================
# TAB 2 — EXTRACTED ID INFORMATION
# =========================================================

with tab2:

    st.title("📄 Extracted ID Information")

    result = st.session_state.result

    if result is None:

        st.info(
            "Upload an ID and perform verification first. "
            "The extracted information will appear here."
        )

    else:

        st.subheader("Information extracted from your ID")

        name = result.get("name", "")
        address = result.get("address", "")
        id_number = result.get("id_number", "")

        # Name
        st.markdown("### 👤 Name")

        if name:
            st.text_input(
                "Extracted Name",
                value=name,
                disabled=True
            )
        else:
            st.warning("No name was detected.")

        # Address
        st.markdown("### 🏠 Address")

        if address:
            st.text_area(
                "Extracted Address",
                value=address,
                height=120,
                disabled=True
            )
        else:
            st.warning("No address was detected.")

        # ID number
        st.markdown("### 🔢 ID Number")

        if id_number:
            st.text_input(
                "Extracted ID Number",
                value=id_number,
                disabled=True
            )
        else:
            st.warning("No ID number was detected.")

        st.divider()

        st.caption(
            "The information above was extracted automatically "
            "from the uploaded ID using YOLOv8 and OCR."
        )