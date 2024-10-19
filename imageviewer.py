import streamlit as st
import cv2
import numpy as np


st.title("ImageViewer System")


uploaded_file = st.file_uploader("이미지 파일을 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if 'angle' not in st.session_state:
        st.session_state.angle = 0

    st.session_state.angle = st.slider("회전 각도", 0, 360, st.session_state.angle)
    brightness = st.slider("밝기 조정", -100, 100, 0)

    with st.container():
        st.header("이미지 변환")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(image, caption='원본 이미지', use_column_width=True)

        with col2:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, st.session_state.angle, 1.0)
            rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
            adjusted_image = cv2.convertScaleAbs(rotated_image, alpha=1, beta=brightness)
            st.image(adjusted_image, caption=f'조정된 이미지: {st.session_state.angle}도, {brightness} 밝기', use_column_width=True)

        with col3:
            if st.button('gray'):
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                st.image(gray_image, caption='그레이스케일 이미지', use_column_width=True)

    with st.container():
        st.header("이미지 크롭")
        x1 = st.number_input("크롭 시작 X 좌표", min_value=0, max_value=image.shape[1]-1, value=0)
        y1 = st.number_input("크롭 시작 Y 좌표", min_value=0, max_value=image.shape[0]-1, value=0)
        x2 = st.number_input("크롭 끝 X 좌표", min_value=0, max_value=image.shape[1]-1, value=image.shape[1]-1)
        y2 = st.number_input("크롭 끝 Y 좌표", min_value=0, max_value=image.shape[0]-1, value=image.shape[0]-1)

        if st.button("이미지 크롭"):
            cropped_image = image[y1:y2, x1:x2]
            st.image(cropped_image, caption='크롭된 이미지', use_column_width=True)
        


