from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

'''
You may find the commands `player.current_room.id`, `player.current_room.get_exits()` and `player.travel(direction)` useful.

PLAYER.current_room gives an error but current_room works
'''

def dft_recur_init(current_room):
    visited=set()
    path=list()

    def dft_recur(current_room, previous_direction=None): #we're going to find prev direction later on
        # print("CURRENT ROOM", current_room)
        visited.add(current_room.id)
        #when you visit a room add it to the visited list
        # print("visited", visited)

        for exit in current_room.get_exits():#for every exit in the current room get the next room in each direction
            next_room=current_room.get_room_in_direction(exit)
            # previous_direction=exit this does not work inside the recur func, just send it in 
            # print("NEXT ROOM",next_room)
            if next_room.id in visited: #if we've been there already...
                continue #skippity do da
            else: #otherwise if we haven't...
                visited.add(next_room.id)#add the next room id to the visited list
                path.append(exit) #attach the exit to the path
            #Run again until all rooms have been visited and all exits appended to path
            dft_recur(next_room, previous_direction=exit)
        
        if previous_direction is not None: #if we've passed in an exit from the recursion line above...
            back={"n": "s", "e": "w", "s": "n", "w": "e"}
            previous=back[previous_direction]#get the opposite of the exit direction
            # print("***PREVIOUS***", previous)
            path.append(previous)#append it to the path to be explored
    dft_recur(current_room)
    return path

traversal_path=dft_recur_init(world.starting_room)

# TRAVERSAL TEST
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
