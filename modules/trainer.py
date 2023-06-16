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

from copy import deepcopy
import os
import time
from modules.pokemon import Pokemon
from modules.common_variables import (
    _B_GREEN, _B_BLUE, _B_RED, _B_WHITE, _F_BLACK, 
    _F_RED, _F_WHITE, _I_LOSE, _I_WIN, _NO_COLOR
)

class Trainer:
    """
    The Trainer class is a class that represents a trainer in the Pokemon game
    """
    _current_pokemon: Pokemon = None
    _pokemons: list[Pokemon] = None
    _defeated_pokemons: list[Pokemon] = None
    _name: str = None
    _throw_pokeball: bool = False

    def __init__(self, trainer_name: str):
        """
        This is a constructor function for a class that initializes the name, list of pokemons, and list
        of defeated pokemons.
        
        :param trainer_name: The parameter "trainer_name" is a string that represents the name of an object being
        initialized. In this case, it is used to set the name of an instance of a class
        """
        self.name = trainer_name
        self._pokemons = list[Pokemon]()
        self._defeated_pokemons = list[Pokemon]()

    @property
    def pokemon_in_battle(self) -> Pokemon:
        """
        It returns the current pokemon in battle.
        :return: The current pokemon in battle.
        """
        return self._current_pokemon

    @property
    def pokeball_threw(self) -> bool:
        """
        This function returns a boolean value of whether or not the pokeball was thrown
        :return: The pokeball_threw method returns a boolean value.
        """
        return self._throw_pokeball

    @property
    def name(self) -> str:
        """
        It returns the name of the object.
        :return: The name of the person
        """
        return self._name

    @property
    def pokemons(self) -> list[Pokemon]:
        """
        It returns a list of Pokemon objects.
        :return: A list of Pokemon objects.
        """
        return self._pokemons

    @property
    def defeated_pokemons(self) -> list[Pokemon]:
        """
        This function returns a list of defeated Pokemons.
        :return: The method `defeated_pokemons` is returning a list of `Pokemon` objects, which is the
        list of defeated pokemons.
        """
        return self._defeated_pokemons

    @pokemon_in_battle.setter
    def pokemon_in_battle(self, poke_batalla: Pokemon) -> Pokemon:
        """
        It sets the current pokemon to the pokemon in battle.
        
        :param poke_batalla: Pokemon
        """
        self._current_pokemon = poke_batalla

    @pokeball_threw.setter
    def pokeball_threw(self, lanzada: bool) -> None:
        """
        The pokeball_threw function takes in a boolean value and sets the value of the _throw_pokeball
        attribute to the value of the lanzada parameter
        
        :param lanzada: bool
        """
        self._throw_pokeball = lanzada

    @name.setter
    def name(self, trainer_name: str) -> None:
        """
        This function takes a string as an argument and assigns it to the _name attribute of the object
        
        :param trainer_name: str
        """
        self._name = trainer_name

    @pokemons.setter
    def pokemons(self, pokes: list[Pokemon]) -> None:
        """
        This function takes a list of Pokemon objects and sets the pokemons attribute of the Trainer
        object to a copy of the list
        
        :param pokes: list[Pokemon]
        """
        self._pokemons = pokes.copy()

    @defeated_pokemons.setter
    def defeated_pokemons(self, pokes: list[Pokemon]) -> None:
        """
        This function takes a list of Pokemon objects and sets the defeated_pokemons attribute of the
        Trainer object to a copy of the list
        
        :param pokes: list[Pokemon]
        """
        self._defeated_pokemons = pokes.copy()

    def speak(self, color_code_init: str, mensaje: str, color_code_end: str) -> None:
        """
        `speak()` is a function that takes in three arguments: `self`, `color_code_init`, and `mensaje`,
        and returns `None`
        
        :param color_code_init: The color code to start the message with
        :param mensaje: str = The message you want to print
        :param color_code_end: str = '\033[0m'
        """
        trainer_text = f'\n{color_code_init}{self.name}: {mensaje}{color_code_end}'
        print(trainer_text)

    def throw_pokeball(self) -> bool:
        """
        If the trainer hasn't thrown a pokeball, then throw a pokeball
        :return: the value of the attribute lanzo_pokebola.
        """
        if not self.pokeball_threw:
            self.pokeball_threw = True
        return self.pokeball_threw

    def check_pokeball(self) -> bool:
        """
        This function checks if the pokeball was thrown
        :return: The pokeball_threw variable is being returned.
        """
        return self.pokeball_threw

    def try_catch_pokemon(self, pokemon: Pokemon)-> None:
        """
        If the pokemon has no life, then catch it
        
        :param pokemon: Pokemon
        """
        if not pokemon.has_hp():
            self.catch_pokemon(pokemon)
            print(f'{_B_GREEN}{_F_BLACK}Felicidades! Atrapaste un {pokemon.name}!{_NO_COLOR}\n')

    def catch_if_pokeball(self, pokemon: Pokemon) -> None:
        """
        If the player has a pokeball, then try to catch the pokemon
        
        :param pokemon: Pokemon
        """
        if self.check_pokeball(): # Chequeo si lanze pokebola o no
            self.try_catch_pokemon(deepcopy(pokemon))

    def catch_pokemon(self, poke: Pokemon) -> bool:
        """
        It tries to heal the pokemon, then append it to the trainer's list of pokemons, and then it
        prints a message saying that the pokemon was caught. If it fails to heal the pokemon, it prints
        a message saying that the pokemon was not caught
        
        :param poke: Pokemon
        :return: The return value is a boolean.
        """
        try:
            poke.heal()
            self.pokemons.append(poke)
            self.speak(f'{_B_GREEN}{_F_BLACK}', f'Atrape a un {poke.name}!!', f'{_NO_COLOR}')
            return True
        except Exception as e:
            self.speak(f'{_B_RED}{_F_WHITE}', f'Falle al Atrapar a {poke.name}', f'{_NO_COLOR}')
            return False

    def check_pokemons(self) -> None:
        """
        It prints the name of the trainer and the name of the pokemon, and the HP of the pokemon
        """
        if self.pokemons:
            self.speak(f'{_B_BLUE}{_F_WHITE}','Mis pokemones son:', f'{_NO_COLOR}')
            for pokemon in self.pokemons:
                print(f'{self.name}: {pokemon.name} con {pokemon.hp} de HP.')
        if self.defeated_pokemons:
            self.speak(f'{_B_BLUE}{_F_WHITE}','Mis pokemones derrotados son:', f'{_NO_COLOR}')
            for pokemon_v in self.defeated_pokemons:
                print(f'{self.name}: {pokemon_v.name} con {pokemon_v.hp} de HP.')

    def next_pokemon(self):
        """
        It takes the first pokemon from the list of pokemons and assigns it to the pokemon_in_battle
        attribute
        """
        try:
            if self.pokemons:
                pokemon = self.pokemons.pop(0)
                if pokemon:
                    message =\
                    f"""
                                    {_B_BLUE}{_F_WHITE} {self.name}: {pokemon.name}, yo te elijo! 👉🏼⛔{_NO_COLOR}
                    """
                    os.system('cls')
                    print(message)
                    time.sleep(2)
                    #self.hablar(f'')
                    self.pokemon_in_battle = pokemon
            else:
                raise IndexError
        except Exception as e:
            print(
                'No te quedan mas pokemones, volve a pueblo paleta.',
                f'Exception: {e}',
                sep='\n')

    def return_to_pokeball(self, pokemon: Pokemon) -> None:
        """
        It takes a pokemon object as an argument and adds it to the defeated_pokemons list
        
        :param pokemon: Pokemon
        """
        self.speak('', f'{pokemon.name}, peleaste bien, regresa a tu pokebola!', '')
        self.defeated_pokemons.append(deepcopy(pokemon))

    def check_win_or_lose(self) -> bool:
        """
        If the player has any pokemon in their party or in battle, they can continue playing
        :return: a boolean value.
        """
        can_continue = False
        if self.pokemons or self.pokemon_in_battle:
            can_continue = True
        return can_continue

    def check_status(self) -> None:
        """
        If the player has any pokemons or is in a battle, they win the game. If not, they lose
        """
        if self.pokemons or self.pokemon_in_battle:
            self.speak(f'{_B_WHITE}{_F_RED}', 'Gane la liga pokemon!', f'{_I_WIN}{_NO_COLOR}')
            if self.pokemon_in_battle:
                self.pokemons.insert(0, deepcopy(self.pokemon_in_battle))
        else:
            self.speak(f'{_B_RED}{_F_WHITE}','Me quede sin pokemones!', f'{_NO_COLOR}{_I_LOSE}')
        self.check_pokemons()
