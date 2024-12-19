import argparse
import json
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from duckdb import IOException
from jinja2 import Template

from database_manager import (
    connect_to_database,
    close_database_connection,
    execute_query,
    read_query
)

def read_locations_ids(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        locations = json.load(f)
        f.close()

    locations_ids = [str(id) for id in locations.keys()]
    locations_ids

def compile_data_file_paths(
    data_file_path_template: str, locations_ids: List[str], start_date: str, end_date:str
) -> List[str]:
    
    start_date = datetime.strptime(start_date, "%Y-%m")
    end_date = datetime.strptime(end_date, "%Y-%m")

    data_file_paths = []
    for locations_id in locations_ids:
        index_date = start_date
        while index_date <= end_date:
            data_file_path = Template(data_file_path_template).render(
                Location_id=locations_id,
                year=str(index_date.year),
                month=str(index_date.month).zfill(2),
            )
            data_file_paths.append(data_file_path)
            index_date += relativedelta(month=1)

    return data_file_paths

def compile_data_file_query(
    base_path: sr, data_file_path: str, extract_query_template: str
) -> str:
    extract_query = Template(extract_query_template).render(
        data_file_path=f"{base_path}/{data_file_path}"
    )
    return extract_query

def extract_data(args):
    locations_ids = read_locations_ids(args.locations_file_path)

    data_file_path_template = "locationid={{location_id}}/year={{year}}/month={{month}}/*"

    data_file_paths  =  compile_data_file_paths(
        data_file_path_template=data_file_path_template,
        locations_ids=locations_ids,
        start_date=args.start_date,
        end_date=args.end_date
    )

    execute_query_template  = read_query(path=args.extract_query_template_path)

    con = connect_to_database(path=args.database_path)

    for data_file_path  in data_file_paths:
        query = compile_data_file_query(
            base_path=args.source_base_path,
            data_file_path=data_file_path,
            extract_query_template=extract_query_template
        )
        execute_query(con, query)

    close_database_connection(con)


def main():
    parser = argparse.ArgumentParser(description="CLI for Elt Extraction")
    parser.add_argument(
        "--locations_file_path",
        type=str,
        required=True,
        help="Path to locations JSON file",
    )

    parser.add_argument(
        "--start_data", type=str, required=True, help="Start date in YYYY-MM format"
    )

    parser.add_argument(
        "--end_date", type=str, required=True, help="End date in YYYY-MM format"
    )

    parser.add_argument(
        "--extract_query_template_path",
        type=True,
        required=True,
        help="Path to the SQL extraction query template",
    )

    parser.add_argument(
        "--database_path", type=str, required=True, help="Path to the database extraction query template",
    )

    parser.add_argument(
        "--source_base_path",
        type=True,
        required=True,
        help="Base path for the remote datafiles"    
    )

    args = parser.parse_args()
    extract_data(args)

if __name__ == "__main__":
    main()