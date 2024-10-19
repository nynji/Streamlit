import streamlit as st
import cv2
import numpy as np

# 제목
st.title("이미지 변환 및 회전")

# 이미지 파일 업로드
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 이미지 열기
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 회전 각도 초기화
    if 'angle' not in st.session_state:
        st.session_state.angle = 0

    # 슬라이더로 각도 조정
    st.session_state.angle = st.slider("회전 각도", 0, 360, st.session_state.angle)

    # 두 개의 열 생성
    col1, col2 = st.columns(2)

    # 왼쪽 열에 원본 이미지 표시
    with col1:
        st.image(image, caption='원본 이미지', use_column_width=True)

    # 오른쪽 열에 변환된 이미지 표시
    with col2:
        # 회전된 이미지 계산
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, st.session_state.angle, 1.0)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))

        st.image(rotated_image, caption=f'회전된 이미지: {st.session_state.angle}도', use_column_width=True)

        if st.button('그레이스케일 변환'):
            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            with col2:
                st.image(gray_image, caption='그레이스케일 이미지', use_column_width=True)
