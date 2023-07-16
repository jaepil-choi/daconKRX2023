from pathlib import Path

## Path configs

BASE_PATH = Path('.').resolve()
DATA_PATH = BASE_PATH / 'data'
OUTPUT_PATH = BASE_PATH / 'output'

krx_df_PATH = DATA_PATH / 'train.csv'
return_df_PATH = DATA_PATH / 'return_20140101_20230705.pickle'
adjclose_df_PATH = DATA_PATH / 'adjClose_20140101_20230705.pickle'
adjhigh_df_PATH = DATA_PATH / 'adjHigh_20140101_20230705.pickle'
adjlow_df_PATH = DATA_PATH / 'adjLow_20140101_20230705.pickle'
adjopen_df_PATH = DATA_PATH / 'adjOpen_20140101_20230705.pickle'
volume_df_PATH = DATA_PATH / 'volume_20140101_20230705.pickle'
dollarvolume_df_PATH = DATA_PATH / 'dollarvolume_df_20140101_20230705.pickle'
marketcap_df_PATH = DATA_PATH / 'marketcap_df_20140101_20230705.pickle'

## Param configs

PORTFOLIO_DATE = '2023-05-30' # SimOS date