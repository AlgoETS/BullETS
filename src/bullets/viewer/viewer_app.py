import streamlit as st
from processing.dataloader import *
from graphs.basic_charts import *

#CONSTANTS TO FETCH FROM CONFIG FILE
PATH_TO_LOG = "../../../log/"


if 'loaded' not in st.session_state.keys() or st.session_state["loaded"]==False:
    file_dict = list_log_files(PATH_TO_LOG)
    st.session_state['file_dict'] = file_dict
    st.session_state['loaded'] = False
st.markdown("# BullETS Strategy Viewer")

selected_file = st.selectbox("Select a log file", file_dict.keys())
is_selected = st.button("Load log file")


if is_selected :

    st.markdown("# Analysing {}".format(selected_file))
    st.markdown("---")
    if not st.session_state['loaded']:
        data = load_strategy(file_dict[selected_file])
        print("not loaded")
        st.session_state['loaded'] = True
    else:
        st.session_state['file_dict'] = file_dict
        print("loaded")

    st.sidebar.markdown("Nice sidebar")


    st.dataframe(data)
    st.plotly_chart(candle_chart(data))