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


def Home():
    file_dict = list_log_files(args.path_to_log)


    if 'loaded' not in st.session_state.keys() or st.session_state["loaded"]==False:
        print("not loaded")
        st.session_state['file_dict'] = file_dict
        st.session_state['loaded'] = False
    st.markdown("# BullETS Strategy Viewer")

    selected_file = st.selectbox("Select a log file", file_dict.keys())
    is_selected = st.button("Load log file")
    if args.file != "":
        selected_file=args.file
        is_selected = True
        args.file = ""

    currency = "$" #TODO: to store and to load from the json file

    if is_selected:
        st.markdown("# Analysing {}".format(selected_file))
        st.markdown("---")
        if not st.session_state['loaded']:
            data, df_transac = load_strategy(file_dict[selected_file])
            st.session_state['data'] = data
            st.session_state['df_transac'] = df_transac
            st.session_state['loaded'] = True
            print(data)
        else:
            file_dict = list_log_files(args.path_to_log)
            st.session_state['file_dict'] = file_dict
            data, df_transac = st.session_state['data'], st.session_state['df_transac']

        col_profit, col_final_balance, col_final_cash = st.columns(3)
        col_profit.metric("Profit", "{:.2%}".format(data['profit']/100),"{}".format("STONKS" if data['profit'] >0 else "NOT STONKS"), delta_color="off")
        col_final_balance.metric("Final balance", "{:.1f} {currency}".format(data['final_balance'], currency=currency),"{:.2f} {currency}".format(data['final_balance'] - data['starting_balance'], currency=currency))
        col_final_cash.metric("Final Cash", "{:.1f} {currency}".format(data['final_cash'],currency = currency))

        col_num_transactions, col_failed_transactions, col_total_fees = st.columns(3)
        col_num_transactions.metric("Volume Transactions", "{:.1f} {currency}".format(data['volume_transactions'],currency = currency),"Successful Transactions: {}".format(data['num_transactions']), delta_color="off")
        col_failed_transactions.metric("Failed Transactions", "{:.2%}".format(data['failed_transactions']))
        col_total_fees.metric("Total fees", "{:.1f} {currency}".format(data['total_fees'], currency=currency))
        st.markdown("---")

        st.markdown("## Transactions DataFrame")
        st.dataframe(df_transac)


def SummaryGraph():

    if not st.session_state['loaded']:
        st.markdown("# Please start by loading a log file in the **HOME** section")
    else:
        file_dict = list_log_files(args.path_to_log)
        st.session_state['file_dict'] = file_dict
        data, df_transac = st.session_state['data'], st.session_state['df_transac']

        st.markdown("# Graphical Summary")
        st.markdown("---")

        #TODO: Insert the actual graph summary
        st.plotly_chart(cash_balance_chart(df_transac))

def Compare():
    st.markdown("Not yet implemented")

def Tutorial():
    st.markdown("*For a guide on how to install BullETS please refer to our [GitHub](https://github.com/AlgoETS/BullETS)*")

pages = {'Home': Home, 'Summary Graph': SummaryGraph,'Compare': Compare, 'Tutorial': Tutorial}  # A dict with each pages,you can create a new page by creating a new function and adding it to this dict
page = st.sidebar.selectbox('Navigation', pages.keys())

pages[page]()
