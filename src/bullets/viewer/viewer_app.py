import streamlit as st
from processing.dataloader import *
from graphs.basic_charts import *
import argparse
import os

#CONSTANTS TO FETCH FROM CONFIG FILE
PATH_TO_LOG = "../../../log/"

parser = argparse.ArgumentParser(description='BullETS Strategy Viewer App')
parser.add_argument('--file', default="test",
                    help="Add one or more animals of your choice")
#To launch the app with the option use : streamlit run viewer_app.py -- --file <path_to_strategy_report>

try:
    args = parser.parse_args()
except SystemExit as e:
    os._exit(e.code)

print(args)


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

    col1, col2, col3 = st.columns(3) #TODO : fetch proper currency
    col1.metric("Profit", "{:.2f}".format(data['profit']), "{:.1f}%".format(100*(data['final_balance']-data['starting_balance'])/data['starting_balance']))
    col2.metric("Final balance", "{:.2f}".format(data['final_balance']), "null")
    col3.metric("Final Cash", "{:.2f}".format(data['final_cash']))

    #st.dataframe(data)
    #st.plotly_chart(candle_chart(data))