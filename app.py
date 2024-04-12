# -*- coding:utf-8 -*-

import streamlit as st
from streamlit_option_menu import option_menu
from home import run_home
from utils import load_data
# from eda.eda_home import run_eda

def main():
    total_df = load_data()
    with st.sidebar:
        # selected = option_menu("대시보드 메뉴", ['홈', '자료분석', '예측'], 
        #                        icons=['house', 'file-bar-graph', 'graph-up-arrow'], menu_icon="cast", default_index=0)
        selected = option_menu("대시보드 메뉴", ['홈'], 
                        icons=['house'], menu_icon="cast", default_index=0)
    if selected == "홈":
        run_home()
    elif selected == "자료분석":
        pass
        # run_eda(total_df)
    elif selected == "예측":
        pass
    else:
        print("error..")
        
if __name__ == "__main__":
    main()