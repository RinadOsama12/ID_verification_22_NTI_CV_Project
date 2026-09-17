import streamlit as st
import requests


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ID Verification",
    page_icon="🪪",
    layout="centered"
)


# --------------------------------------------------
# FastAPI URL
# --------------------------------------------------

API_URL = st.sidebar.text_input(
    "FastAPI base URL",
    "http://localhost:8000"
)

st.sidebar.caption(
    "Change this if your FastAPI server runs on a different host/port."
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🪪 ID Verification")

st.write(
    "Upload your **ID document** and take a **live selfie**. "
    "We'll check that the face on the ID matches your live photo."
)


# --------------------------------------------------
# Upload ID and take selfie
# --------------------------------------------------

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


# --------------------------------------------------
# Verification
# --------------------------------------------------

st.divider()

ready = bool(id_file and selfie_file)


if st.button(
    "Verify Identity",
    type="primary",
    disabled=not ready,
    use_container_width=True
):

    with st.spinner(
        "Verifying, this can take a few seconds..."
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


            # Send request to FastAPI
            response = requests.post(
                f"{API_URL}/verify-face",
                files=files,
                timeout=60
            )


            response.raise_for_status()

            result = response.json()


        # --------------------------------------------------
        # Connection error
        # --------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                f"❌ Could not connect to FastAPI at {API_URL}"
            )


        # --------------------------------------------------
        # HTTP error
        # --------------------------------------------------

        except requests.exceptions.HTTPError:

            st.error(
                f"❌ FastAPI returned an error: "
                f"{response.status_code}"
            )

            try:
                st.json(response.json())

            except Exception:
                st.code(response.text)


        # --------------------------------------------------
        # Other request errors
        # --------------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Request failed: {e}"
            )


        # --------------------------------------------------
        # Request succeeded
        # --------------------------------------------------

        else:

            # ----------------------------------------------
            # ID face was not detected
            # ----------------------------------------------

            if not result.get("id_detected", False):

                st.error(
                    "❌ No face detected on the uploaded ID."
                )


            # ----------------------------------------------
            # Identity verified
            # ----------------------------------------------

            elif result.get("verified"):

                distance = result.get("face_distance")

                st.success(
                    "## 😊 Identity Verified!"
                )

                st.markdown(
                    "**You are the owner of this ID.**"
                )

                if distance is not None:

                    st.info(
                        f"**Face match distance:** "
                        f"`{distance:.4f}`"
                    )


            # ----------------------------------------------
            # Identity not verified
            # ----------------------------------------------

            else:

                distance = result.get("face_distance")

                st.warning(
                    "## ⚠️ Identity Not Verified"
                )

                st.markdown(
                    "**The selfie does not appear to match "
                    "the face on the ID.**"
                )

                if distance is not None:

                    st.info(
                        f"**Face match distance:** "
                        f"`{distance:.4f}`"
                    )


            # ----------------------------------------------
            # Raw API response
            # ----------------------------------------------

            with st.expander("🔍 Raw API response"):

                st.json(result)


# --------------------------------------------------
# Not ready
# --------------------------------------------------

elif not ready:

    st.info(
        "Upload an ID image and take a selfie above "
        "to enable verification."
    )