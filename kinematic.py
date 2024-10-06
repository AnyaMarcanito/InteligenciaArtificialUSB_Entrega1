import random
from vector import Vector
import math

class Kinematic:
    def __init__(self, position, orientation, velocity, rotation):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.rotation = rotation

    def update(self, steering, time):
        self.position += self.velocity * time
        self.orientation += self.rotation * time
        self.velocity += steering.velocity * time
        self.rotation += steering.rotation * time

    def update_with_steering(self, steering, maxSpeed, time):
        # Update the position and orientation.
        self.position += self.velocity * time
        self.orientation += self.rotation * time

        # Update the velocity and rotation.
        self.velocity += steering.linear * time
        self.rotation += steering.angular * time

        # Check for speeding and clip.
        if self.velocity.length() > maxSpeed:
            self.velocity.normalize()
            self.velocity *= maxSpeed

    def newOrientation(self, current, velocity):
        if velocity.length() > 0:
            return math.atan2(-velocity.x, velocity.y)
        else:
            return current

    @staticmethod
    def orientationToVector(orientation):
        return Vector(math.cos(orientation), math.sin(orientation))

class KinematicSteeringOutput:
    def __init__(self, velocity=None, rotation=0):
        self.velocity = velocity if velocity is not None else Vector(0, 0)
        self.rotation = rotation

class KinematicSeek:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = SteeringOutput()
        result.linear = self.target.position - self.character.position
        result.linear.normalize()
        result.linear *= self.maxSpeed
        result.angular = 0
        return result
    
class KinematicArrive:
    def __init__(self, character, target, maxSpeed, radius):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.radius = radius

    def getSteering(self):
        result = SteeringOutput()
        direction = self.target.position - self.character.position
        distance = direction.length()

        if distance < self.radius:
            return None

        result.linear = direction
        result.linear.normalize()
        result.linear *= self.maxSpeed * (distance / self.radius)
        result.angular = 0
        return result

class KinematicWander:
    def __init__(self, character, maxSpeed, maxRotation):
        self.character = character
        self.maxSpeed = maxSpeed
        self.maxRotation = maxRotation

    def getSteering(self):
        result = KinematicSteeringOutput()
        result.velocity = Kinematic.orientationToVector(self.character.orientation) * self.maxSpeed
        self.character.orientation += (random.random() - 0.5) * self.maxRotation
        result.velocity *= random.uniform(0.5, 1.5)
        return result

    def randomBinomial(self):
        return random.random() - random.random()

class KinematicFlee:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = SteeringOutput()
        result.linear = self.character.position - self.target.position
        result.linear.normalize()
        result.linear *= self.maxSpeed
        result.angular = 0
        return result