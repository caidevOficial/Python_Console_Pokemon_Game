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
        """
        This is the initialization function for a class that takes in a file path, log path, and creates
        an empty list for wild Pokemon.
        
        :param file_path: A string representing the file path of a file that contains data about Pokemon
        :param log_path: The `log_path` parameter is a string that represents the file path where the
        log file will be saved. This log file will contain information about the program's execution and
        any errors that may occur
        """
        self._filename = file_path
        self._log_path = log_path
        self._wild_pokemones = list[Pokemon]()

    @property
    def log_path(self) -> str:
        """
        This function returns the log path as a string.
        :return: The method `log_path` is returning a string which is the value of the private attribute
        `_log_path`.
        """
        return self._log_path

    @property
    def pokemons(self) -> list[Pokemon]:
        """
        This function returns a list of wild Pokemon.
        :return: A list of Pokemon objects is being returned. The method `pokemons` returns the private
        attribute `_wild_pokemones` of the class, which is a list of Pokemon objects.
        """
        return self._wild_pokemones
    
    @property
    def player_score(self) -> int:
        """
        This function returns the player's score as an integer.
        :return: the player's score as an integer.
        """
        return self._player_score

    @log_path.setter
    def log_path(self, path: str) -> None:
        """
        This function sets the log path for a class instance.
        
        :param path: The "path" parameter is a string that represents the file path where the log file
        will be stored. The method "log_path" sets the value of the instance variable "_log_path" to the
        value of the "path" parameter
        :type path: str
        """
        self._log_path = path

    @pokemons.setter
    def pokemons(self, pokemons: list[Pokemon]) -> None:
        """
        This function sets the list of wild pokemons for a given object.
        
        :param pokemons: The "pokemons" parameter is a list of objects of the class "Pokemon". This
        method is a part of a class and it takes a list of Pokemon objects as input. The method then
        creates a copy of this list and assigns it to the instance variable "_wild_pokemones"
        :type pokemons: list[Pokemon]
        """
        self._wild_pokemones = pokemons.copy()
    
    @player_score.setter
    def player_score(self, score: int) -> None:
        """
        This function sets the score of a player object.
        
        :param score: The "score" parameter is an integer that represents the score of a player. This
        function sets the player's score to the value of the "score" parameter
        :type score: int
        """
        self._player_score = score
    
    def __normalize_score(self, score: int) -> int:
        """
        This function normalizes a score by returning the score if it is greater than or equal to 0,
        otherwise it returns 0.
        
        :param score: The input parameter "score" is an integer value representing a score
        :return: The function `__normalize_score` takes an integer `score` as input and returns an
        integer. If the input `score` is greater than or equal to 0, the function returns the input
        `score`. Otherwise, it returns 0.
        """
        return score if score >= 0 else 0

    def calculate_score(self, pkm_trainer: Trainer = None) -> int:
        """
        This function calculates the score of a Pokemon trainer based on their number of Pokemon,
        effectiveness in battle, and number of defeated Pokemon.
        
        :param pkm_trainer: The pkm_trainer parameter is an instance of the Trainer class, which
        represents a trainer in the game who has a collection of pokemons and can battle with other
        trainers. The method is calculating a score for the player based on the number of pokemons they
        have, the effectiveness of their current pokemon
        :return: an integer value, which is the calculated score based on the given conditions and
        inputs.
        """
        score = self.player_score
        if not score:
            score = 10 * len(pkm_trainer.pokemons)
        elif pkm_trainer.pokemon_in_battle or pkm_trainer.pokemons:
            score += pkm_trainer.pokemon_in_battle.effectivity
        elif pkm_trainer.pokemons:
            pass
        else:
            score -= (2 * len(pkm_trainer.defeated_pokemons))
        return self.__normalize_score(score)
    
    @staticmethod 
    def load_file(path: str) -> list[dict]:
        """
        This function loads a JSON file containing information about pokemons and returns a list of
        dictionaries representing each pokemon.
        
        :param path: The path parameter is a string that represents the file path of the JSON file that
        contains information about pokemons
        :return: a list of dictionaries containing information about pokemons. The information is being
        loaded from a JSON file located at the specified path.
        """
        with open(path, 'r', encoding='utf-8') as archivo:
            return list[dict](json.load(archivo)['pokemons'])
    
    @staticmethod
    def write_file(path: str, mode: str, message: str) -> bool:
        """
        This function writes a message to a file specified by its path and mode and returns a boolean
        indicating whether the operation was successful or not.
        
        :param path: The path parameter is a string that represents the file path where the message will
        be written
        param mode: The mode parameter in the write_file function specifies the mode in which the file
        is opened. It can be 'w' for write mode, 'a' for append mode, 'x' for exclusive creation mode,
        'r' for read mode, and more. The mode parameter determines how the file
        :param message: The message parameter is a string that contains the text that will be written to
        the file
        :return: a boolean value indicating whether the file write operation was successful or not.
        """
        success = False
        with open(path, mode, encoding='utf-8', newline='\n') as archivo:
            archivo.write(f'{message}')
            success = True
        return success

    @staticmethod
    def parse_objects(pokemons: list[dict]) -> list[Pokemon]:
        """
        The function takes a list of dictionaries representing Pokemon and returns a list of Pokemon
        objects with the data from the dictionaries.
        
        :param pokemons: A list of dictionaries representing Pokemon objects. Each dictionary contains
        the following keys: 'id', 'poder', 'nombre', 'icon', 'icon_element', 'tipo', 'evoluciones',
        'debilidad', 'fortaleza', and 'ataques'
        :return: a list of Pokemon objects.
        """
        lista_pokemones_o = list[Pokemon]()
        for pokemon in pokemons:
            actual_poke = Pokemon(
                pokemon['id'], pokemon['poder'], str(pokemon['nombre']).capitalize(),
                pokemon['icon'], pokemon['icon_element'], pokemon['tipo'],
                pokemon['evoluciones'], pokemon['debilidad'],
                pokemon['fortaleza'], pokemon['ataques']
            )
            lista_pokemones_o.insert(0, actual_poke)
        return lista_pokemones_o

    def init_pokemons(self):
        """
        This function initializes a list of pokemons by parsing objects from a file and logs any errors
        encountered.
        """
        try:
            self.pokemons = PokeSystem.parse_objects(
                PokeSystem.load_file(
                    self._filename
                )
            )
            random.shuffle(self.pokemons)
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
        This function returns the first element of a list of Pokemon objects or False if the list is
        empty, and logs any errors that occur.
        :return: either the first Pokemon object in the list of pokemons or False if the list is empty.
        If an error occurs, it returns None.
        """
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
        """
        The function randomly chooses whether it is the player's or the opponent's turn to attack.
        :return: a randomly chosen boolean value from the list `turnos`, which contains the values
        `True` and `False`.
        """
        turns = [True, False]
        return random.choice(turns)

    def system_message(self, pkm_trainer: Trainer, turno: bool, poke_a: Pokemon, poke_b: Pokemon) -> Pokemon | None:
        """
        This function displays a message during a Pokemon battle and returns the Pokemon that fainted,
        if any.
        
        :param pkm_trainer: The trainer object that is participating in the battle
        :param turno: The "turno" parameter is a boolean value that indicates whether it is the player's
        turn to attack or the opponent's turn
        :param poke_a: The first Pokemon involved in the battle
        :param poke_b: The parameter `poke_b` is a variable representing a Pokemon object that is being
        targeted by an attack in a battle
        :return: either a Pokemon object or None.
        """
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
                return poke_a
        except Exception as e:
            message = f'{datetime.datetime.now()} - {e.args}'
            PokeSystem.write_file(PokeSystem.log_path, 'a+', message)
            print(
                'Error Al mostrar mensaje de batalla',
                f'Exception: {e.args}',
                sep='\n')
        

    @staticmethod
    def manage_game_turn(turno: bool, pkm_trainer: Trainer, poke_enemy: Pokemon):
        """
        This function manages the turns of a game between a player's Pokemon and an enemy Pokemon.
        
        :param turno: boolean variable indicating whether it is the player's turn (True) or the enemy's
        turn (False)
        :param pkm_trainer: Trainer object representing the player's trainer
        :param poke_enemy: The Pokemon that the player is currently battling against
        :return: None.
        """
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
        """
        This function assigns three random pokemons from a list to a trainer's list of pokemons.
        
        :param pkm_trainer: The parameter `pkm_trainer` is of type `Trainer`, which is presumably a
        class representing a Pokemon trainer
        :type pkm_trainer: Trainer
        """
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
        """
        The function resets the damage, effectiveness message, effectiveness value, and critical damage
        status of all Pokemon in a given list.
        
        :param pokemons: a list of Pokemon objects that we want to reset the damage, effectiveness, and
        critical damage for
        """
        for poke in pokemons:
            if poke:
                poke.dmg_current_attack = 0
                poke.efectivity_message = ''
                poke.effectivity = 0
                poke.is_critical_damage = False
    
    def show_score(self) -> None:
        """
        This function prints the final score of a player in a formatted message.
        """
        message =\
        """
        {0}{1}Puntaje Final: {2:4d}{3}
        """.format(_B_BLUE, _F_WHITE, self.player_score, _NO_COLOR)
        print(message)
    
    @staticmethod
    def clear_console() -> None:
        """
        This function clears the console screen in Python.
        """
        if os.name in ['ce', 'nt', 'dos']: os.system("cls")
        else: os.system("clear")
