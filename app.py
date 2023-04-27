import cv2
import streamlit as st

st.set_page_config(page_title="streaming-app")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Webcam Live Feed")
options = st.radio("Select any", ["RTSP CAMERA FEED", "LAPTOP WEBCAM FEED"])

if options == "RTSP CAMERA FEED":
    rtsp_url = st.text_input(label="Enter the RTSP URL", type='default')
    if rtsp_url:
        run = st.checkbox('Run')
        # if run:
        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(rtsp_url)

        while run:
            _, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
        else:
            st.write('Stopped')

elif options == "LAPTOP WEBCAM FEED":
    run = st.checkbox('Run')
    # if run:
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    else:
        st.write('Stopped')