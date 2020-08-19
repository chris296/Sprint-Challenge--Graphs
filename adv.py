from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2) 
        else:
            raise IndexError("nonexisten vertex")

    def get_parents(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            return -1 

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
print("room id:", player.current_room.get_exits())

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
backtrack_directions = {"n":"s", "s": "n", "e": "w", "w":"e"}
backtrack = []
rooms = {}
rooms[player.current_room.id] = player.current_room.get_exits()

previous_rooms = None

while len(rooms) < len(room_graph):
    if player.current_room.id not in rooms:
        rooms[player.current_room.id] = player.current_room.get_exits()
        reverse_direction = backtrack[-1]
        rooms[player.current_room.id].remove(reverse_direction)
    while len(rooms[player.current_room.id]) < 1:
        reverse_direction = backtrack.pop()
        traversal_path.append(reverse_direction)
        player.travel(reverse_direction)
    exit_direction = rooms[player.current_room.id].pop(0)
    traversal_path.append(exit_direction)
    backtrack.append(backtrack_directions[exit_direction])
    player.travel(exit_direction)
    if len(room_graph) - len(rooms) == 1:
        rooms[player.current_room.id] = player.current_room.get_exits()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
