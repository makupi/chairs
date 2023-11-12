from main import process_rooms, Room, LayoutLine

def test_process_rooms():
    plan = """
    +---------+--------+
    |  (a)    |  (b)   |
    |  W      |   C    |
    |  S      /   X    |
    +--------+--------+"""
    

    rooms = process_rooms(plan)
    assert len(rooms) == 2

    assert rooms[0].name == "a"
    assert rooms[1].name == "b"
    assert rooms[0].chairs.get("W") == 1
    assert rooms[0].chairs.get("S") == 1
    assert rooms[1].chairs.get("C") == 1

    # X doesn't exist and shouldn't be processed
    assert rooms[1].chairs.get("X") is None

def test_is_connected():
    line0 = LayoutLine("", 1, 1, 10)
    line1 = LayoutLine("", 1, 11, 20)
    line2 = LayoutLine("", 2, 2, 9)
    line3 = LayoutLine("", 2, 1, 10)
    room = Room([line0])

    # line1 is on the same line as line0
    assert room.is_connected(line1) == False
    assert room.is_connected(line2) == True
    assert room.is_connected(line3) == True
