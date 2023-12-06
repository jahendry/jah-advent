from unittest import TestCase
from input_data import TEST_DATA
from solution import solution_part_1, solution_part_2


class TestSolution(TestCase):
    def test_part_one(self) -> None:
        excepted_part_one_answer = 8
        returned_answer = solution_part_1(TEST_DATA)
        self.assertEqual(excepted_part_one_answer, returned_answer)

    def test_part_two(self) -> None:
        excepted_part_one_answer = 2286
        returned_answer = solution_part_2(TEST_DATA)
        self.assertEqual(excepted_part_one_answer, returned_answer)
