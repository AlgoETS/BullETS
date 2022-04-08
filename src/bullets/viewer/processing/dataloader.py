import os.path as osp
import random
from glob import glob
import pandas as pd
import json
import numpy as np

def list_log_files(path_to_log):
    log_dict = {}
    paths_to_directories = glob(path_to_log + "/*", recursive = True)
    for path in paths_to_directories:
        if osp.isfile(osp.join(path,'strategy_report.json')):
            log_dict[osp.basename(path)] = path
        elif len(glob(osp.join(path) + "/*", recursive = True))!=0 :
            log_dict.update(list_log_files(path))
    return log_dict

def get_value_symbol(symbol,timestamp): #TODO: make this function request the defined datasource, right now it's just here for a testing purpose
    return 13 + random.randint(0,1000) * 0.01

def load_strategy(path_to_log):
    #data = pd.read_csv(osp.join(path_to_log,"stock_1.csv"))

    with open(osp.join(path_to_log,'strategy_report.json'), 'r') as f:
        data = json.load(f)
        df_transac = pd.DataFrame(data['transactions'])
        df_transac['timestamp'] = pd.to_datetime(df_transac['timestamp'])
        df_successful_transac = df_transac[df_transac.status == "SUCCESSFUL"]
        data['failed_transactions'] = (df_transac.shape[0]-len(df_transac[df_transac.status == "SUCCESSFUL"]))/df_transac.shape[0]  #TODO : make it derive directly fromthe Order classin portofolio
        data['num_transactions'] = len(df_transac)
        data['volume_transactions'] = df_successful_transac['total_price'].apply(lambda x: np.abs(x)).sum()
        data['total_fees'] = df_successful_transac['transaction_fees'].sum()

        # running_value_by_symbol = {s:0 for s in df_transac['symbol']}
        # l_value = []
        # for i in range(df_transac.shape[0]):
        #     running_value_by_symbol[df_transac.loc[i, 'symbol']] += df_transac.loc[i,
        #     l_value.append(
        traded_symbols = pd.unique(df_successful_transac['symbol'])

        df_cum_share = pd.DataFrame(np.zeros((df_transac.shape[0],traded_symbols.shape[0])),columns=[ "num_share_" + txt for txt in traded_symbols.tolist()])
        df_cum_share_value = pd.DataFrame(np.zeros((df_transac.shape[0],traded_symbols.shape[0])),columns=[ "share_value_" + txt for txt in traded_symbols.tolist()])
        df_transac = pd.concat([df_transac, df_cum_share,df_cum_share_value], axis=1, join="inner")
        for index, row in df_transac.iterrows():
                if row['status'] == "SUCCESSFUL":
                    df_transac.loc[index:,"num_share_" + row['symbol']] += row['nb_shares']
                else:
                    if index != 0:
                        df_transac.loc[index:, "num_share_" + row['symbol']] = row[index-1:, "num_share_" + row['symbol']]
                    else:
                        pass
                for symb in traded_symbols:
                    df_transac.loc[index:, "share_value_" + symb] = df_transac.loc[index:,"num_share_" + symb] * get_value_symbol(symb,row['timestamp'])
    return data, df_transac