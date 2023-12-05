from unittest import TestCase
from input_data import PART_1_TEST_DATA, PART_2_TEST_DATA
from solution import produce_solution, NUMBER_REGEX, NUMBER_PLUS_TEXT_REGEX


class TestSolution(TestCase):
    def test_part_one(self) -> None:
        excepted_part_one_answer = 142
        returned_answer = produce_solution(PART_1_TEST_DATA, NUMBER_REGEX)
        self.assertEqual(excepted_part_one_answer, returned_answer)

    def test_part_two(self) -> None:
        excepted_part_two_answer = 281
        returned_answer = produce_solution(PART_2_TEST_DATA, NUMBER_PLUS_TEXT_REGEX)
        self.assertEqual(excepted_part_two_answer, returned_answer)
