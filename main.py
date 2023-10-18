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

import datetime
import time
import pygame.mixer as mixer
from modules.trainer import Trainer
from modules.poke_system import PokeSystem
from modules.database.db_manager import DAOManager
from modules.common_variables import (
    _B_WHITE, _F_RED, _I_START, _NO_COLOR, 
    load_file, poke_message, validate_input
)

__FILE = './assets/configs/pokemons_data.json'
__LOG = './assets/logs/pokemons_log.txt'
__GAME_SOUNDS = load_file(__FILE)
__BATTLE_S = __GAME_SOUNDS['battle_theme']
__INTRO_S = __GAME_SOUNDS['intro_theme']

def __show_menu():
    """
    The function displays a menu with two options and prompts the user to select one of them.
    :return: The function `show_menu()` returns the user's selected option (either 1 or 2) after
    validating the input.
    """
    message =\
        """
        1 - New Game
        2 - Show ranking
        """
    option = validate_input('^[1-2]{1}$', input(f'{message}\nselect: '), 0)
    return option

def __pokemon_game():
    """
    The function "pokemon_game" runs a game where the player battles against randomly assigned Pokemon.
    """
    try:
        
        mixer.init()
        sound = mixer.Sound(__INTRO_S)
        sound.set_volume(0.2)
        sound.play()
        poke_message('Hola entrenador/a, por favor dime tu nombre: ', 'info')
        
        trainer_name = validate_input('^[a-zA-Z0-9 _]+$', input(), 'Ash Ketchum')
        trainer_name = ' '.join([word.capitalize() for word in trainer_name.split(' ')])

        poke_message(f'Gracias {trainer_name}, te asignare 3 pokémones aleatorios para que puedas luchar.\nPresiona enter y empezemos!', 'success')
        _ = input()
        sound.stop()

        sound = mixer.Sound(__BATTLE_S)
        sound.set_volume(0.2)
        sound.play()
        
        sys_manager = PokeSystem(__FILE, __LOG)
        sys_manager.init_pokemons()
        dao_manager = DAOManager()
        pkm_trainer = Trainer(trainer_name)

        dao_manager.create_table()
        sys_manager.assign_init_pokemons(pkm_trainer)
        sys_manager.player_score = sys_manager.calculate_score(pkm_trainer)
        
        pkm_trainer.speak(f'{_B_WHITE}{_F_RED}', f'Hora del duelo Pokemon!', f'{_I_START}{_NO_COLOR}')
        pkm_trainer.next_pokemon()
        enemy_pokemon = sys_manager.next_pokemon() # Traigo al proximo pokemon para pelear
        still_can_fight = True
        time.sleep(2)
        while still_can_fight and sys_manager.pokemons:
            PokeSystem.clear_console()
            if not enemy_pokemon or not enemy_pokemon.has_hp():
                enemy_pokemon = sys_manager.next_pokemon()
            is_player_turn = sys_manager.attack_turn()
            PokeSystem.manage_game_turn(is_player_turn, pkm_trainer, enemy_pokemon)
            sys_manager.player_score = sys_manager.calculate_score(pkm_trainer)
            pkm_trainer.pokemon_in_battle = sys_manager.system_message(pkm_trainer, is_player_turn, pkm_trainer.pokemon_in_battle, enemy_pokemon)
            PokeSystem.reset_buff([pkm_trainer.pokemon_in_battle, enemy_pokemon])
            still_can_fight = pkm_trainer.check_win_or_lose()
            if still_can_fight:
                pkm_trainer.catch_if_pokeball(enemy_pokemon)
        pkm_trainer.check_status()
        sys_manager.player_score = sys_manager.calculate_score(pkm_trainer)
        sys_manager.show_score()
        dao_manager.insert_table(pkm_trainer, sys_manager)
        dao_manager.select_table(type='view')
        sound.stop()

    except Exception as e:
        message = f'{datetime.datetime.now()} - {e.args}'
        PokeSystem.write_file(sys_manager.log_path, 'a+', message)
        print(
            'Error al ejecutar la funcion principal',
            f'Exception: {e.__traceback__.tb_lineno}',
            f'Details: {e}',
            sep='\n')

def main_game() -> None:
    """
    The function presents a menu to the user and executes different actions based on their selection.
    """
    selected = __show_menu()
    match selected:
        case '1':
            __pokemon_game()
        case '2':
            dao_manager = DAOManager()
            dao_manager.select_table(type='view')
        case _:
            print('Error, please select between 1 or 2.')


if __name__ == '__main__':
    main_game()