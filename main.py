"""SkyFlight — a small, polished 2D flight animation built with Pygame."""

from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass

import pygame

WIDTH, HEIGHT = 1100, 680
FPS = 60
SKY_TOP = (18, 105, 184)
SKY_BOTTOM = (139, 211, 239)
WHITE = (245, 250, 255)
INK = (16, 39, 64)


def lerp_color(a: tuple[int, ...], b: tuple[int, ...], t: float) -> tuple[int, ...]:
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


@dataclass
class Cloud:
    x: float
    y: float
    scale: float
    speed: float
    alpha: int = 205

    def update(self, dt: float, multiplier: float) -> None:
        self.x -= self.speed * multiplier * dt
        if self.x < -150 * self.scale:
            self.x = WIDTH + random.randint(80, 280)
            self.y = random.randint(70, 300)

    def draw(self, surface: pygame.Surface, night: bool = False) -> None:
        layer = pygame.Surface((int(170 * self.scale), int(76 * self.scale)), pygame.SRCALPHA)
        color = (205, 218, 246, self.alpha) if night else (255, 255, 255, self.alpha)
        s = self.scale
        pygame.draw.ellipse(layer, color, (int(8*s), int(38*s), int(115*s), int(27*s)))
        for x, y, r in ((42, 37, 23), (72, 24, 31), (105, 39, 22)):
            pygame.draw.circle(layer, color, (int(x*s), int(y*s)), int(r*s))
        surface.blit(layer, (round(self.x), round(self.y)))


