import argparse

import utils
from extraction.woldbank_api import search_for_serie, get_df
from extraction.db_handler import upload_dataframe, create_schema


def main():
    parser = argparse.ArgumentParser(description='wbas commands')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Create subparsers for each command
    search_parser = subparsers.add_parser('search', help='Search for series by keyword and returns the ids '
                                                         'if any founded.'
                                                         'Use all to get a list of all the series')
    search_parser.add_argument('keyword', nargs='+', help='Keyword to search for series')

    add_parser = subparsers.add_parser('download', help='Download the dataframe of the id and upload it '
                                                        'to the BD')
    add_parser.add_argument('id', help='id of the serie')
    add_parser.add_argument('rename', help='if added the dataframe will be uploaded to the DB with this'
                                           'name')

    delete_parser = subparsers.add_parser('delete', help='Delete a serie from BD by id')
    delete_parser.add_argument('id', help='ID of the serie to delete')

    args = parser.parse_args()

    if args.subcommand == 'search':
        keyword = args.keyword
        search_for_serie(keyword)
    elif args.subcommand == 'download':
        create_schema()
        add_serie(args.id, args.rename)
    elif args.subcommand == 'delete':
        delete_serie(args.series_id)
    else:
        print("No command provided. Please use wbas -h to see a list of commands.")


def add_serie(serie_id: str, rename: str = None):
    df = get_df(serie_id)
    upload_dataframe(df, serie_id, rename)




if __name__ == "__main__":
    main()
