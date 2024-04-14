import numpy as np

class celestial_object:
    
    # arguments for constructor:

    #   coordinates, [x, y, z] matrix numpy format  |  unit used is meters
    #   velocity, [x, y, z] matrix numpy format     |  unit used is meters per second
    #   mass, decimal                               |  unit used is kilograms
    #   radius, decimal                             |  unit used is meters
    #   name, string                                |  unit N/A

    def __init__(self, c, v, m, r, n):
        self.__coordinates = c
        self.__velocity = v
        self.__mass = m
        self.__radius = r
        self.__name = n

    def set_coordinates(self, c):
        self.__coordinates = c

    def set_velocity(self, v):
        self.__velocity = v

    def return_coordinates(self):
        return self.__coordinates

    def return_velocity(self):
        return self.__velocity

    def return_mass(self):
        return self.__mass

    def return_radius(self):
        return self.__radius

    def return_name(self):
        return self.__name
    
    def apply_acceleration(self, a, t):
        self.__velocity = np.add(self.__velocity, np.divide(a, t))
    
    def apply_velocity(self, t):
        self.__coordinates = np.add(self.__coordinates, np.divide(self.__velocity, t))