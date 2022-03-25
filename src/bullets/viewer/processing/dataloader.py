import os.path as osp
from glob import glob
import pandas as pd
import json

def list_log_files(path_to_log):
    log_dict = {}
    paths_to_directories = glob(path_to_log + "/*", recursive = True)
    for path in paths_to_directories:
        if osp.isfile(osp.join(path,'strategy_report.json')):
            log_dict[osp.basename(path)] = path
        elif len(glob(osp.join(path) + "/*", recursive = True))!=0 :
            log_dict.update(list_log_files(path))
    return log_dict


def load_strategy(path_to_log):
    #data = pd.read_csv(osp.join(path_to_log,"stock_1.csv"))

    with open(osp.join(path_to_log,'strategy_report.json'), 'r') as f:
        data = json.load(f)
        df_transac = pd.DataFrame(data['transactions'])
        df_transac['timestamp'] = pd.to_datetime(df_transac['timestamp'])
        df_successful_transac = df_transac[df_transac.status == "SUCCESSFUL"]
        data['failed_transactions'] = (df_transac.shape[0]-len(df_transac[df_transac.status == "SUCCESSFUL"]))/df_transac.shape[0]  #TODO : make it derive directly fromthe Order classin portofolio
        data['num_transactions'] = len(df_transac)
        data['volume_transactions'] = df_successful_transac['total_price'].sum()
        data['total_fees'] = df_successful_transac['transaction_fees'].sum()
    return data, df_transac