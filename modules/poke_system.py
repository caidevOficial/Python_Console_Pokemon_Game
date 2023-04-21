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
import json
import os
import random
import time

from modules.pokemon import Pokemon
from modules.trainer import Trainer

from modules.common_variables import (
    _B_GREEN, _B_BLUE, _B_RED, 
    _F_BLACK, _F_WHITE, _NO_COLOR
)

class PokeSystem:
    _log_path: str = ''
    _filename: str = ''
    _wild_pokemones: list[Pokemon] = None
    _player_score: int = 0

    def __init__(self, file_path: str, log_path: str):
        self._filename = file_path
        self._log_path = log_path
        self._wild_pokemones = list[Pokemon]()

    @property
    def log_path(self) -> str:
        return self._log_path

    @property
    def pokemons(self) -> list[Pokemon]:
        return self._wild_pokemones
    
    @property
    def player_score(self) -> int:
        return self._player_score

    @log_path.setter
    def log_path(self, path: str) -> None:
        self._log_path = path

    @pokemons.setter
    def pokemons(self, pokemons: list[Pokemon]) -> None:
        self._wild_pokemones = pokemons.copy()
    
    @player_score.setter
    def player_score(self, puntos: int) -> None:
        self._player_score = puntos

    def calculate_score(self, pkm_trainer: Trainer = None) -> int:
        puntos = self.player_score
        if not puntos:
            puntos = 10 * len(pkm_trainer.pokemons)
        elif pkm_trainer.pokemon_in_battle or pkm_trainer.pokemons:
            puntos += pkm_trainer.pokemon_in_battle.effectivity
        elif pkm_trainer.pokemons:
            pass
        else:
            puntos += (-4 * len(pkm_trainer.defeated_pokemons))
        return puntos
    
    @staticmethod 
    def load_file(path: str) -> list[dict]:
        with open(path, 'r', encoding='utf-8') as archivo:
            return list[dict](json.load(archivo)['pokemons'])
    
    @staticmethod
    def write_file(path: str, mode: str, message: str) -> bool:
        success = False
        with open(path, mode) as archivo:
            archivo.write(f'{message}\n')
            success = True
        return success

    @staticmethod
    def parse_objects(pokemons: list[dict]) -> list[Pokemon]:
        lista_pokemones_o = list[Pokemon]()
        for pokemon in pokemons:
            actual_poke = Pokemon(
                pokemon['id'], pokemon['poder'], pokemon['nombre'].capitalize(),
                pokemon['icon'], pokemon['icon_element'], pokemon['tipo'],
                pokemon['evoluciones'], pokemon['debilidad'],
                pokemon['fortaleza'], pokemon['ataques']
            )
            lista_pokemones_o.insert(0, actual_poke)
        return lista_pokemones_o

    def init_pokemons(self):
        try:
            self.pokemons = PokeSystem.parse_objects(
                PokeSystem.load_file(
                    self._filename
                )
            )
            print(f'Sistema: {len(self.pokemons)} Pokemones salvajes encontrados!')
        except Exception as e:
            message = f'{datetime.datetime.now()} - {e.args}'
            PokeSystem.write_file(self.log_path, 'a+', message)
            print(
                'Error al inicializar pokemones',
                f'Exception: {e.args}',
                sep='\n')

    def next_pokemon(self) -> Pokemon | bool:
        """
        It returns the first pokemon in the list of pokemones, or False if the list is empty
        :return: The first element of the list.
        """
        try:
            if self.pokemons:
                return self.pokemons.pop(0)
            raise IndexError
        except Exception as e:
            message = f'{datetime.datetime.now()} - {e.args}'
            PokeSystem.write_file(self.log_path, 'a+', message)
            print(
                'Error Al cargar pokemones',
                f'Exception: {e.args}',
                sep='\n')
            return None
    
    def attack_turn(self):
        turnos = [True, False]
        return random.choice(turnos)

    def system_message(self, pkm_trainer: Trainer, turno: bool, poke_a: Pokemon, poke_b: Pokemon) -> Pokemon | None:
        try:
            if poke_a and poke_b:
                if turno:
                    attack_message = f'>>⬆️  {_B_GREEN}{_F_BLACK}{poke_a.name} uso {poke_a.current_attack} contra {poke_b.name} enemigo y causo {poke_a.dmg_current_attack} daño{_NO_COLOR} {poke_a.efectivity_message}'
                    #poke_b.restar_vida(int(poke_a.dmg_ataque_actual*1.5))
                else:
                    attack_message = f'>>⬇️  {_B_RED}{_F_WHITE}{poke_b.name} enemigo uso {poke_b.current_attack} contra {poke_a.name} y causo {poke_b.dmg_current_attack} daño{_NO_COLOR} {poke_b.efectivity_message}'
                    #poke_a.restar_vida(int(poke_b.dmg_ataque_actual*0.5))
                consola =\
                """
                Pokemon Actual: {7} {8} {9}             Puntaje: {10}
                Restantes: {5:02d}
                Pokemones: {6}
                {0}
                    Tu Pokemon: {1:10s}                 Enemigo:{2:10s}
                    HP: {3:06.2f}                              HP: {4:06.2f}
                """.format(attack_message, poke_a.name, poke_b.name, poke_a.hp, poke_b.hp, len(pkm_trainer.pokemons),
                ' | '.join([x.name for x in pkm_trainer.pokemons]), poke_a.name, poke_a.icon, poke_a.icon_el, self.player_score)
                print(consola)

                if not poke_a.has_hp():
                    poke_a.check_faint()
                    pkm_trainer.return_to_pokeball(poke_a)
                    poke_a = None

                poke_b.check_faint()
                time.sleep(1)
                # os.system('cls')
                return poke_a
        except Exception as e:
            message = f'{datetime.datetime.now()} - {e.args}'
            PokeSystem.write_file(PokeSystem.log_path, 'a+', message)
            print(
                'Error Al mostrar mensaje de batalla',
                f'Exception: {e.args}',
                sep='\n')
        

    @staticmethod
    def manage_game_turn(
        turno: bool, pkm_trainer: Trainer, poke_enemy: Pokemon):
        try:
            match turno:
                case True:
                    if pkm_trainer.pokemon_in_battle and pkm_trainer.pokemon_in_battle.has_hp():
                        pokebola_lanzada = random.choice([True, False]) # veo si lanzo la pokebola o no
                        pkm_trainer.pokeball_threw = pokebola_lanzada # Actualizo si lanze la pokebola o no
                        pkm_trainer.pokemon_in_battle.continue_battle(poke_enemy) # Ataco
                    elif not pkm_trainer.pokemon_in_battle:
                        pkm_trainer.next_pokemon()
                case False:
                    if not pkm_trainer.pokemon_in_battle:
                        pkm_trainer.next_pokemon()
                    if pkm_trainer.pokemon_in_battle and pkm_trainer.pokemon_in_battle.has_hp() and poke_enemy.has_hp():
                        poke_enemy.continue_battle(pkm_trainer.pokemon_in_battle) # Me ataca
        except Exception as e:
            message = f'{datetime.datetime.now()} - {e.args}'
            PokeSystem.write_file(PokeSystem.log_path, 'a+', message)
            print(
                'Error Al Gestionar turnos de jugador o enemigo',
                f'Exception: {e.args}',
                sep='\n')
            return None
    
    def assign_init_pokemons(self, pkm_trainer: Trainer) -> None:
        for _ in range(3):
            pkm_trainer.pokemons.append(
                self.pokemons.pop(
                    self.pokemons.index(
                        random.choice(
                            self.pokemons
                        )
                    )
                )
            )
    
    @staticmethod
    def reset_buff(pokemons: list[Pokemon]) -> None:
        for poke in pokemons:
            if poke:
                poke.dmg_current_attack = 0
                poke.efectivity_message = ''
                poke.effectivity = 0
                poke.is_critical_damage = False
    
    def show_score(self) -> None:
        mensaje =\
        """
        {0}{1}Puntaje Final: {2:4d}{3}
        """.format(_B_BLUE, _F_WHITE, self.player_score, _NO_COLOR)
        print(mensaje)
    
    @staticmethod
    def clear_console() -> None:
        os.system('cls')
