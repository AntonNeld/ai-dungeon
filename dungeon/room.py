from entities.wall import Wall

class Room:

    def __init__(self):
        self._things = []
    
    def add_things(self, *things):
        for thing in things:
            if thing not in self._things:
                self._things.append(thing)
            else:
                raise RuntimeError("Cannot add thing twice: " + str(thing))
    
    def get_things(self):
        return self._things.copy()


# Create a default room (just for testing)
default_room = Room()
default_room.add_things(Wall(0,0), Wall(1,2), Wall(3,3))