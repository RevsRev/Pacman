import pyglet
from game import physical_object

class score_object(physical_object.physical_object):

    def __init__(self, time, *args, **kwargs):
        super(score_object, self).__init__(*args, **kwargs)

        pyglet.clock.schedule_once(self.die, time)

    def die(self, dt):
        self.delete()
