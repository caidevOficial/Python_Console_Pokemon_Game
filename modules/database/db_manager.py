# GNU General Public License V3
#
# Copyright (C) <2022>  <Facundo Falcone> - Improvements
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import sqlite3 as db
from pandas import DataFrame
import pandas as pd
from modules.common_variables import load_configs
from modules.trainer import Trainer
from modules.poke_system import PokeSystem

class DAOManager:
    "Represents the DAO Manager, using SQLite"
    __result_from_query: list = list()
    def __init__(self) -> None:
        self.__db_configs = load_configs('./modules/configs.json')
        self.__db_name: str = self.__db_configs['name']
        self.__insert_deleting_before = self.__db_configs['delete_before_insert']
        self.__table: str = self.__db_configs['table_name']
        self.__db_output_file: str = self.__db_configs['paths']['db_file']
        self.__ddl_paths: dict = self.__db_configs['paths']['DDL']
        self.__dml_paths: dict = self.__db_configs['paths']['DML']


    def __open_query_file(self, query_path: str) -> str:
        """
        It opens a file, reads it, and returns the contents of the file
        
        :param query_path: The path to the query file
        :type query_path: str
        :return: The query file is being returned.
        """
        with open(query_path, 'r') as db_config:
            return db_config.read()

    def __execute_queries(self, queries: list[str], error_msg: str, success_msg: str, type: str = 'create') -> db.Cursor:
        """
        It executes a list of queries and returns the result of the last query executed
        
        :param queries: list[str] - a list of queries to be executed
        :type queries: list[str]
        :param error_msg: The error message to be displayed if the query fails
        :type error_msg: str
        :param success_msg: The message to be displayed when the query is executed successfully
        :type success_msg: str
        :param type: str = 'create', defaults to create
        :type type: str (optional)
        :return: The result of the query.
        """
        with db.connect(f'{self.__db_output_file}') as conection:
            try:
                if queries:
                    rows_amount = 0
                    for query in queries:
                        result = conection.execute(query)
                        if result and result.rowcount > 0:
                            rows_amount += result.rowcount
                    conection.commit()
                    if result and result.rowcount > 0:
                        print(f'>> {success_msg}')
                        if not type == 'create':
                            print(f'>> System: {rows_amount} rows affected')
                    return result
                else: print(f">> System: There isn't query to execute")
            except db.OperationalError as oe:
                print(f'>> System: {error_msg}', oe)

    def __replace_table_name(self, query: str) -> str:
        """
        It takes a query string and replaces the string 'T_NAME' with the name of the table
        
        :param query: The query to be executed
        :type query: str
        :return: The query is being returned with the table name replaced.
        """
        return query.replace('T_NAME', self.__table)
    
    def __re_do_table(self) -> None:
        """
        It drops the table and then creates it again
        """
        self.drop_table()
        self.create_table()

    def create_table(self) -> None:
        """
        It opens a file, reads the contents, replaces a string in the contents, and then executes the
        query creating the table if not exists.
        """
        query = self.__replace_table_name(self.__open_query_file(self.__ddl_paths['create']))
        self.__execute_queries([query], 'Table already exists', f'Table {self.__table} created successfully')
    
    def insert_table(self, trainer: Trainer, poke_sys: PokeSystem) -> None:
        if self.__insert_deleting_before:
            self.__re_do_table()
        query = self.__replace_table_name(self.__open_query_file(self.__dml_paths['insert']))
        to_replace = re.findall("1_.", query)
        elements = [
            trainer.name, trainer.status, 
            len(trainer.defeated_pokemons) + len(trainer.pokemons), 
            poke_sys.player_score]
        queries = list[str]()
        query_replaced = self.__create_insert_query(to_replace, elements, query)
        queries.append(query_replaced)
        self.__execute_queries(queries, 'Error adding the data', 'Data inserted successfully', type='insert')
    
    def __create_insert_query(self, to_replace: list[str], replacement: list, query_base: str) -> str:
        """
        It takes a list of strings and a tuple of strings and replaces the strings in the list with the
        strings in the tuple in a given string
        
        :param to_replace: list of strings to be replaced in the query
        :param replacement: list with the values to replace in the query
        :param query_base: The base query that will be used to create the insert query by replacing its values
        :return: The query with all the values replaced to be executed.
        """
        query_replaced = query_base
        for i in range(len(replacement)):
            query_replaced = query_replaced.replace(to_replace[i], f'{replacement[i]}')
        return query_replaced

    def delete_table(self) -> None:
        """
        It opens a file, reads the contents of the file, replaces the table name in the file with the
        table name provided by the user, executes the query and prints a message
        """
        query = self.__replace_table_name(self.__open_query_file(self.__dml_paths['delete']))
        self.__execute_queries([query], 'Error deleting the table', f'Table {self.__table} deleted successfully', type='delete')
    
    def drop_table(self) -> None:
        """
        It opens a file, reads the contents of the file, replaces the table name in the file with the
        table name of the class, and then executes the query
        """
        query = self.__replace_table_name(self.__open_query_file(self.__ddl_paths['drop']))
        self.__execute_queries([query], 'Error dropping the table', f'Table {self.__table} dropped successfully', type='drop')
    
    def __create_df(self, columns: list, data: list[tuple]) -> pd.DataFrame:
        """
        This function creates a pandas DataFrame from a list of columns and data.
        
        :param columns: A list of column names for the DataFrame
        :param data: A list of tuples where each tuple represents a row of data for the DataFrame. The
        length of each tuple should match the number of columns specified in the 'columns' parameter
        :return: a pandas DataFrame object created from the input columns and data.
        """
        db_df = DataFrame(data, columns=columns)
        return db_df
    
    def __query_select(self) -> db.Cursor:
        """
        This function executes a select query on a database table and returns the result as a cursor
        object.
        :return: a database cursor object.
        """
        query = self.__replace_table_name(self.__open_query_file(self.__dml_paths['select']))
        result = self.__execute_queries([query], 'Error getting the table info', f'Table {self.__table} read successfully', type='select')
        return result
    
    def __select_to_df(self) -> pd.DataFrame:
        """
        This function executes a SELECT query, retrieves the result, and returns it as a pandas
        DataFrame.
        :return: A pandas DataFrame is being returned.
        """
        self.__result_from_query = self.__query_select()
        query = self.__replace_table_name(self.__open_query_file(self.__dml_paths['select']))
        result = self.__execute_queries([query], 'Error getting the table info', f'Table {self.__table} read successfully', type='select')
        fields = [field[0] for field in result.description]
        return self.__create_df(fields, self.__result_from_query.fetchall())
    
    def select_table(self) -> DataFrame:
        """
        This function prints the result of selecting data from a database table as a pandas DataFrame.
        """
        print(
            "Players ordered by score DESC:",
            self.__select_to_df(), sep='\n')
