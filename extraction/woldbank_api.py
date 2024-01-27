import wbgapi as wb
import pandas as pd
from typing import List
import logging
import argparse

import utils


def get_df(series: str, time: str = 'all') -> pd.DataFrame:
    logging.info(f'Looking for {series}. This may take some seconds...')

    df = wb.data.DataFrame(series=series)

    if not df.empty:

        logging.info(f'{series} found')
        logging.debug(df)

        # Delete YR from the years
        df.columns = df.columns.str.extract(r'YR(\d{4})').squeeze()

        return df


def get_all_series_id() -> pd.DataFrame:
    series = wb.series.info()
    df_2 = pd.DataFrame(series.items)

    return df_2


# Returns all series where keywords passed appears (OR)
def search_for_serie(keyword: str or List[str]):
    df = get_all_series_id()

    if isinstance(keyword, list):
        keyword = '|'.join(keyword)

    if keyword != 'all':
        result = df[df['value'].str.contains(keyword, case=False)]
    else:
        result = df

    if result.empty:
        logging.info('Not found')
    else:
        msg = str()
        for index, row in result.iterrows():
            msg = msg + f"\n{row['value'].ljust(100)}|\t{row['id']}"

        logging.info(msg)





