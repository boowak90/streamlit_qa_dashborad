# -*- coding:utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from utils import load_data
import streamlit as st
from millify import prettify
import os
from matplotlib import font_manager as fm


# # Set the layout to "wide" mode
# st.set_page_config(layout="wide")

# # Inject custom CSS with st.markdown
# st.markdown("""
# <style>
#     /* Ensures full control over the width */
#     .css-1lcbmhc {
#         padding: 0;
#     }
#     .css-1adrfps {
#         padding: 0;
#     }
#     .reportview-container .main {
#         flex: 1;
#     }
#     .block-container css-1y4p8pa e1g8pov64 {
#         width: 95%;
#         padding: 2rem 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# Matplotlib에서 한글 깨짐 문제
# plt.rcParams['font.family'] ='Malgun Gothic'
# plt.rcParams['axes.unicode_minus'] =False

fpath = os.path.join(os.getcwd(), "font/NanumGothic-Regular.ttf")
prop = fm.FontProperties(fname=fpath)


def generate_summary_report(data):
    # Replace NaN values with 'N/A' if they are being read as NaN
    data['우선순위'].fillna('N/A', inplace=True)

    status_categories = {
        "Critical": "red",
        "Major": "blue",
        "Minor": "green",
        "Trivial": "gray",
    }

    # summary = {
    #     "Total TC": len(data),
    #     "Passed": (data['Status'] == 'Pass').sum(),
    #     "Failed": (data['Status'] == 'Fail').sum(),
    #     "N/T": (data['Status'] == 'N/T').sum(),
    #     "N/A": (data['Status'] == 'N/A').sum(),
    # }

    # Create a summary dictionary
    summary = {"Total TC": len(data)}
    # Add the counts of each status to the summary
    for status, color in status_categories.items():
        summary[status] = (data['우선순위'] == status).sum()
    return summary


# Function to plot results
def plot_test_outcomes(data):
    status_categories = {
        "Critical": "red",
        "Major": "blue",
        "Minor": "green",
        "Trivial": "gray",
    }
    
    outcome_counts = data['우선순위'].value_counts().reindex(status_categories.keys(), fill_value=0)
    colors = [status_categories[status] for status in outcome_counts.index]
    
    fig, ax = plt.subplots()

    # Create a bar chart
    bars = ax.bar(outcome_counts.index, outcome_counts.values, color=colors)
    # Add numerical labels to each bar
    ax.bar_label(bars, padding=0)  # padding: adjusts the vertical spacing of labels from the bars
    
    outcome_counts.plot(kind='bar', ax=ax, color=colors)
    ax.set_title(f'이슈 현황', fontproperties=prop)
    ax.set_xlabel('우선순위', fontproperties=prop)
    ax.set_ylabel('개수', fontproperties=prop)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    st.pyplot(fig)




def plot_components_from_excel(data):

    # Assume the column names are in Korean, e.g., '컴포넌트' for components
    component_counts = data['컴포넌트'].value_counts()

    # Set up colors, map each component to a color
    colors = plt.cm.viridis(np.linspace(0, 1, len(component_counts)))

    fig, ax = plt.subplots()
    # Create a bar chart
    bars = ax.bar(component_counts.index, component_counts.values, color=colors)
    # Add numerical labels to each bar
    ax.bar_label(bars, padding=0)

    ax.set_title('컴포넌트별 이슈 현황', fontproperties=prop)
    ax.set_xlabel('컴포넌트', fontproperties=prop)
    ax.set_ylabel('개수', fontproperties=prop)
    ax.set_xticklabels(component_counts.index, rotation=45, ha="right", fontproperties=prop)
    st.pyplot(fig)




