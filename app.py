import os
import requests
import streamlit as st
from PIL import Image

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
).rstrip("/") + "/predict"


st.set_page_config(
    page_title="Potato Disease Detector",
    page_icon="🥔",
    layout="centered"
)

st.title("🥔 Potato Leaf Disease Detector")

st.write(
    "Upload a potato leaf image to detect disease."
)

uploaded_file = st.file_uploader(
    "Upload Leaf Image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Potato Leaf",
        use_container_width=True
    )

    if st.button("Predict Disease"):

        with st.spinner("Predicting..."):

            response = requests.post(
                API_URL,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                },
                timeout=180
            )

        if response.ok:

            result = response.json()

            disease = (
                result["predicted_class"]
                .replace("Potato___", "")
                .replace("_", " ")
            )

            st.success("Prediction Completed")

            st.subheader(f"Result: {disease}")

            st.metric(
                "Confidence",
                f'{result["confidence"]:.2f}%'
            )

            st.write("Class Probabilities")

            for name, score in result["probabilities"].items():

                st.write(
                    f"{name}: {score:.2f}%"
                )

                st.progress(
                    min(100, max(0, int(score)))
                )

        else:
            st.error(response.text)