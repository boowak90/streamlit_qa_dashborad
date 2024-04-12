# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # data = pd.read_csv('data/sample1 copy.csv')
    data = pd.read_csv('data/리뉴얼_이슈현황.csv')
    # data.fillna(0, inplace=True)

    return data
