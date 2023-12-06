from input_data import TEST_DATA, INPUT_DATA
from dataclasses import dataclass
import re
from collections import defaultdict


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(f"{self.x}{self.y}")


def _is_inside_search_range(coord: Coord, height: int, width: int) -> bool:
    return (0 <= coord.y < height) and (0 <= coord.x < width)


@dataclass
class SchematicPart:
    value: int
    row: int
    slice_start: int
    slice_end: int

    def _point_intersects(self, coord: Coord) -> bool:
        return (coord.y == self.row) and (self.slice_start <= coord.x < self.slice_end)

    def generate_internal_coors(self) -> list[Coord]:
        all_coords = []
        y_coord = self.row
        for x_coord in range(self.slice_start, self.slice_end):
            coord = Coord(x=x_coord, y=y_coord)
            all_coords.append(coord)

        return all_coords

    def generate_neighbour_coords(self, max_height: int, max_width: int) -> list[Coord]:
        neighbor_points = []
        for horizontal_range in range(self.slice_start - 1, self.slice_end + 1):
            for vertical_range in range(self.row - 1, self.row + 2):
                potential_neighbor = Coord(x=horizontal_range, y=vertical_range)

                if not (
                    self._point_intersects(potential_neighbor)
                ) and _is_inside_search_range(
                    potential_neighbor, max_height, max_width
                ):
                    neighbor_points.append(potential_neighbor)

        return neighbor_points

    def __hash__(self) -> int:
        return hash(f"{self.row}{self.slice_start}{self.slice_end}")


class SchematicBin:
    def __init__(
        self,
        schematic: list[str],
        part_numbers: list[SchematicPart],
        gears: list[SchematicPart],
    ) -> None:
        self.schematic = schematic
        self.part_numbers = part_numbers
        self.gears = gears
        self.internal_part_coors = set(
            [
                coord
                for part_number in self.part_numbers
                for coord in part_number.generate_internal_coors()
            ]
        )
        self.part_number_lookup = {}
        for part in self.part_numbers:
            for coord in part.generate_internal_coors():
                self.part_number_lookup[coord] = part

        self.part_number_index = defaultdict(list)

        for part in self.part_numbers:
            self.part_number_index[part.row].append((part.slice_start, part.slice_end))

    def find_meshing_gears(self) -> int:
        all_gear_ratios = 0
        height, width = len(self.schematic), len(self.schematic[0])
        for gear in self.gears:
            neighboring_points = set(gear.generate_neighbour_coords(height, width))
            intersecting_points = neighboring_points.intersection(
                self.internal_part_coors
            )
            if len(intersecting_points) != 0:
                meshing_parts = set(
                    [self.part_number_lookup[coord] for coord in intersecting_points]
                )
                if len(meshing_parts) == 2:
                    meshing_part_list = list(meshing_parts)
                    all_gear_ratios += (
                        meshing_part_list[0].value * meshing_part_list[1].value
                    )

        return all_gear_ratios


def _find_all_numbers(schematic: list[str]) -> list[SchematicPart]:
    NUM_SEARCH_REGEX = re.compile("\d+")

    all_schematic_parts: list[SchematicPart] = []

    for row_idx, line in enumerate(schematic):
        for number_match in NUM_SEARCH_REGEX.finditer(line):
            found_schematic_part = SchematicPart(
                value=int(number_match.group()),
                row=row_idx,
                slice_start=number_match.start(),
                slice_end=number_match.end(),
            )
            all_schematic_parts.append(found_schematic_part)

    return all_schematic_parts


def solution_part_one(schematic: list[str]) -> int:
    all_schematic_parts = _find_all_numbers(schematic)
    height, width = len(schematic), len(schematic[0])
    all_numbers = []
    for schematic_part in all_schematic_parts:
        for coord in schematic_part.generate_neighbour_coords(height, width):
            value = schematic[coord.y][coord.x]
            if not (value.isalnum()) and value != ".":
                all_numbers.append(schematic_part.value)
                break

    return sum(all_numbers)


def solution_part_two(schematic: list[str]) -> int:
    all_schematic_parts = _find_all_numbers(schematic)
    all_gears = []
    GEAR_SEARCH_REGEX = re.compile("\*+")

    for row_idx, line in enumerate(schematic):
        for gear in GEAR_SEARCH_REGEX.finditer(line):
            found_gear = SchematicPart(
                value=0, row=row_idx, slice_start=gear.start(), slice_end=gear.end()
            )
            all_gears.append(found_gear)

    schematic_bin = SchematicBin(schematic, all_schematic_parts, all_gears)

    mesh = schematic_bin.find_meshing_gears()
    return mesh


if __name__ == "__main__":
    part_one_solution = solution_part_one(INPUT_DATA)
    print(f"Part One Solution {part_one_solution}")

    part_two_solution = solution_part_two(INPUT_DATA)
    print(f"Part Two Solution {part_two_solution}")
