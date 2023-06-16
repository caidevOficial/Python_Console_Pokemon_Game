# MIT License
#
# Copyright (c) 2023 [FacuFalcone] All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import re

_B_RED: enumerate = '\033[41m'
_B_GREEN: enumerate = '\033[42m'
_B_BLUE: enumerate = '\033[44m'
_B_WHITE: enumerate = '\033[47m'
_F_RED: enumerate = '\033[1;31m'
_F_WHITE: enumerate = '\033[37m'
_F_BLACK: enumerate = '\033[30m'
_NO_COLOR: enumerate = '\033[0m'
_I_WIN: enumerate = '🎉'
_I_LOSE: enumerate = '😵‍💫💀☠️'
_I_START: enumerate = '🦾😎'

def load_file(path: str) -> dict:
    """
    This function loads a JSON file from a given path and returns a dictionary containing the 'sounds'
    key from the file.
    
    :param path: The path parameter is a string that represents the file path of the JSON file that
    contains the data to be loaded
    :return: A dictionary containing the 'sounds' data from a JSON file located at the specified path.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return dict(json.load(file)['sounds'])

def validate_input(input: str) -> str:
    """
    This function validates if the input string contains only alphanumeric characters, spaces, and
    underscores, and returns the input if it does, otherwise returns 'Ash Ketchum'.
    
    :param input: A string that needs to be validated
    :type input: str
    :return: If the input string contains only letters, numbers, spaces, and underscores, it will return
    the input string. Otherwise, it will return the string 'Ash Ketchum'.
    """
    if re.match('^[a-zA-Z0-9 _]+$', input):
        return input
    return 'Ash Ketchum'

def poke_message(message: str, message_type: str) -> None:
    """
    This is a Python function that prints messages with different colors and message types (error,
    success, information).
    
    :param message: A string containing the message to be displayed
    :param message_type: A string indicating the type of message being passed (e.g. "Error",
    "Success", "Info")
    """
    _b_red: str = '\033[41m'
    _b_green: str = '\033[42m'
    _b_blue: str = '\033[44m'
    _f_white: str = '\033[37m'
    _no_color: str = '\033[0m'
    message_type = message_type.strip().capitalize()
    match message_type:
        case 'Error':
            print(f'{_b_red}{_f_white}> Error: {message}{_no_color}')
        case 'Success':
            print(f'{_b_green}{_f_white}> Success: {message}{_no_color}')
        case 'Info':
            print(f'{_b_blue}{_f_white}> Information: {message}{_no_color}')

def load_configs(path: str) -> dict:
    """
    This function loads a dictionary of database configurations from a JSON file located at the given
    path.
    
    :param path: The path parameter is a string that represents the file path of the JSON file
    containing the database configurations
    :type path: str
    :return: A dictionary containing the database configurations loaded from a JSON file located at the
    specified path.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return dict(json.load(file)['database'])