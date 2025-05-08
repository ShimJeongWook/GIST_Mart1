import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import pandas as pd
import ast

# Streamlit 페이지 설정
st.set_page_config(page_title="QR Code Scanner", layout="wide")
#st.image("Logo_Small.png",  use_container_width='always')
st.title("")
st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            border-radius: 20px; /* Rounded button edges */
        }
""", unsafe_allow_html=True)

def add_to_cart(product_row):
    # 상품이 장바구니에 이미 있는지 확인하고, 수량을 업데이트하거나 새 항목을 추가
    cart_index = st.session_state.cart.index[st.session_state.cart['product'] == product_row['product']]
    if cart_index.empty:
        # 상품을 장바구니에 추가
        st.session_state.cart = st.session_state.cart._append({
            'brand' : product_row['brand'],
            'category': product_row['category'],
            'product': product_row['product'],
            'item': product_row['item'],
            'price': product_row['price'],
            'sales': product_row['sales'],
            'location' : product_row['location'],
            'quantity': product_row['quantity']
        }, ignore_index=True)
    else:
        st.session_state.cart.at[cart_index[0], 'quantity'] += product_row['quantity']

# QR 코드를 읽어서 텍스트를 반환하는 함수
def read_qr_code(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = hull
        n_points = len(points)
        for j in range(n_points):
            cv2.line(frame, tuple(points[j]), tuple(points[(j+1) % n_points]), (0,255,0), 3)
        barcode_data = obj.data.decode("utf-8")
        return barcode_data, frame
    return None, frame

# 장바구니 세션 상태 초기화
if 'cart' not in st.session_state:
    # 장바구니 DataFrame 초기화
    st.session_state.cart = pd.DataFrame(columns=['location', 'sales', 'brand', 'category', 'product', 'item', 'price', 'quantity'])



# Streamlit 사이드바 설정
run = st.button('Capture QR')

# 웹캠에서 영상을 캡처할 때 사용할 변수
cap = cv2.VideoCapture(0)

# 메인 화면 설정
frame_holder = st.empty()
info_holder = st.empty()

if run:
    if st.button("Stop"):
        run = False
    while run:
        ret, frame = cap.read()
        if not ret:
            break
        # QR 코드 읽기 시도
        text, annotated_frame = read_qr_code(frame)
        # 웹캠 영상을 화면에 표시
        frame_holder.image(annotated_frame, channels="BGR", use_container_width=True)
        # QR 코드 정보 표시
        if text:
            df = pd.DataFrame(ast.literal_eval(text))
            for index, row in df.iterrows():
                add_to_cart(row) 
                
            
            break
        # Streamlit에서 "Stop" 버튼을 누르면 반복 중단
else:
    st.markdown("""
        <style>
        .centered-text {
            text-align: center;
            padding-bottom: 0.5rem;
        }
        </style>
        <div class="centered-text">
            Press the 'Capture QR' button to start scanning.
        </div>
        """, unsafe_allow_html=True)

# 자원 해제
cap.release()

with st.sidebar:
    st.header("Cart")
    if not st.session_state.cart.empty:
        cart_list = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_list[['product', 'price', 'quantity']])
        if st.button("Clear cart"):
            st.session_state.cart = pd.DataFrame(columns=['location', 'sales', 'brand', 'category', 'product', 'item', 'price', 'quantity'])  # 장바구니 비우기


