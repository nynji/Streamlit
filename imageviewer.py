import streamlit as st
import numpy as np
import cv2
from PIL import Image

# 이미지 회전 함수
def rotate_image(image, angle):
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, rot_mat, (image.shape[1], image.shape[0]))

# Streamlit 애플리케이션 시작
st.title("이미지 뷰어")

# 이미지 업로드
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # OpenCV로 이미지 읽기
    image = np.array(Image.open(uploaded_file))
    st.image(image, caption='원본 이미지', use_column_width=True)

    # 회전 각도 설정
    rotation_angle = st.slider("회전 각도", 0, 360, 0)

    # 이미지 회전
    if rotation_angle != 0:
        rotated_image = rotate_image(image, rotation_angle)
        st.image(rotated_image, caption='회전된 이미지', use_column_width=True)

    # 회색조 변환 버튼
    if st.button("회색조 변환"):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        st.image(gray_image, caption='회색조 이미지', use_column_width=True)

# 추가적인 기능은 여기에 작성
