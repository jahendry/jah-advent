from enum import Enum
from dataclasses import dataclass
from input_data import INPUT_DATA
from functools import reduce
import re


class CubeColours(str, Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"


class Round:
    def __init__(self, round_str: str) -> None:
        self.cube_count = {
            CubeColours.BLUE.value: 0,
            CubeColours.RED.value: 0,
            CubeColours.GREEN.value: 0,
        }

        for colour in self.cube_count.keys():
            capture_regex = re.compile(r"(\d+)\s+" + colour)
            result = capture_regex.findall(round_str)
            if len(result) != 0:
                self.cube_count[colour] = int(result[0])

    def is_possible(self, limits: dict[str, int]):
        for colour, limit in limits.items():
            if self.cube_count[colour] > limit:
                return False

        return True


@dataclass
class Game:
    game_number: int
    rounds: list[Round]

    def is_possible(self, limits: dict[str, int]):
        for round in self.rounds:
            if round.is_possible(limits) == False:
                return False

        return True

    def power_of_mins(self) -> int:
        self.current_fewest = {
            CubeColours.BLUE.value: 0,
            CubeColours.RED.value: 0,
            CubeColours.GREEN.value: 0,
        }
        for round in self.rounds:
            for colour, value in round.cube_count.items():
                if self.current_fewest[colour] < value:
                    self.current_fewest[colour] = value

        values = list(self.current_fewest.values())
        return reduce(lambda x, y: x * y, values[1:], values[0])


def _generate_rounds(input_data: list[str]) -> list[Game]:
    game_list: list[Game] = []
    for game in input_data:
        game_number, rounds = game.split(":")
        game_index = int(game_number[5:])

        round_list: list[Round] = []
        for round in rounds.split(";"):
            round_list.append(Round(round))

        game_list.append(Game(game_number=game_index, rounds=round_list))

    return game_list


def solution_part_1(input_data: list[str]) -> int:
    game_list = _generate_rounds(input_data)

    LIMITS = {
        CubeColours.BLUE.value: 14,
        CubeColours.RED.value: 12,
        CubeColours.GREEN.value: 13,
    }

    answer = sum([game.game_number for game in game_list if game.is_possible(LIMITS)])
    return answer


def solution_part_2(input_data: list[str]) -> int:
    game_list = _generate_rounds(input_data)

    answer = sum([game.power_of_mins() for game in game_list])
    return answer


if __name__ == "__main__":
    part_1_solution = solution_part_1(INPUT_DATA)
    print(f"Part 1 Solution: {part_1_solution}")

    part_2_solution = solution_part_2(INPUT_DATA)
    print(f"Part 2 Solution: {part_2_solution}")
