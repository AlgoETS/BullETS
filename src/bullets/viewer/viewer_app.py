import streamlit as st
from processing.dataloader import *
from graphs.basic_charts import *
import argparse
import os
print(os.getcwd())
#CONSTANTS TO FETCH FROM CONFIG FILE

parser = argparse.ArgumentParser(description='BullETS Strategy Viewer App')
parser.add_argument('--file', default="")
parser.add_argument('--path_to_log', default="../../../log/")
#To launch the app with the option use : streamlit run viewer_app.py -- --file <path_to_strategy_report>

try:
    args = parser.parse_args()
except SystemExit as e:
    os._exit(e.code)

print(args)

if 'loaded' not in st.session_state.keys() or st.session_state["loaded"]==False:
    print("not loaded")
    file_dict = list_log_files(args.path_to_log)
    st.session_state['file_dict'] = file_dict
    st.session_state['loaded'] = False
st.markdown("# BullETS Strategy Viewer")

selected_file = st.selectbox("Select a log file", file_dict.keys())
is_selected = st.button("Load log file")
if args.file != "":
    selected_file=args.file
    is_selected = True
    args.file = ""


if is_selected:
    print("is_selected")
    st.markdown("# Analysing {}".format(selected_file))
    st.markdown("---")
    if not st.session_state['loaded']:
        data, df_transac = load_strategy(file_dict[selected_file])
        st.session_state['loaded'] = True
    else:
        st.session_state['file_dict'] = file_dict

    st.sidebar.markdown("Nice sidebar")

    col_profit, col_final_balance, col_final_cash = st.columns(3) #TODO : fetch proper currency
    col_profit.metric("Profit", "{:.2%}".format(data['profit']/100),"{}".format("STONKS" if data['profit'] >0 else "NOT STONKS"))
    col_final_balance.metric("Final balance", "{:.2f}".format(data['final_balance']),"Starting : {:.2f}".format(data['starting_balance']), delta_color="off")
    col_final_cash.metric("Final Cash", "{:.2f}".format(data['final_cash']))

    col_num_transactions, col_failed_transactions, col3 = st.columns(3)
    col_num_transactions.metric("Volume Transactions", "{:.2f}".format(data['volume_transactions']),"Successful Transactions: {}".format(data['num_transactions']), delta_color="off")
    col_failed_transactions.metric("Failed Transactions", "{:.2%}".format(data['failed_transactions']))

    st.dataframe(df_transac)
    st.plotly_chart(cash_balance_chart(df_transac))
    #st.plotly_chart(candle_chart(data))