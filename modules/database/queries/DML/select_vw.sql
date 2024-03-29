/** GNU General Public License V3
*
* Copyright (C) <2022>  <Facundo Falcone>
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

SELECT
    `id`, `trainer_name`, `status`, `amount_pokemons`, `score`, `dataingestiondttm`
FROM `T_NAME_vw`
GROUP BY
`id`, `trainer_name`, `status`, `amount_pokemons`, `score`, `dataingestiondttm`
ORDER BY 
`status` DESC,
`score` DESC, 
`amount_pokemons` DESC,
`trainer_name` DESC