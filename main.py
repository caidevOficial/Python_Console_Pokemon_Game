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
from modules.poke_system import Sistema
from modules.common_variables import (
    _b_white, _f_red, _i_start, _no_color
)

FILE = './assets/configs/pokemons_data.json'
LOG = './assets/logs/pokemons_log.txt'
SOUND = './assets/music/battle.mp3'


def pokemon_game():
    try:
        mixer.init()
        mixer.Sound.play(mixer.Sound(SOUND))

        sys_manager = Sistema(FILE, LOG)
        sys_manager.init_pokemons()
        pkm_trainer = Trainer('Ash Ketchum')

        sys_manager.assign_init_pokemons(pkm_trainer)
        sys_manager.player_score = sys_manager.calculate_score(pkm_trainer)
        
        pkm_trainer.speak(f'{_b_white}{_f_red}', f'Hora del duelo Pokemon!', f'{_i_start}{_no_color}')
        pkm_trainer.next_pokemon()
        enemy_pokemon = sys_manager.next_pokemon() # Traigo al proximo pokemon para pelear
        still_can_fight = True
        time.sleep(2)
        while still_can_fight and sys_manager.pokemons:
            Sistema.clear_console()
            if not enemy_pokemon or not enemy_pokemon.has_hp():
                enemy_pokemon = sys_manager.next_pokemon()
            is_player_turn = sys_manager.attack_turn()
            Sistema.manage_game_turn(is_player_turn, pkm_trainer, enemy_pokemon)
            sys_manager.player_score = sys_manager.calculate_score(pkm_trainer)
            pkm_trainer.pokemon_in_battle = sys_manager.system_message(pkm_trainer, is_player_turn, pkm_trainer.pokemon_in_battle, enemy_pokemon)
            Sistema.reset_buff([pkm_trainer.pokemon_in_battle, enemy_pokemon])
            still_can_fight = pkm_trainer.check_win_or_lose()
            if still_can_fight:
                pkm_trainer.catch_if_pokeball(enemy_pokemon)
        pkm_trainer.check_status()
        sys_manager.player_score = sys_manager.calculate_score(pkm_trainer)
        sys_manager.show_score()

    except Exception as e:
        message = f'{datetime.datetime.now()} - {e.args}'
        Sistema.write_file(sys_manager.log_path, 'a+', message)
        print(
            'Error al ejecutar la funcion principal',
            f'Exception: {e.__traceback__.tb_lineno}',
            f'Details: {e}',
            sep='\n')


if __name__ == '__main__':
    pokemon_game()