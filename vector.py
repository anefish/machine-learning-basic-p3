from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'no unique orthogonal component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)


    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)


    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)


    def magnitude(self):
        '''大小'''
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))


    def normalized(self):
        '''方向'''
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector.')


    def dot(self, v):
        '''点积'''
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])


    def angle_with(self, v, in_degress=False):
        '''夹角'''
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            angle_in_radians = acos(u1.dot(u2))

            if in_degress:
                degress_per_radian = 180. / pi
                return angle_in_radians * degress_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e


    def is_orthogonal_to(self, v, tolerance=1e-10):
        '''是否正交'''
        return abs(self.dot(v)) < tolerance


    def is_parallel_to(self, v):
        '''是否平行'''
        return ( self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi )


    def is_zero(self, tolerance=1e-10):
        '''是否零向量'''
        return self.magnitude() < tolerance


    def component_parallel_to(self, basis):
        '''向量投影'''
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e


    def component_orthogonal_to(self, basis):
        '''向量垂直'''
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        '''向量积'''
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [ y_1*z_2 - y_2*z_1 ,
                              -(x_1*z_2 - x_2*z_1),
                                x_1*y_2 - x_2*y_1 ]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or
                  msg == 'need more than 1 value to unpack'):
                raise Exception('......') # TODO:
            else:
                raise e

    def area_of_parallelogram_with(self, v):
        '''平行四边形面积'''
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def area_of_triangle_with(self, v):
        '''三角形面积'''
        return self.area_of_parallelogram_with(v) / 2


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
