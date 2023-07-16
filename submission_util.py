import numpy as np
import pandas as pd

from sklearn.metrics import (
    confusion_matrix, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    roc_curve, 
    auc
    )
# TODO: SimOS 에서의 정답을 알고있다. 그러므로 eval metric 계산할 수 있다. 

import submission_config as subconfig

DACON_SID_CNT = 2000

krx_df = pd.read_csv(subconfig.krx_df_PATH)
return_df = pd.read_pickle(subconfig.return_df_PATH)

def get_tradables(return_df, trading_date=subconfig.PORTFOLIO_DATE):
    sid_list = return_df.columns

    notnull = return_df.loc[trading_date, :].notnull()
    notzero = return_df.loc[trading_date, :] != 0

    return sid_list[notnull * notzero]

def is_tradables(sid_list, tradables):
    tradables = set(tradables)

    return np.array([True if sid in tradables else False for sid in sid_list])

def get_daconsids(krx_df):
    krx_df.columns = ['date', 'code', 'name', 'volume', 'open', 'high', 'low', 'close']
    dacon_sid_list = [ii[1:] for ii in krx_df['code'].unique()] # 060310 형식으로 바꿔줌

    return dacon_sid_list

def is_daconsids(sid_list, daconsids):
    daconsids = set(daconsids)

    return np.array([True if sid in daconsids else False for sid in sid_list])

class Submission:
    def __init__(self, alpha_series:pd.Series, alpha_name:str, top=200, bottom=200):
        self.alpha_series = alpha_series
        self.alpha_name = alpha_name
        self.top = top
        self.bottom = bottom

        self.sid_list = self.alpha_series.index
        self.tradables = get_tradables(return_df)
        self.daconsids = get_daconsids(krx_df)
    
        self.is_selectables = is_tradables(self.sid_list, self.tradables) * is_daconsids(self.sid_list, self.daconsids)
        self.submission_df = None
        self.alpha_winners = None
        self.alpha_losers = None

    def get_rank(self, export_path=None):
        selectables = self.alpha_series[self.is_selectables]
        top_s = selectables.nlargest(self.top)
        bottom_s = selectables.nsmallest(self.bottom)
        
        self.alpha_winners = top_s.index
        self.alpha_losers = bottom_s.index
        
        submission_df = pd.DataFrame(
            data={'rank': [-1]*DACON_SID_CNT},
            index=self.daconsids
        )
        submission_df.index.name = 'sid'

        submission_df['rank'][top_s.index] = np.arange(1, self.top+1)
        submission_df['rank'][bottom_s.index] = np.arange(DACON_SID_CNT, DACON_SID_CNT - self.bottom, -1)

        submission_df['rank'][submission_df['rank'] == -1] = np.arange(self.top+1, DACON_SID_CNT - self.bottom + 1)

        self.submission_df = submission_df

        if export_path:
            submission_df.index = ['A' + idx for idx in submission_df.index]
            submission_df.index.name = '종목코드'
            submission_df.columns = ['순위']
            submission_df.to_csv(export_path / f'{self.alpha_name}.csv', encoding='utf-8')
            
            print(f'Saved to {export_path / self.alpha_name}.csv')
            return submission_df

        return submission_df
    
    

    