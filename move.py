

import os
import time

import pandas as pd

DIR_BASE = "/home/zhenlin4/kaggle/kaggle-3/weights"

def check_info(cfg="cfg_2a", fold=0):
    # check the creation time of the files in the directory
    # return a dict with the file name and the creation time
    # in the format {file_name: creation_time}
    dir_path = os.path.join(DIR_BASE, cfg, f"fold{fold}")
    files = os.listdir(dir_path)
    file_info = {}
    for file in files:
        file = os.path.join(dir_path, file)
        file_info[file] = {
            'time': time.ctime(os.path.getctime(file)),
            'timet': time.mktime(time.strptime(time.ctime(os.path.getctime(file)))),
            'path': file
        }
        # convert the time to a number for comparison
    file_info = pd.DataFrame(file_info).T
    file_info = file_info[file_info['path'].map(lambda x: x.endswith(".pth"))]
    file_info['seed'] = file_info['path'].map(lambda x: x.split("_seed")[-1].split(".")[0])
    file_info = file_info.sort_values('timet', ascending=True)
    assert cfg.endswith("a")
    assert len(file_info) % 4 == 0
    file_info['config_version'] = [_ for _ in ['a', 'b','c','d'] for _i in range(4)][:len(file_info)]
    assert (file_info.groupby('config_version')['seed'].nunique() == 2).all()

    file_info['dst_file'] = file_info.apply(lambda r: r['path'].replace(cfg, cfg.replace("a", r['config_version'])), axis=1)

    return file_info


def move_files(cfg="cfg_2a", fold=0, do=False):
    file_info = check_info(cfg, fold)
    for i, row in file_info.iterrows():
        if row['dst_file'] == row['path']:
            continue
        if not os.path.exists(os.path.dirname(row['dst_file'])):
            os.makedirs(os.path.dirname(row['dst_file']))
            print(f"mkdir {os.path.dirname(row['dst_file'])}")
        if do:
            os.system(f"mv {row['path']} {row['dst_file']}")
        print(f"mv {row['path']} {row['dst_file']}")

if __name__ == '__main__':
    #res = check_info("cfg_2a", 1)
    #move_files("cfg_2a", 1, do=False)
    for fold in [0,1,2,3]:
        move_files("cfg_5a", fold, do=True)