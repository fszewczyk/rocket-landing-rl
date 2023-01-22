import math


class Vector():
    """!
    Class containing all the required geometric operations,
    such as rotation and translation.
    """

    def __init__(self, x=0, y=1):
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

        self.__normalize()

    def rotate_around_z(self, angle):
        """!
        Rotates the vector around z axis.

        @param angle (float): Angle in radians
        """

        temp_x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)

        self.x = temp_x

        self.__normalize()

    def get_components(self, length):
        """!
        Calculates the components of a vector of specified length.

        @param length (float): Length of a desired vector

        @return list: Vector components
        """

        return [self.x * length, self.y * length]

    def get_component_along_vector(self, vector):
        """!
        Calculates the components along a specified vector
        using a dot product.

        @param vector (Vector): Vector to calculate the components along
        """

        return self.x * vector.x + self.y * vector.y

    def get_rotated_vectors(self):
        """!
        Calculated 2 axis that are rotated to fit this vector

        @return list: Vectors defining transformed coordinate system

        Example:
        [1,1] -> ([0.707,0.707,0],[0.707,-0.707,0])
        """

        along = Vector(self.x, self.y)
        side = Vector(self.x, self.y)
        side.rotate_around_z(math.pi / 2)

        return along, side

    def __normalize(self):
        """!
        Converts the vector into unit vector
        """

        length = Vector.get_length(self.x, self.y)

        if length > 0:
            self.x /= length
            self.y /= length

    @staticmethod
    def get_length(x, y):
        return math.sqrt(x*x + y*y)

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"
