import os.path as osp
from glob import glob
import pandas as pd
import json

def list_log_files(path_to_log):
    print(glob(path_to_log + "/*", recursive = True))
    log_dict = {}
    paths_to_directories = glob(path_to_log + "/*", recursive = True)
    for path in paths_to_directories:
        if osp.isfile(osp.join(path,'strategy_report.json')):
            print("bah frérot")
            print(osp.basename(path))
            log_dict[osp.basename(path)] = path
        elif len(glob(osp.join(path) + "/*", recursive = True))!=0 :
            log_dict.update(list_log_files(path))
        else :
            return log_dict
    print(log_dict)
    return log_dict


def load_strategy(path_to_log):
    #data = pd.read_csv(osp.join(path_to_log,"stock_1.csv"))

    with open(osp.join(path_to_log,'strategy_report.json'), 'r') as f:
        data = json.load(f)


    return data