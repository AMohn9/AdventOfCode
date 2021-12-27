from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, List


@dataclass
class Amphipod:
    movement_cost: int

    room_num: Optional[int]
    place_in_room: Optional[int]

    hallway_place: Optional[int]

    can_move: bool = True

    @property
    def color(self):
        if self.movement_cost == 1:
            return "A"
        if self.movement_cost == 10:
            return "B"
        if self.movement_cost == 100:
            return "C"
        if self.movement_cost == 1000:
            return "D"

    @property
    def is_lower(self):
        return self.place_in_room == 1


@dataclass
class Room:
    room_num: int
    target_cost: int

    # amphipods: List[Amphipod]

    higher_amphipod: Optional[Amphipod]
    lower_amphipod: Optional[Amphipod]

    @property
    def is_empty(self) -> bool:
        # return not any(self.amphipods)
        return self.lower_amphipod is None

    @property
    def is_full(self) -> bool:
        # return self.amphipods[0] is not None
        return self.higher_amphipod is not None

    # @property
    # def higher_amphipod(self):
    #     return self.amphipods[0]
    #
    # @property
    # def lower_amphipod(self):
    #     return self.amphipods[1]


def parse_input_file(path: Path) -> Dict[int, Room]:
    # return {
    #     2: Room(2, 1, [Amphipod(10, 2, 0, None), Amphipod(1, 2, 1, None)]),
    #     4: Room(4, 10, [Amphipod(100, 4, 0, None), Amphipod(1000, 4, 1, None)]),
    #     6: Room(6, 100, [Amphipod(10, 6, 0, None), Amphipod(100, 6, 1, None)]),
    #     8: Room(8, 1000, [Amphipod(1000, 8, 0, None), Amphipod(1, 8, 1, None)])
    # }
    return {
        2: Room(2, 1, Amphipod(10, 2, 0, None), Amphipod(1, 2, 1, None)),
        4: Room(4, 10, Amphipod(100, 4, 0, None), Amphipod(1000, 4, 1, None)),
        6: Room(6, 100, Amphipod(10, 6, 0, None), Amphipod(100, 6, 1, None)),
        8: Room(8, 1000, Amphipod(1000, 8, 0, None), Amphipod(1, 8, 1, None))
    }
    # return {
    #     2: Room(2, 1, [Amphipod(1000, 2, 0, None), Amphipod(100, 2, 1, None)]),
    #     4: Room(4, 10, [Amphipod(10, 4, 0, None), Amphipod(100, 4, 1, None)]),
    #     6: Room(6, 100, [Amphipod(10, 6, 0, None), Amphipod(1000, 6, 1, None)]),
    #     8: Room(8, 1000, [Amphipod(1, 8, 0, None), Amphipod(1, 8, 1, None)])
    # }


def can_enter_room(amphipod: Amphipod, room: Room) -> bool:
    # Amphipods can only go in their "target" room
    if amphipod.movement_cost != room.target_cost:
        return False

    # Can't go in a full room
    if room.is_full:
        return False

    # An amphipod can enter a room if it's empty or if everything already in there has it's same "color"
    if room.is_empty:
        return True

    # FIXXX
    # return all(a.movement_cost == amphipod.movement_cost for a in room.amphipods if a)
    return room.lower_amphipod.movement_cost == amphipod.movement_cost


def distance_to_hallway(amphipod, hallway_num) -> int:
    # Does not check if the amphipod can move to this spot in the hallway
    distance = abs(hallway_num - amphipod.room_num)
    distance += amphipod.place_in_room + 1
    return distance


def distance_to_room(amphipod: Amphipod, room: Room) -> int:
    if amphipod.room_num == room.room_num:
        return 0

    # Does not check if the amphipod can move to this room
    current_place = amphipod.room_num or amphipod.hallway_place

    # Move through the hallway
    distance = abs(room.room_num - current_place)

    # Leave room
    if amphipod.room_num:
        distance += amphipod.place_in_room + 1

    # FIXXX
    # Settle in room
    # Find the deepest unoccupied spot
    # for place, a in enumerate(room.amphipods[::-1]):
    #     if not a:
    #         distance += len(room.amphipods) - place
    #         break
    if room.lower_amphipod is None:
        distance += 2
    else:
        distance += 1

    return distance


room_targets = {
    1: 2,
    10: 4,
    100: 6,
    1000: 8
}


