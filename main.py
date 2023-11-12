import click
import re
from typing import Iterable, List, Dict

CHAIR_TYPES = ["P", "C", "S", "W"]


class LayoutLine:
    line: str
    y: int
    x_start: int
    x_end: int

    def __init__(self, line: str, y: int, x_start: int, x_end: int):
        self.line = line
        self.y = y
        self.x_start = x_start
        self.x_end = x_end

    def __repr__(self) -> str:
        return f"LayoutLine(y:{self.y}, x:{self.x_start}-{self.x_end})"

    @classmethod
    def from_matches(cls, y: int, matches: Iterable[re.Match]) -> List["LayoutLine"]:
        lines = []
        for match in matches:
            lines.append(LayoutLine(match.group(), y, match.start(), match.end()))
        return lines


class Room:
    layout: List[LayoutLine]
    completed: bool = False
    name: str = ""
    chairs: Dict[str, int] = {}

    def __init__(self, layout: List[LayoutLine]):
        self.layout = layout

    def __repr__(self) -> str:
        return f"Room({self.name}, chairs: {self.chairs})"

    def print_room(self):
        for l in self.layout:
            print(l.line)

    def find_name(self) -> str:
        regex = re.compile(r"\([\w ]+\)")
        for l in self.layout:
            m = regex.search(l.line)
            if m is not None:
                return m.group().strip("()")

    def find_chairs(self) -> Dict[str, int]:
        chairs = {}
        for l in self.layout:
            for chair in CHAIR_TYPES:
                if chair in l.line:
                    chairs[chair] = chairs.get(chair, 0) + l.line.count(chair)
        return chairs

    def is_connected(self, line: LayoutLine) -> bool:
        for l in self.layout:
            if l.y == line.y:
                return False  # we already have a line at this y coord
            if l.y == line.y - 1:
                if abs(l.x_start - line.x_start) <= 1 or abs(l.x_end - line.x_end) <= 1:
                    return True
        return False


def process_rooms(plan: List[str]) -> List[Room]:
    regex = re.compile(r"[\ ()\w]+")
    rooms = []
    for y, row in enumerate(plan.splitlines()):
        m = regex.finditer(row)
        lines = LayoutLine.from_matches(y, m)

        extended_rooms = []
        for room in rooms:
            for i, line in enumerate(lines):
                if not room.completed and room.is_connected(line):
                    room.layout.append(lines.pop(i))
                    extended_rooms.append(room)

        for room in rooms:
            if not room.completed and room not in extended_rooms:
                room.completed = True

        for line in lines:
            if line is not None:
                rooms.append(Room([line]))

    validated_rooms = []
    for room in rooms:
        if not room.completed:
            continue
        name = room.find_name()
        if name is None:
            continue
        room.name = name

        room.chairs = room.find_chairs()
        validated_rooms.append(room)

    validated_rooms.sort(key=lambda x: x.name)
    return validated_rooms


def process_total(rooms: List[Room]) -> Dict[str, int]:
    total_chairs = {}
    for room in rooms:
        for chair, count in room.chairs.items():
            total_chairs[chair] = total_chairs.get(chair, 0) + count
    return total_chairs


def display(name: str, chairs: Dict[str, int]):
    print(
        f"""{name}:
    W: {chairs.get('W', 0)}, P: {chairs.get('P', 0)}, S: {chairs.get('S', 0)}, C: {chairs.get('C', 0)}"""
    )


@click.command()
@click.option("--plan", "-p", type=click.File("r"), default="plan.txt")
def main(plan: click.File):
    plan = plan.read()

    rooms = process_rooms(plan)

    total_chairs = process_total(rooms)
    display("total", total_chairs)

    for room in rooms:
        display(room.name, room.chairs)


if __name__ == "__main__":
    main()
