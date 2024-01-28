import argparse
import logging

import config
import utils
from extraction.woldbank_api import search_for_serie, get_df, get_all_series_id
from extraction.db_handler import upload_dataframe, create_schema, delete_table


def main():
    parser = argparse.ArgumentParser(description='wbas commands')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Create subparsers for each command
    search_parser = subparsers.add_parser('search', help='Search for series by keyword and returns the ids '
                                                         'if any founded.'
                                                         'Use all to get a list of all the series.'
                                                         '(wbas search inflation)'
                                                         '(wbas search inflation, spain) (OR)')
    search_parser.add_argument('keyword', nargs='+', help='Keyword to search for series')

    add_parser = subparsers.add_parser('download', help='Download the dataframe of the id and upload it '
                                                        'to the BD')
    add_parser.add_argument('id', help='id of the serie. Use all to upload all the series')
    add_parser.add_argument('-r', '--rename', help='if added the dataframe will be uploaded to the'
                                                   ' DB with this name.'
                                                   '(wbas download FP.CPI.TOTL.ZG -r inflacion)'
                                                   '(wbas download all')

    delete_parser = subparsers.add_parser('delete', help='Delete a serie from BD by id or its name')
    delete_parser.add_argument('id', help='ID or name (In the BD) of the serie to delete')

    args = parser.parse_args()

    if args.subcommand == 'search':
        keyword = args.keyword
        search_for_serie(keyword)
    elif args.subcommand == 'download':
        create_schema()
        if args.id == 'all':
            add_all_series()
        else:
            add_serie(args.id, args.rename)
    elif args.subcommand == 'delete':
        delete_serie(args.id)
    else:
        print("No command provided. Please use wbas -h to see a list of commands.")


def add_serie(serie_id: str, rename: str = None):
    df = get_df(serie_id)
    upload_dataframe(df, serie_id, rename)


def add_all_series():
    logging.info('Downloading all series')
    df = get_all_series_id()
    for index, row in df.iterrows():
        add_serie(row['id'])
    logging.info('Finished')


def delete_serie(name: str):
    logging.info(f'Deleting {config.schema_name}.{name} from BD')
    delete_table(name)


if __name__ == "__main__":
    main()