@dataclass
class Runner:
    amphipods: List[Amphipod]
    rooms: Dict[int, Room]
    hallway_occupation: Dict[int, Optional[Amphipod]]
    best_so_far: int = float("inf")
    seen: Dict = field(default_factory=dict)
    move_stack: List = field(default_factory=list)

    def amphipod_can_move(self, amphipod: Amphipod):
        # If it's already settled in it's final room, it can't move again
        if not amphipod.can_move:
            return False

        # FIXXX
        # It can't leave its room if it's blocked in it's room
        # if amphipod.room_num:
        #     for a in self.rooms[amphipod.room_num].amphipods:
        #         if a:
        #             if a == amphipod:
        #                 break
        #             else:
        #                 return False
        if amphipod.room_num and amphipod.is_lower and self.rooms[amphipod.room_num].higher_amphipod is not None:
            return False

        return True

    def can_move_to_room(self, amphipod: Amphipod, room: Room) -> bool:
        if not self.amphipod_can_move(amphipod):
            return False

        # If it can't enter the room, then no point in trying
        if not can_enter_room(amphipod, room):
            return False

        current_place = amphipod.room_num or amphipod.hallway_place

        # It can't move through the hallway if any intermediate space is occupied
        for i in range(min(current_place + 1, room.room_num), max(current_place, room.room_num)):
            if self.hallway_occupation.get(i, None):
                return False

        return True

    def can_move_to_hallway(self, amphipod: Amphipod, hallway_num) -> bool:
        if self.hallway_occupation[hallway_num] is not None:
            return False

        if not self.amphipod_can_move(amphipod):
            return False

        room_num = amphipod.room_num

        # It can't move to the hallway if it's already in the hallway
        if not room_num:
            return False

        # It can't move through the hallway any intermediate space is occupied
        for i in range(min(room_num, hallway_num), max(room_num, hallway_num)):
            if self.hallway_occupation.get(i, None):
                return False

        return True

    def put_amphipod_in_room(self, amphipod: Amphipod, room: Room) -> int:
        if amphipod.room_num == room.room_num:
            return 0

        distance = distance_to_room(amphipod, room)

        # Remove it from it's current room or hallway
        if amphipod.room_num:
            # self.rooms[amphipod.room_num].amphipods[amphipod.place_in_room] = None
            if amphipod.is_lower:
                self.rooms[amphipod.room_num].lower_amphipod = None
            else:
                self.rooms[amphipod.room_num].higher_amphipod = None
        else:
            self.hallway_occupation[amphipod.hallway_place] = None

        # FIXXX
        # Settle in room
        # Find the deepest unoccupied spot
        # place = 0
        # for place, a in enumerate(room.amphipods[::-1]):
        #     if not a:
        #         room.amphipods[-1 - place] = amphipod
        #         break
        if room.lower_amphipod:
            place = 0
            room.higher_amphipod = amphipod
        else:
            place = 1
            room.lower_amphipod = amphipod
        # room.amphipods[place] = amphipod

        amphipod.room_num = room.room_num
        # FIXXX
        # amphipod.place_in_room = len(room.amphipods) - 1 - place
        amphipod.place_in_room = place
        amphipod.hallway_place = None

        return distance

    def put_amphipod_in_hallway(self, amphipod: Amphipod, hallway_num: int) -> int:
        distance = distance_to_hallway(amphipod, hallway_num)

        # Remove the amphipod from its room
        # self.rooms[amphipod.room_num].amphipods[amphipod.place_in_room] = None
        if amphipod.is_lower:
            self.rooms[amphipod.room_num].lower_amphipod = None
        else:
            self.rooms[amphipod.room_num].higher_amphipod = None

        # Put the amphipod in the hallway
        self.hallway_occupation[hallway_num] = amphipod

        amphipod.room_num = None
        amphipod.place_in_room = None
        amphipod.hallway_place = hallway_num

        return distance

    def done(self) -> bool:
        for room in self.rooms.values():
            # FIXXX
            # If we have mixed amphipods we're not done
            # for a in room.amphipods:
            #     if not a:
            #         return False
            #     if a.movement_cost != room.target_cost:
            #         return False
            if room.higher_amphipod is None or room.lower_amphipod is None or room.higher_amphipod.movement_cost != room.lower_amphipod.movement_cost:
                return False
        return True

    def recurse(self, total_move_cost: int, depth=0):

        amphipod, old_room_num, old_hallway_num = None, None, None
        def move_back():
            if old_room_num:
                # if amphipod.room_num:
                #     print(" " * depth + f"Moving amphipod {amphipod} back from room {amphipod.room_num} to room {old_room_num}")
                # if amphipod.hallway_place:
                #     print(" " * depth + f"Moving amphipod {amphipod} back from hallway {amphipod.hallway_place} to room {old_room_num}")
                self.put_amphipod_in_room(amphipod, self.rooms[old_room_num])
            else:
                # if amphipod.room_num:
                #     print(" " * depth + f"Moving amphipod {amphipod} back from room {amphipod.room_num} to hallway {old_hallway_num}")
                # if amphipod.hallway_place:
                #     print(" " * depth + f"Moving amphipod {amphipod} back from hallway {amphipod.hallway_place} to hallway {old_hallway_num}")
                self.put_amphipod_in_hallway(amphipod, old_hallway_num)
            amphipod.can_move = True

        # if total_move_cost == 40:
        #     print("Here")

        if total_move_cost >= self.best_so_far:
            yield None
        elif self.done():
            self.best_so_far = total_move_cost
            yield total_move_cost
        else:
            for amphipod in self.amphipods:

                # if total_move_cost == 0:
                #     print("Starting")

                # If it can't move then no use trying
                if not amphipod.can_move:
                    continue

                old_room_num = amphipod.room_num
                old_hallway_num = amphipod.hallway_place

                # Try to enter target room first
                target_room = self.rooms[room_targets[amphipod.movement_cost]]
                if self.can_move_to_room(amphipod, target_room):
                    distance = self.put_amphipod_in_room(amphipod, target_room)
                    # self.move_stack.append(" " * depth + f"Amphipod {amphipod} can move to room {target_room.room_num} with cost {distance * amphipod.movement_cost}")
                    # self.move_stack.append(str(self))
                    new_cost = total_move_cost + distance * amphipod.movement_cost
                    hash_code = self.hashy()
                    if self.seen.get(hash_code, float("inf")) > new_cost:
                        self.seen[hash_code] = new_cost
                        # print(" " * depth + f"Amphipod {amphipod} can move to room {target_room.room_num} with cost {distance}")
                        # print(self)
                        amphipod.can_move = False
                        yield from self.recurse(new_cost, depth + 1)

                    # Move it back to it's original place
                    move_back()
                    # self.move_stack.pop()
                    # self.move_stack.pop()
                    # print(self)

                # Try to enter hallways
                if amphipod.hallway_place is None:
                    for hallway_num in self.hallway_occupation.keys():
                        if self.can_move_to_hallway(amphipod, hallway_num):
                            # If it can move to this hallway place, put it there and recurse
                            distance = self.put_amphipod_in_hallway(amphipod, hallway_num)
                            # self.move_stack.append(" " * depth + f"Amphipod {amphipod} can move to hallway {hallway_num} cost {distance * amphipod.movement_cost}")
                            # self.move_stack.append(str(self))
                            new_cost = total_move_cost + distance * amphipod.movement_cost
                            hash_code = self.hashy()
                            if self.seen.get(hash_code, float("inf")) > new_cost:
                                self.seen[hash_code] = new_cost
                                # print(" " * depth + f"Amphipod {amphipod} can move to hallway {hallway_num} cost {distance}")
                                # print(self)
                                yield from self.recurse(new_cost, depth + 1)

                            # Move it back to it's original place
                            move_back()
                            # self.move_stack.pop()
                            # self.move_stack.pop()
                            # print(self)

    def __str__(self):
        s = "#############\n"
        s += "#"
        for i in range(0, 11):
            if self.hallway_occupation.get(i):
                s += self.hallway_occupation[i].color
            else:
                s += "."
        s += "#\n"

        s += "###"
        for room in self.rooms.values():
            if room.higher_amphipod:
                s += room.higher_amphipod.color
            else:
                s += "."
            s += "#"
        s += "##\n"

        s += "  #"
        for room in self.rooms.values():
            if room.lower_amphipod:
                s += room.lower_amphipod.color
            else:
                s += "."
            s += "#"
        s += "\n  #########\n"
        return s

    def hashy(self):
        s = ""
        for a in self.amphipods:
            s += str(a)
        return s


def part_1(path: Path) -> int:
    rooms = parse_input_file(path)
    amphipods = []
    for room in rooms.values():
        # amphipods.extend(room.amphipods)
        amphipods.append(room.higher_amphipod)
        amphipods.append(room.lower_amphipod)
    hallway_places = {i: None for i in [0, 1, 3, 5, 7, 9, 10]}

    runner = Runner(amphipods, rooms, hallway_places)
    runner.move_stack.append(str(runner))

    for solution_distance in runner.recurse(0):
        if solution_distance:
            print(solution_distance)

    # return min(solution_distance for solution_distance in runner.recurse(0))

    return 0


def part_2(path: Path) -> int:
    return 0


if __name__ == "__main__":
    print(part_1(Path("day_23.txt")))
    # print(part_2(Path("day_23.txt")))