def run_home():
    
    total_df = load_data()
    st.markdown("# 대시보드 개요 \n"
    "#### 본 프로젝트는 QA 및 Tester를 위한 대시보드입니다.")

    st.markdown("#### 사이드 메뉴의 [컴포넌트]와 [월]을 선택하면 각 컴포넌트의 월별 이슈 데이터가 출력됩니다.")
    st.markdown(" - 필수 컬럼명: 생성일자, 우선순위, 컴포넌트")
    st.markdown(" - 생성일자: YYYY-MM-DD")
    st.markdown(" - 우선순위: Critical, Major, Minor, Trivial")
    st.markdown(" - 컴포넌트: 사용자 지정")

    if st.checkbox('업로드 데이터 확인'):
        st.write(total_df)


    total_df['생성일자'] = pd.to_datetime(total_df['생성일자'], format="%Y-%m-%d")
    total_df['month'] = total_df['생성일자'].dt.month
    # total_df = total_df.loc[total_df['HOUSE_TYPE'] == '아파트', :]

    
    sgg_nm = st.sidebar.selectbox("컴포넌트", sorted(total_df['컴포넌트'].unique()))
    select_month = st.sidebar.selectbox("확인하고 싶은 월을 선택하세요 ", ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'])
    # select_month = st.sidebar.radio("확인하고 싶은 월을 선택하세요 ", ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'])
    month_dict = {'1월' : 1, '2월' : 2, '3월' : 3, '4월' : 4,'5월' : 5, '6월' : 6, '7월' : 7, '8월' : 8, '9월' : 9, '10월' : 10, '11월' : 11, '12월' : 12}

    status_dict = {'Critical' : 1, 'Major' : 2, 'Minor' : 3, 'Trivial' : 4}

    status_critical = total_df[total_df['우선순위'] == 'Critical'].shape[0]
    status_major = total_df[total_df['우선순위'] == 'Major'].shape[0]
    status_minor = total_df[total_df['우선순위'] == 'Minor'].shape[0]
    status_trivial = total_df[total_df['우선순위'] == 'Trivial'].shape[0]
    

    total = total_df['No.'].count()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    # st.subheader(f'전체 이슈: {total}')
    st.subheader('전체 이슈 현황')
    total_col1, total_col2, total_col3, total_col4, total_col5 = st.columns(5)
    # with total_col1:
    #     st.metric(label= f"Critical 이슈", value = prettify(status_critical))
    # with total_col2:
    #     st.metric(label= f"Major 이슈", value = prettify(status_major))
    # with total_col3:
    #     st.metric(label= f"Minor 이슈", value = prettify(status_minor))
    # with total_col4:
    #     st.metric(label= f"Trivial 이슈", value = prettify(status_trivial))
    # st.markdown("<hr>", unsafe_allow_html=True)

    with total_col1:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>전체 이슈</h4>
                    <h3 style='margin: 0; color: white;'>{prettify(total)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with total_col2:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Critical 이슈</h4>
                    <h3 style='margin: 0; color: red;'>{prettify(status_critical)}</h3>
                    </div>
                    """, unsafe_allow_html=True)

    with total_col3:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Major 이슈</h4>
                    <h3 style='margin: 0; color: blue;'>{prettify(status_major)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with total_col4:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Minor 이슈</h4>
                    <h3 style='margin: 0; color: green;'>{prettify(status_minor)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with total_col5:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Trivial 이슈</h4>
                    <h3 style='margin: 0; color: gray;'>{prettify(status_trivial)}</h3>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)



    st.subheader("전체 이슈 현황 그래프")
    plot_test_outcomes(total_df)
    plot_components_from_excel(total_df)
    st.markdown("<hr>", unsafe_allow_html=True)


    st.subheader(f'({select_month}) "{sgg_nm}" 이슈 현황')

    col1, col2, col3, col4, col5 = st.columns(5)
    filtered_month = total_df[total_df['month'] == month_dict[select_month]]
    filtered_month = filtered_month[filtered_month['컴포넌트'] == sgg_nm]
    # march_min_price = filtered_month['OBJ_AMT'].count()
    # march_max_price = filtered_month['OBJ_AMT'].count()

    priority_status = filtered_month['우선순위'].count()
    priority_critical = filtered_month[filtered_month['우선순위'] == 'Critical'].shape[0]
    priority_major = filtered_month[filtered_month['우선순위'] == 'Major'].shape[0]
    priority_minor = filtered_month[filtered_month['우선순위'] == 'Minor'].shape[0]
    priority_trivial = filtered_month[filtered_month['우선순위'] == 'Trivial'].shape[0]

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("컴포넌트별 현황 그래프")
    plot_test_outcomes(filtered_month)
    

    # with col1:
    #     st.metric(label= f"총 이슈", value = prettify(priority_status))
    # with col2:
    #     st.metric(label= f"Critical 이슈", value = prettify(priority_critical))
    # with col3:
    #     st.metric(label= f"Major 이슈", value = prettify(priority_major))
    # with col4:
    #     st.metric(label= f"Minor 이슈", value = prettify(priority_minor))
    # with col5:
    #     st.metric(label= f"Trivial 이슈", value = prettify(priority_trivial))

    with col1:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>전체 이슈</h4>
                    <h3 style='margin: 0; color: white;'>{prettify(priority_status)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Critical 이슈</h4>
                    <h3 style='margin: 0; color: red;'>{prettify(priority_critical)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Major 이슈</h4>
                    <h3 style='margin: 0; color: blue;'>{prettify(priority_major)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Minor 이슈</h4>
                    <h3 style='margin: 0; color: green;'>{prettify(priority_minor)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h4 style='margin: 0; color: #999; font-size: 20px;'>Trivial 이슈</h4>
                    <h3 style='margin: 0; color: gray;'>{prettify(priority_trivial)}</h3>
                    </div>
                    """, unsafe_allow_html=True)

    # st.markdown("<hr>", unsafe_allow_html=True)
    # st.markdown("### 아파트 가격 상위 3")
    # sorted_df = filtered_month[["컴포넌트", "우선순위", "BLDG_NM", "OBJ_AMT"]]
    # df = st.dataframe(sorted_df.sort_values(by='OBJ_AMT', ascending=False).head(3).reset_index(drop=True))
    # st.markdown("<hr>", unsafe_allow_html=True)
    # st.markdown("### 아파트 가격 하위 3")
    # sorted_df = filtered_month[["컴포넌트", "우선순위", "BLDG_NM", "OBJ_AMT"]]
    # st.dataframe(sorted_df.sort_values(by='OBJ_AMT', ascending=True).head(3).reset_index(drop=True))
    # st.markdown("<hr>", unsafe_allow_html=True)
    # st.caption("Made By. Choi Byoung Wook")