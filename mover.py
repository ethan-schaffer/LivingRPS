import random

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def trim(v, upper, lower):
    if v > upper:
        return upper
    if v < lower:
        return lower
    return v

def between_range(v, u):
    p = v + u
    m = u * 2
    return random.randint(p // 2, (m + p) // 2) - u

def abs(x):
    return x if x > 0 else -x


class Mover:
    def __init__(self, thing, coords, v, a, max_height, max_width, max_velo, max_accel):
        self.ticks = 0
        self.time = 0
        self.color = thing
        self.coord_x, self.coord_y = coords
        self.velocity_x, self.velocity_y = v
        self.acceleration_x, self.acceleration_y = a
        self.max_height = max_height
        self.max_width = max_width
        self.max_velo = max_velo
        self.max_accel = max_accel

    def get_color(self):
        return self.color

    def update_color(self, c):
        if (c, self.color) in [(0, 1), (1, 2), (2, 0)]:
            self.color = c

    def get_x(self):
        return self.coord_x

    def get_y(self):
        return self.coord_y

    def get_position(self):
        return self.coord_x, self.coord_y

    def update_position(self):
        self.coord_x += self.velocity_x
        self.coord_y += self.velocity_y

        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y

        self.ticks += 1
        if self.ticks == 5:
            self.time += 1
            self.ticks = 0
            target_x = random.randint(
                trim((self.time * self.max_width // 100), self.max_width // 4, 0),
                trim(self.max_width - (self.time * self.max_width // 100), self.max_width, 3*self.max_width//4))
            vector_x = target_x - self.coord_x
            self.acceleration_x = self.max_accel * vector_x / self.max_width

            target_y = random.randint(
                trim((self.time * self.max_height // 100), self.max_height // 4, 0),
                trim(self.max_height - (self.time * self.max_height // 100), self.max_height, 3*self.max_height//4))
            vector_y = target_y - self.coord_y
            self.acceleration_y = self.max_accel * vector_y / self.max_height

        self.coord_x = trim(self.coord_x, self.max_width, 0)
        self.coord_y = trim(self.coord_y, self.max_height, 0)

        self.velocity_x = trim(self.velocity_x, self.max_velo, -self.max_velo)
        self.velocity_y = trim(self.velocity_y, self.max_velo, -self.max_velo)

        self.acceleration_x = trim(self.acceleration_x, self.max_accel, -self.max_accel)
        self.acceleration_y = trim(self.acceleration_y, self.max_accel, -self.max_accel)

    def __str__(self):
        return "" + str(self.color) + " " + str(self.coord_x) + " " + str(self.coord_y)