import os.path as osp
from glob import glob
import pandas as pd


def list_log_files(path_to_log):
    print(glob(path_to_log + "/*", recursive=True))
    log_dict = {}
    paths_to_directories = glob(path_to_log + "/*", recursive=True)
    for path in paths_to_directories:
        if osp.isfile(osp.join(path, 'strategy_log.json')):
            print(osp.basename(path))
            log_dict[osp.basename(path)] = path
        elif len(glob(osp.join(path) + "/*", recursive=True)) != 0:
            log_dict.update(list_log_files(path))
        else:
            return {}
    print(log_dict)
    return log_dict


def load_strategy(path_to_log):
    data = pd.read_csv(osp.join(path_to_log, "stock_1.csv"))
    return data
