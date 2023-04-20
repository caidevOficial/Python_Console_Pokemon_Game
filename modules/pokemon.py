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

import random
from modules.common_variables import (
    _b_green, _b_blue, _b_red, _b_white,
    _f_black, _f_red, _f_white, _i_lose, _i_start,
    _i_win, _no_color
)

class Pokemon:
    """
    The Pokemon class is a class that represents a pokemon in the Pokemon game
    """
    _MIN_HP: int = 50
    _MAX_HP: int = 250
    _id: int = None
    _power: int = None
    _life: float = 0
    _name: str = None
    _icon: bytes = None
    _icon_el: bytes = None
    _types: list[str] = None
    _evolutions: list[str] = None
    _weakness: list[str] = None
    _strenghts: list[str] = None
    _attacks: list[str] = None
    _current_attack: str = ''
    _attack_damage: int = 0
    _msg_efectivity: str = ''
    _effectivity: int = 0
    _critical_hit: bool = False

    def __init__(self, pkm_id: int, pkm_power: int, pkm_name: str, pkm_icon: bytes, pkm_icon_el: bytes, 
                pkm_types: list[str], pkm_evolutions: list[str], pkm_weakness: list[str], pkm_strenghts: list[str], 
                pkm_attacks: list[str]) -> None:
        """
        This function is a constructor for the Pokemon class. It takes in the following parameters:
        pkm_id, pkm_power, pkm_name, pkm_icon, pkm_icon_el, pkm_types, pkm_evolutions, pkm_weakness,
        pkm_strenghts, pkm_attacks. It returns None
        
        :param pkm_id: The ID of the pokemon
        :param pkm_power: The power of the pokemon
        :param pkm_name: The name of the pokemon
        :param pkm_icon: The icon of the pokemon
        :param pkm_icon_el: The icon of the pokemon, but with the background removed
        :param pkm_types: list[str]
        :param pkm_evolutions: list[str]
        :param pkm_weakness: list[str]
        :param pkm_strenghts: list[str]
        :param pkm_attacks: list[str]
        """
        self.set_hp()
        self.id = pkm_id
        self.power = pkm_power
        self.name = pkm_name
        self.icon = pkm_icon
        self.icon_el = pkm_icon_el
        self.types = pkm_types
        self.evolutions = pkm_evolutions
        self.weakness = pkm_weakness
        self.strenghts = pkm_strenghts
        self.attacks = pkm_attacks

    @property
    def current_attack(self) -> str:
        """
        The function ataque_actual returns the value of the attribute _ataque_actual
        :return: The method returns the value of the attribute _ataque_actual.
        """
        return self._current_attack

    @property
    def dmg_current_attack(self) -> int:
        """
        It returns the damage of the attack, rounded to 2 decimal places
        :return: The damage of the attack.
        """
        return round(self._attack_damage, 2)

    @property
    def hp(self) -> float:
        """
        It returns the value of the attribute _vida of the object self
        :return: The value of the attribute _vida
        """
        return round(self._life, 2)

    @property
    def types(self) -> list[str]:
        """
        returns a list of strings
        """
        return self._types

    @property
    def evolutions(self) -> list[str]:
        """
        It returns a list of strings.
        :return: A list of strings.
        """
        return self._evolutions

    @property
    def strenghts(self) -> list[str]:
        """
        It returns a list of strings.
        :return: A list of strings
        """
        return self._strenghts

    @property
    def weakness(self) -> list[str]:
        """
        It returns a list of strings.
        :return: A list of strings
        """
        return self._weakness

    @property
    def attacks(self) -> list[str]:
        """
        It returns a list of strings.
        :return: A list of strings
        """
        return self._attacks

    @property
    def id(self) -> int:
        """
        It returns the id of the object.
        :return: The id of the object.
        """
        return self._id

    @property
    def name(self) -> str:
        """
        It returns the name of the object.
        :return: The name of the person
        """
        return self._name

    @property
    def power(self) -> int:
        """
        It returns the power of the car.
        :return: The power of the car.
        """
        return self._power

    @property
    def icon(self) -> bytes:
        """
        It returns the icon of the object.
        :return: The icon is being returned.
        """
        return self._icon

    @property
    def icon_el(self) -> bytes:
        """
        <code>def icon_el(self) -&gt; bytes:
        </code>
        The function <code>icon_el</code> takes a parameter <code>self</code> and returns a
        <code>bytes</code> object.
        :return: The icon_el is being returned.
        """
        return self._icon_el

    @property
    def efectivity_message(self) -> str:
        """
        It returns a string that is the value of the private attribute _msg_efectivity
        :return: The message of the efectivity of the attack.
        """
        return self._msg_efectivity

    @property
    def effectivity(self) -> int:
        """
        The function effectivity() returns the value of the variable _effectivity
        :return: The effectivity of the weapon.
        """
        return self._effectivity

    @property
    def is_critical_damage(self) -> bool:
        """
        This function returns a boolean value of whether or not the attack is a critical hit
        :return: The return value is a boolean value.
        """
        return self._critical_hit

    @current_attack.setter
    def current_attack(self, pkm_attack: str) -> None:
        """
        It takes a string as an argument and sets the value of the current_attack attribute to that
        string
        
        :param ataque: str
        :type ataque: str
        """
        self._current_attack = pkm_attack

    @dmg_current_attack.setter
    def dmg_current_attack(self, pkm_attack: int) -> None:
        """
        It takes an integer as an argument and sets the value of the attribute _attack_damage to the
        value of the argument rounded to two decimal places
        
        :param ataque: int
        :type ataque: int
        """
        self._attack_damage = round(pkm_attack, 2)

    @hp.setter
    def hp(self, pkm_amount_hp: float) -> None:
        """
        It takes a float as an argument and returns None
        
        :param cantidad: float = The amount of life you want to add to the player
        :type cantidad: float
        """
        self._life = round(pkm_amount_hp, 2)

    @types.setter
    def types(self, pkm_types: list[str]) -> None:
        """
        <code>types</code> is a function that takes a list of strings and returns None
        
        :param tipos: list[str]
        :type tipos: list[str]
        """
        self._types = pkm_types.copy()

    @evolutions.setter
    def evolutions(self, pkm_evolutions: list[str]) -> None:
        """
        The function takes a list of strings as an argument and assigns it to the _evolutions attribute
        of the object
        
        :param evoluciones: list[str]
        :type evoluciones: list[str]
        """
        self._evolutions = pkm_evolutions.copy()

    @strenghts.setter
    def strenghts(self, pkm_strenghts: list[str]) -> None:
        """
        The function takes a list of strings as an argument and assigns it to the attribute _strenghts
        
        :param fortalezas: list[str]
        :type fortalezas: list[str]
        """
        self._strenghts = pkm_strenghts.copy()

    @weakness.setter
    def weakness(self, pkm_weakness: list[str]) -> None:
        """
        It takes a list of strings as an argument and assigns it to the instance variable _weakness
        
        :param debilidades: list[str]
        :type debilidades: list[str]
        """
        self._weakness = pkm_weakness.copy()

    @attacks.setter
    def attacks(self, pkm_attacks: list[str]) -> None:
        """
        It takes a list of strings as an argument and assigns it to the _attacks attribute of the object
        
        :param ataques: list[str]
        :type ataques: list[str]
        """
        self._attacks = pkm_attacks.copy()

    @id.setter
    def id(self, pkm_id: int) -> None:
        """
        This function takes in an integer and sets the id of the object to that integer
        
        :param pkm_: The id of the user
        """
        self._id = pkm_id

    @name.setter
    def name(self, pkm_name: str) -> None:
        """
        This function takes a string as an argument and assigns it to the _name attribute of the object
        
        :param nombre: str
        :type nombre: str
        """
        self._name = pkm_name

    @power.setter
    def power(self, pkm_power: int) -> None:
        """
        This function takes in a parameter called poder, which is an integer, and returns None
        
        :param poder: int
        :type poder: int
        """
        self._power = pkm_power

    @icon.setter
    def icon(self, pkm_icon: bytes) -> None:
        """
        It takes a bytes object and sets it as the icon of the window
        
        :param icono: The icon to be used
        :type icono: bytes
        """
        self._icon = pkm_icon

    @icon_el.setter
    def icon_el(self, pkm_icon_el: bytes) -> None:
        """
        The function <code>efectivity_message</code> takes a <code>self</code> parameter and a
        <code>mensaje</code> parameter, both of which are strings. The function returns
        <code>None</code>
        
        :param icono_el: bytes
        :type icono_el: bytes
        """
        self._icon_el = pkm_icon_el

    @efectivity_message.setter
    def efectivity_message(self, effct_message: str) -> None:
        """
        <code>def efectivity_message(self, mensaje: str) -&gt; None:
        </code>
        The function <code>efectivity_message</code> takes a <code>self</code> parameter and a
        <code>mensaje</code> parameter, both of which are strings. The function returns
        <code>None</code>.
        
        :param mensaje: str
        :type mensaje: str
        """
        self._msg_efectivity = effct_message

    @effectivity.setter
    def effectivity(self, number: int) -> None:
        """
        This function takes in a number and sets the effectivity of the pokemon to that number
        
        :param number: int
        :type number: int
        """
        self._effectivity = number

    @is_critical_damage.setter
    def is_critical_damage(self, is_critical: bool) -> None:
        """
        "This function sets the value of the private attribute _critical_hit to the value of the
        parameter es_critico."
        
        The function is_critical_damage() is a setter function. It sets the value of the private
        attribute _critical_hit
        
        :param es_critico: bool
        :type es_critico: bool
        """
        self._critical_hit = is_critical

    def has_hp(self) -> bool:
        """
        It returns a boolean value.
        :return: a boolean value.
        """
        return self.hp > 0

    def set_hp(self) -> None:
        """
        This function sets the hp of the player to a random number between the minimum and maximum hp
        """
        self.hp = random.randint(self._MIN_HP, self._MAX_HP)

    def substract_hp(self, amount_hp: int) -> None:
        """
        If the amount of damage is less than the current HP, then subtract the damage from the current
        HP, otherwise, make the character faint
        
        :param cantidad: int
        :type cantidad: int
        """
        if amount_hp <= self.hp:
            self.hp = self.hp - amount_hp
        else:
            self.do_faint()

    def critical_chance(self) -> bool:
        """
        It returns a boolean value of True or False based on a 25% chance of being True
        :return: A random choice from the list of chances.
        """
        chances = [False, True, False, False]
        return random.choice(chances)

    def damage_from_attack(self) -> int:
        """
        It returns a random number between 10 and 20, and adds the value of the power attribute to it
        :return: The damage from the attack.
        """
        danho = random.randint(10, 20)
        self.is_critical_damage = self.critical_chance()
        return danho + self.power

    def attack_enemy(self, enemy_pokemon) -> None:
        """
        It chooses a random attack from the pokemon's attacks, calculates the damage of that attack, and
        then subtracts that damage from the enemy pokemon's health
        
        :param poke: The pokemon that is being attacked
        """
        ataque = random.choice(self.attacks)
        self.dmg_current_attack = self.calculate_dmg(enemy_pokemon)
        self.current_attack = ataque
        enemy_pokemon.substract_hp(self.dmg_current_attack)

    def has_weakness(self, enemy_pokemon) -> bool:
        """
        If the pokemon has a type that is a weakness of the enemy pokemon, return True, otherwise return
        False
        
        :param poke_enemigo: The enemy pokemon
        :return: a boolean value.
        """
        for tipo in self.types:
            if tipo in enemy_pokemon.strenghts:
                return True
        return False

    def has_strenghts(self, enemy_pokemon) -> bool:
        """
        If the pokemon has a type that is in the weakness of the enemy pokemon, return True, otherwise
        return False
        
        :param poke_enemigo: The enemy pokemon
        :return: a boolean value.
        """
        for tipo in self.types:
            if tipo in enemy_pokemon.weakness:
                return True
        return False

    def calculate_dmg(self, enemy_pokemon):
        """
        It calculates the damage of an attack, taking into account the type of the attack and the type
        of the pokemon that is being attacked
        
        :param poke_enemigo: The enemy pokemon
        :return: The damage of the attack
        """
        damage = self.damage_from_attack()
        booster = 1
        if self.has_weakness(enemy_pokemon) and (not self.has_strenghts(enemy_pokemon)):
            booster = 0.85
            mensaje = f'>> Es poco efectivo! Daño -15%'
            effect_point = -3
            if self.is_critical_damage:
                mensaje = f'>> Es poco efectivo! Daño -5% {_f_red}[CRITICAL DAMAGE]{_no_color}'
                booster = 0.95
                effect_point = -2
            self.effectivity = effect_point
            self.efectivity_message = mensaje
        elif self.has_strenghts(enemy_pokemon) and (not self.has_weakness(enemy_pokemon)):
            booster = 1.15
            mensaje = f'>> Es MUY efectivo! Daño +15% '
            effect_point = 3
            if self.is_critical_damage:
                mensaje = f'>> Es MUY efectivo! Daño +25%  {_f_red}[CRITICAL DAMAGE]{_no_color}'
                booster = 1.25
                effect_point = 4
            self.effectivity = effect_point
            self.efectivity_message = mensaje
        else:
            self.effectivity = 1
            self.efectivity_message = '>> Daño Normal!'
        return (damage * booster)

    def check_faint(self) -> None:
        """
        If the character does not have life, it will print a message saying that the character has been
        defeated
        """
        if not self.has_hp():
            print(f'>>> {self.name} ha sido vencido!')

    def do_faint(self) -> None:
        """
        It takes a character object, and sets its hp to 0
        """
        self.substract_hp(self.hp)

    def show_info(self) -> None:
        """
        It prints a message that contains the id, name, and hp of the object that calls it
        """
        message =\
        "ID: {0:03d} | Nombre: {1:10s} | Vida Restante: {2:03d}".format(self.id, self.name, self.hp)
        print(message)

    def continue_battle(self, enemy_pokemon):
        """
        If the enemy pokemon has life, the player pokemon attacks the enemy pokemon
        
        :param pokemon_enemigo: The enemy pokemon
        """
        if enemy_pokemon.has_hp():
            self.attack_enemy(enemy_pokemon)
            
    def heal(self) -> None:
        """
        The function heal() takes in a parameter self and returns None
        """
        self.hp = random.randint(self._MIN_HP, self._MAX_HP)
