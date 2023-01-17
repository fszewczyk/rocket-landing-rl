import math


class Vector():
    """!
    Class containing all the required geometric operations,
    such as rotation and translation.
    """

    def __init__(self, x=0, y=1, z=0):
        """!
        Initializes a Vector.
        Note that this vector is always a unit vector.
        Defaults to a vertical vector

        @param x (float): x component of the vector. Default: 0
        @param y (float): y component of the vector. Default: 1
        @param y (float): z component of the vector. Default: 0
        """

        self.x = x
        self.y = y
        self.z = z

        self.__normalize()

    def rotate_around_x(self, angle):
        """!
        Rotates the vector around x axis.

        @param angle (float): Angle in radians
        """

        self.y = self.y * math.cos(angle) - self.z * math.sin(angle)
        self.z = self.y * math.sin(angle) + self.z * math.cos(angle)

        self.__normalize()

    def rotate_around_z(self, angle):
        """!
        Rotates the vector around z axis.

        @param angle (float): Angle in radians
        """

        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)

        self.__normalize()

    def get_components(self, length):
        """!
        Calculates the components of a vector of specified length.

        @param length (float): Length of a desired vector

        @return list: Vector components
        """

        return [self.x * length, self.y * length, self.z * length]

    def __normalize(self):
        length = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

        self.x /= length
        self.y /= length
        self.z /= length
