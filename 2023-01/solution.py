import re
from input_data import INPUT_DATA

NUMBER_PLUS_TEXT_REGEX = re.compile(
    r"""
        (?=        # look ahead
        (
            [0-9]| # either a number
            one|   # or the text representation
            two|
            three|
            four|
            five|
            six|
            seven|
            eight|
            nine)
        )
        """,
    re.VERBOSE,
)
NUMBER_REGEX = re.compile("[0-9]")


def _cast_to_str_int(number_string: str) -> str:
    try:
        return {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }[number_string]
    except KeyError:
        return number_string


def produce_solution(calibration_data: list[str], regex: re.Pattern) -> int:
    answer = 0
    for input_line in calibration_data:
        contained_numbers = regex.findall(input_line)
        value = int(
            f"{_cast_to_str_int(contained_numbers[0])}{_cast_to_str_int(contained_numbers[-1])}"
        )

        answer += value

    return answer


if __name__ == "__main__":
    part_1_solution = produce_solution(INPUT_DATA, NUMBER_REGEX)
    print(f"Part 1 Solution: {part_1_solution}")

    part_2_solution = produce_solution(INPUT_DATA, NUMBER_PLUS_TEXT_REGEX)
    print(f"Part 1 Solution: {part_2_solution}")
