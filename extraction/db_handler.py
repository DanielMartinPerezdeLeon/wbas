import logging

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema, DropTable, Table
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


def delete_table(table_name: str):
    logging.debug(f'Dropping table {table_name} if exists')
    base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=get_engine(), schema=config.schema_name)
    table = metadata.tables[f'{config.schema_name}.{table_name}']
    if table_name is not None:
        base.metadata.drop_all(get_engine(), [table], checkfirst=True)
