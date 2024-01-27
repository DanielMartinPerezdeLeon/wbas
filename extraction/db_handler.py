import logging
from sqlalchemy.schema import CreateSchema
from sqlalchemy.engine import create_engine, Engine
import pandas as pd

import config


def get_engine() -> Engine:
    return create_engine(config.db_url)


def upload_dataframe(df: pd.DataFrame, serie_id: str, rename: str = None):
    name = serie_id if rename is None else rename
    logging.info(f'Uploading {name} to BD')

    df.to_sql(con=get_engine(), schema=config.schema_name, name=name,
              if_exists='replace')


def create_schema():
    with get_engine().connect() as con:
        logging.debug(f'Creating schema {config.schema_name} if not exists')
        con.execute(CreateSchema(config.schema_name, if_not_exists=True))
        con.commit()