class SkyFlight:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("SkyFlight  |  A 2D Animation Studio")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeui", 17)
        self.small = pygame.font.SysFont("segoeui", 13)
        self.title = pygame.font.SysFont("segoeui", 25, bold=True)
        self.running = True
        self.paused = False
        self.fullscreen = False
        self.night_mode = False
        self.speed = 1.0
        self.elapsed = 0.0
        self.plane_x = -130.0
        self.propeller_angle = 0.0
        random.seed(18)
        self.stars = [(random.randrange(25, WIDTH-25), random.randrange(25, 390), random.choice((1, 1, 2))) for _ in range(72)]
        self.clouds = [Cloud(x, y, s, v, a) for x, y, s, v, a in (
            (60, 98, .82, 15, 185), (350, 170, 1.12, 21, 210),
            (720, 82, .72, 13, 175), (900, 240, 1.0, 18, 195),
            (540, 300, .58, 11, 145))]
        self.buttons: dict[str, pygame.Rect] = {}

    def draw_background(self, dt: float) -> None:
        sky_top, sky_bottom = ((7, 17, 48), (59, 67, 112)) if self.night_mode else (SKY_TOP, SKY_BOTTOM)
        for y in range(HEIGHT):
            pygame.draw.line(self.canvas, lerp_color(sky_top, sky_bottom, y / HEIGHT), (0, y), (WIDTH, y))
        if self.night_mode:
            for x, y, radius in self.stars:
                pygame.draw.circle(self.canvas, (226, 237, 255), (x, y), radius)
        # Sun by day, crescent moon at night.
        glow = pygame.Surface((190, 190), pygame.SRCALPHA)
        glow_color = (192, 207, 255) if self.night_mode else (255, 227, 145)
        for radius, alpha in ((88, 15), (68, 20), (48, 28)):
            pygame.draw.circle(glow, (*glow_color, alpha), (95, 95), radius)
        self.canvas.blit(glow, (625, 85))
        if self.night_mode:
            pygame.draw.circle(self.canvas, (228, 235, 255), (720, 180), 25)
            pygame.draw.circle(self.canvas, sky_top, (731, 169), 23)
        else:
            pygame.draw.circle(self.canvas, (255, 238, 174), (720, 180), 30)
            pygame.draw.circle(self.canvas, (255, 247, 213), (711, 171), 7)

        for cloud in self.clouds:
            cloud.update(dt, self.speed)
            cloud.draw(self.canvas, self.night_mode)

        # Distant peaks and nearer foothills scroll at different rates.
        far_offset = (self.elapsed * 8 * self.speed) % 520
        near_offset = (self.elapsed * 20 * self.speed) % 430
        for offset in (-520, 0, 520, 1040):
            x = offset - far_offset
            far_color = (50, 68, 108) if self.night_mode else (104, 158, 174)
            snow_color = (151, 165, 198) if self.night_mode else (224, 238, 232)
            second_peak = (59, 83, 119) if self.night_mode else (121, 177, 180)
            pygame.draw.polygon(self.canvas, far_color, [(x-90, 490), (x+105, 285), (x+270, 490)])
            pygame.draw.polygon(self.canvas, snow_color, [(x+64, 329), (x+105, 285), (x+146, 330), (x+120, 321), (x+105, 338), (x+91, 320)])
            pygame.draw.polygon(self.canvas, second_peak, [(x+175, 490), (x+355, 338), (x+540, 490)])
        for offset in (-430, 0, 430, 860, 1290):
            x = offset - near_offset
            hill_far = (36, 79, 83) if self.night_mode else (83, 151, 139)
            hill_near = (43, 96, 82) if self.night_mode else (104, 168, 143)
            pygame.draw.polygon(self.canvas, hill_far, [(x-60, 510), (x+130, 411), (x+285, 510)])
            pygame.draw.polygon(self.canvas, hill_near, [(x+110, 510), (x+305, 430), (x+465, 510)])

        ground = (26, 72, 59) if self.night_mode else (60, 137, 91)
        edge = (48, 107, 78) if self.night_mode else (119, 177, 112)
        grass = (43, 95, 70) if self.night_mode else (76, 151, 99)
        pygame.draw.rect(self.canvas, ground, (0, 502, WIDTH, HEIGHT-502))
        pygame.draw.rect(self.canvas, edge, (0, 502, WIDTH, 8))
        ground_offset = (self.elapsed * 105 * self.speed) % 90
        for x in range(-100, WIDTH + 100, 90):
            xx = x - ground_offset
            pygame.draw.line(self.canvas, grass, (xx, 510), (xx-32, 568), 3)
            pygame.draw.line(self.canvas, grass, (xx+18, 515), (xx+49, 561), 3)

    def draw_airplane(self) -> None:
        # Aircraft is drawn in local coordinates, then rotated as one sprite.
        sprite = pygame.Surface((300, 180), pygame.SRCALPHA)
        # Tailplane and vertical stabilizer
        pygame.draw.polygon(sprite, (200, 58, 63), [(54, 91), (17, 53), (68, 77), (91, 88)])
        pygame.draw.polygon(sprite, (189, 44, 55), [(60, 87), (30, 45), (74, 74), (94, 88)])
        # Main wings with a subtle shaded lower edge
        pygame.draw.polygon(sprite, (27, 91, 155), [(124, 80), (83, 16), (119, 22), (190, 79), (204, 90)])
        pygame.draw.polygon(sprite, (20, 72, 130), [(128, 91), (89, 151), (126, 143), (191, 96), (202, 88)])
        # Fuselage, nose points right
        pygame.draw.polygon(sprite, (244, 248, 246), [(28, 87), (76, 77), (167, 77), (232, 82), (262, 90), (232, 98), (162, 101), (75, 98), (32, 94)])
        pygame.draw.polygon(sprite, (210, 224, 234), [(75, 96), (162, 98), (232, 95), (247, 91), (231, 99), (162, 104), (75, 101)])
        # Cockpit and cabin windows
        pygame.draw.polygon(sprite, (30, 99, 145), [(198, 80), (221, 82), (237, 88), (200, 88)])
        for x in (146, 163, 180):
            pygame.draw.rect(sprite, (80, 154, 190), (x, 83, 10, 7), border_radius=3)
        # Red stripe and engine nacelles
        pygame.draw.polygon(sprite, (217, 60, 61), [(80, 94), (167, 94), (225, 91), (218, 95), (164, 98), (82, 98)])
        pygame.draw.ellipse(sprite, (196, 211, 219), (114, 115, 58, 15))
        pygame.draw.ellipse(sprite, (112, 137, 151), (112, 119, 61, 8))
        # Rotating propeller at nose.
        cx, cy = 264, 90
        a = math.radians(self.propeller_angle)
        for extra in (0, math.pi):
            ex, ey = math.cos(a+extra), math.sin(a+extra)
            pygame.draw.line(sprite, (36, 50, 67), (cx-ex*25, cy-ey*25), (cx+ex*25, cy+ey*25), 4)
        pygame.draw.circle(sprite, (220, 68, 57), (cx, cy), 6)
        rotated = pygame.transform.rotozoom(sprite, math.sin(self.elapsed*1.4)*2.2, 1.0)
        y = 320 + math.sin(self.elapsed*2.0)*16
        self.canvas.blit(rotated, rotated.get_rect(center=(round(self.plane_x), round(y))))

    def pill(self, text: str, center: tuple[int, int], active: bool = False) -> pygame.Rect:
        label = self.font.render(text, True, (255, 255, 255))
        rect = pygame.Rect(0, 0, label.get_width()+28, 38)
        rect.center = center
        pygame.draw.rect(self.canvas, (31, 65, 91, 235) if active else (29, 58, 82), rect, border_radius=19)
        pygame.draw.rect(self.canvas, (111, 173, 205), rect, 1, border_radius=19)
        self.canvas.blit(label, label.get_rect(center=rect.center))
        return rect

    def draw_hud(self) -> None:
        # Header plate
        pygame.draw.rect(self.canvas, (12, 37, 62), (24, 22, 286, 77), border_radius=18)
        pygame.draw.rect(self.canvas, (84, 170, 211), (24, 22, 4, 77), border_radius=2)
        self.canvas.blit(self.title.render("SKYFLIGHT", True, WHITE), (44, 30))
        self.canvas.blit(self.small.render("2D ANIMATION STUDIO  /  FLIGHT 01", True, (157, 202, 224)), (46, 65))
        # Live status panel
        status = "PAUSED" if self.paused else "IN FLIGHT"
        pygame.draw.circle(self.canvas, (250, 185, 75) if self.paused else (107, 225, 168), (44, 127), 5)
        self.canvas.blit(self.small.render(f"{status}   •   SPEED {self.speed:.1f}×", True, (236, 248, 252)), (57, 119))
        # Compact flight instrument card.
        panel = pygame.Rect(WIDTH-280, 22, 252, 132)
        pygame.draw.rect(self.canvas, (12, 37, 62), panel, border_radius=18)
        pygame.draw.rect(self.canvas, (84, 170, 211), (panel.left, panel.top+17, 4, 46), border_radius=2)
        self.canvas.blit(self.small.render("SIMULATED FLIGHT DATA", True, (157, 202, 224)), (panel.left+18, panel.top+15))
        altitude = round(3200 + math.sin(self.elapsed * 0.7) * 140)
        airspeed = round(175 + self.speed * 52)
        self.canvas.blit(self.font.render(f"ALT  {altitude:,} ft", True, WHITE), (panel.left+18, panel.top+43))
        self.canvas.blit(self.font.render(f"IAS   {airspeed} kt", True, WHITE), (panel.left+18, panel.top+70))
        heading = round((90 + math.sin(self.elapsed * 0.12) * 3) % 360)
        self.canvas.blit(self.small.render(f"HDG {heading:03d}°     {('NIGHT' if self.night_mode else 'DAY')}", True, (157, 202, 224)), (panel.left+18, panel.top+105))
        # Controls bar
        pygame.draw.rect(self.canvas, (12, 37, 62), (WIDTH//2-330, HEIGHT-76, 660, 54), border_radius=18)
        self.buttons["pause"] = self.pill("▶  Resume" if self.paused else "Ⅱ  Pause", (WIDTH//2-245, HEIGHT-49), self.paused)
        self.buttons["slower"] = self.pill("−", (WIDTH//2-135, HEIGHT-49))
        self.buttons["faster"] = self.pill("+", (WIDTH//2-70, HEIGHT-49))
        self.buttons["reset"] = self.pill("↺  Reset", (WIDTH//2+34, HEIGHT-49))
        self.buttons["daynight"] = self.pill("☼  Day" if self.night_mode else "☾  Night", (WIDTH//2+200, HEIGHT-49), self.night_mode)
        hint = self.small.render("SPACE pause   ·   ↑ / ↓ speed   ·   N day/night   ·   R reset   ·   ESC quit", True, (18, 58, 79))
        self.canvas.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT-96)))

    def reset(self) -> None:
        self.elapsed = 0
        self.plane_x = -130
        self.propeller_angle = 0
        self.speed = 1.0
        self.paused = False

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_n:
                    self.night_mode = not self.night_mode
                elif event.key in (pygame.K_UP, pygame.K_EQUALS, pygame.K_PLUS):
                    self.speed = min(3.0, self.speed + .2)
                elif event.key in (pygame.K_DOWN, pygame.K_MINUS):
                    self.speed = max(.2, self.speed - .2)
                elif event.key == pygame.K_r:
                    self.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point = event.pos
                # Map window coordinates to fixed design canvas.
                sx, sy = WIDTH/self.screen.get_width(), HEIGHT/self.screen.get_height()
                point = (int(point[0]*sx), int(point[1]*sy))
                if self.buttons.get("pause", pygame.Rect(0,0,0,0)).collidepoint(point):
                    self.paused = not self.paused
                elif self.buttons.get("slower", pygame.Rect(0,0,0,0)).collidepoint(point):
                    self.speed = max(.2, self.speed-.2)
                elif self.buttons.get("faster", pygame.Rect(0,0,0,0)).collidepoint(point):
                    self.speed = min(3.0, self.speed+.2)
                elif self.buttons.get("reset", pygame.Rect(0,0,0,0)).collidepoint(point):
                    self.reset()
                elif self.buttons.get("daynight", pygame.Rect(0,0,0,0)).collidepoint(point):
                    self.night_mode = not self.night_mode

    def run(self) -> None:
        while self.running:
            dt = min(self.clock.tick(FPS)/1000, .05)
            self.events()
            if not self.paused:
                self.elapsed += dt
                self.plane_x += 150 * self.speed * dt
                if self.plane_x > WIDTH + 160:
                    self.plane_x = -150
                self.propeller_angle = (self.propeller_angle + 1100 * dt * self.speed) % 360
            self.draw_background(dt if not self.paused else 0)
            self.draw_airplane()
            self.draw_hud()
            scaled = pygame.transform.smoothscale(self.canvas, self.screen.get_size())
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    try:
        SkyFlight().run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)
