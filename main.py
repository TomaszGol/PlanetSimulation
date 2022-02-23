import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (70, 190, 237)
RED = (190, 40, 50)
DARK_GREY = (100, 100, 100)

FONT = pygame.font.SysFont('comicsans', 16)

AU = 149.6e6 * 1000
G = 6.67428e-11
SCALE = 250 / AU  # 1AU = 100px
TIMESTEP = 3600 * 24  # 1 day


class CelestialBodies:

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.distance_to_sun = 0

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x, y), self.radius)


class Planet(CelestialBodies):
    def __init__(self, x, y, radius, color, mass):
        CelestialBodies.__init__(self, x, y, radius, color, mass)
        self.distance_to_sun = 0

        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + WIDTH / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        distance_text = FONT.render(f'{round(self.distance_to_sun)/1000}km', 1, WHITE)
        win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if isinstance(other, Sun):
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)  # Getting angel
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.orbit.append((self.x, self.y))


class Sun(CelestialBodies):
    def __init__(self, x, y, radius, color, mass):
        CelestialBodies.__init__(self, x, y, radius, color, mass)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Sun(0, 0, 30, YELLOW, 1.98892 * 10**30)

    earth = Planet(AU, 0, 16, BLUE, 5.5842 * 10*24)
    earth.y_vel = -29.783 * 1000  # Meters per second

    mars = Planet(1.524 * AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = -24.077 * 1000

    mercury = Planet(0.387 * AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    objects = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in objects:
            if not isinstance(planet, Sun):
                planet.update_position(objects)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


main()
