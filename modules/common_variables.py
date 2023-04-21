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
    with open(path, 'r', encoding='utf-8') as archivo:
        return dict(json.load(archivo)['sounds'])