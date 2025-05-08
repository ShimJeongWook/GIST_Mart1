import streamlit as st
import pandas as pd
import os
import random
import serial
import time
import threading
from streamlit_autorefresh import st_autorefresh


def check_photo():
    # 폴더 경로 설정
    directory = 'photo'
    # 파일 확장자
    extension = '.jpg'
    # directory 내의 파일 중 jpg 파일의 이름을 저장할 리스트
    jpg_files = []
    # os.listdir 함수를 사용하여 directory 내의 파일 목록을 가져옴
    for filename in os.listdir(directory):
        # os.path.join을 사용하여 파일의 전체 경로를 구성
        if filename.endswith(extension):
            # 확장자가 .jpg로 끝나는 파일만 리스트에 추가
            jpg_files.append(filename)
    return jpg_files

def check_foods():
    # 폴더 경로 설정
    directory = 'photo/foods'
    # 파일 확장자
    extension = '.jpg'
    # directory 내의 파일 중 jpg 파일의 이름을 저장할 리스트
    jpg_files = []
    # os.listdir 함수를 사용하여 directory 내의 파일 목록을 가져옴
    for filename in os.listdir(directory):
        # os.path.join을 사용하여 파일의 전체 경로를 구성
        if filename.endswith(extension):
            # 확장자가 .jpg로 끝나는 파일만 리스트에 추가
            jpg_files.append(filename)
    return jpg_files

# Streamlit 페이지 설정
st.set_page_config(page_title="POX MART", layout="wide")

# 사용자 정보 딕셔너리 초기화
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {
        "name": "",
        "email": "",
        "points": ""
    }

# 로그인 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 로그인 함수
def login_user(username, password):
    # Placeholder for actual authentication logic
    st.session_state['logged_in'] = True
    # 사용자 정보 업데이트
    st.session_state['user_info']['name'] = f"{username}"
    st.session_state['user_info']['email'] = "anoymous@naver.com"  # 예시 이메일, 실제 로직에 맞게 변경 필요
    st.session_state['user_info']['points'] = str(random.randint(1, 1000)) + "점"  # 예시 포인트, 실제 로직에 맞게 변경 필요

# 로그아웃 함수
def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = {
        "name": "",
        "email": "",
        "points": ""
    }
    st.experimental_rerun()

# 사이드바에 사용자 정보를 표시하는 함수
def show_user_info_in_sidebar():
    name_list = check_photo()
    if str(st.session_state['user_info']['name']+'.jpg') in name_list:
        st.sidebar.image('./photo/' + st.session_state['user_info']['name'] + '.jpg', width = 100)
    else:
        st.sidebar.image('./photo/anony.jpg',width = 100)
    st.sidebar.markdown(f"**{st.session_state['user_info']['name'] + '님'}**")
    st.sidebar.text(st.session_state['user_info']['email'])
    st.sidebar.markdown(f"포인트: {st.session_state['user_info']['points']}")
    st.sidebar.button("로그아웃", on_click=logout_user)
    
# 로그인 폼을 보여주는 함수
def show_login_form():
    st.markdown("""
        <style>
            .stButton > button {
                width: 100%;
                border-radius: 20px; /* Rounded button edges */
            }
            .stTextInput > div > div > input {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns([3,0.5,3])
    with cols[0]:
        st.image('mart.png')
    with cols[2]:
        st.title("GIST MART")
        username = st.text_input("User Name", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        if st.button('Login'):
            login_user(username, password)  # 로그인 검증 로직을 구현해야 함
        
        # 이미지를 나란히 표시
        st.markdown("""
        <style>
        .centered-text {
            text-align: center;
            padding-bottom: 0.5rem;
        }
        </style>
        <div class="centered-text">
            Or sign up with
        </div>
        """, unsafe_allow_html=True)
        
        banner = 'photo/banner.png'    
        colss = st.columns([1,2,1])
        with colss[1]:
            st.image(banner)
    
    
# 로그인 상태라면 사이드바와 메인 페이지를 보여주고,
# 로그인 상태가 아니라면 로그인 폼을 보여줌
if st.session_state['logged_in']:
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
    #st.image("Logo_Small.png",  use_container_width='always')

    # 데이터 초기화 및 세션 상태 설정
    if 'cart' not in st.session_state:
        st.session_state.cart = pd.DataFrame(columns=['location', 'sales', 'brand', 'category', 'product', 'item', 'price', 'quantity'])

    # 품 행을 화면에 표시하는 함수
    def display_product_row():
        st.markdown(
        """
        <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: center;
            align-items: center;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: center;
            align-items: center;
        } 
        div[data-testid="column"]:nth-of-type(3)
        {
            text-align: center;
            align-items: center;
        } 
        div[data-testid="column"]:nth-of-type(4)
        {
            text-align: center;
            align-items: center;
        } 
        div[data-testid="column"]:nth-of-type(5)
        {
            text-align: center;
            align-items: center;
        } 
        </style>
        """,unsafe_allow_html=True
        )
        
        cols = st.columns([1,1,1,1,1])
        with cols[0]:
            """
            ##### Image
            """
        
        with cols[1]:
            """
            ##### Details
            """

        with cols[2]:
            """
            ##### Price
            """
        
        with cols[3]:
            """
            ##### Quantity
            """ 
        with cols[4]:
            """
            ##### Total
            """            
        st.divider()

        for index, row in st.session_state.cart.iterrows():
            cols = st.columns([1,1,1,1,1])
            
            with cols[0]:
                food_list = check_foods()
                if row['brand'] + row['product'] + '.jpg' in food_list:
                   st.image('./photo/foods/' + row['brand'] + row['product'] + '.jpg')
                else:
                   st.image('./photo/foods/sample.jpg')
                    
            
            with cols[1]:       
                st.markdown(f"**{str(row['brand'] + ' ' + row['product'])}**")
                st.write(f"Details : {row['item']}")
                st.write(f"Location : {row['location']}구역")
                
                
            with cols[2]:
                st.markdown(f"**₩ {format(int(row['price']), ',d')}**")
                
            with cols[3]:
                qty = st.number_input(label = '123', value=row['quantity'], min_value=0, max_value=100, step=1, key=f"qty_{index}", label_visibility="collapsed")
                st.session_state.cart.at[index, 'quantity'] = qty
            
            with cols[4]:
                st.markdown(f"**₩ {format(int(row['quantity'] * row['price']), ',d')}**")
                st.markdown("""
                <style>
                    .stButton > button {
                        width: 100%;
                        padding-top: 0rem;
                        padding-bottom: 0rem;
                    }
                </style>
                """, unsafe_allow_html=True)
            if st.button("Remove", key=f"remove_{index}"):
                st.session_state.cart = st.session_state.cart.drop(index).reset_index(drop=True)
            if not(index == len(st.session_state.cart) - 1):
                st.divider()
            
                    
    # 상품 목록 출력
    display_product_row()
    #st.title("")

    # 합계 계산 및 출력
    subtotal = st.session_state.cart['price'].mul(st.session_state.cart['quantity']).sum()
    colll = st.columns([1,1])
    with colll[1]:
        st.markdown(f"<div style='text-align: right;'>Shipping : ₩ 0</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right;'>Total : {'₩ ' + format(subtotal, ',d')}</div>", unsafe_allow_html=True)
    st.title("")
    st.title("")

    # 체크아웃 버튼
    if st.button('Check Out', key='checkout'):
        st.write('Checkout process here...')
    st.title("")


    show_user_info_in_sidebar()
    st.title("")

else:
    
    #상단 배너 출력
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
    #st.image("Logo_Small.png",  use_container_width='always')
    
    st.divider()
    show_login_form()





