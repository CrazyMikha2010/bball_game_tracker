import cv2
import pygame as pg
import numpy


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class PygameFacade:
    def __init__(self, screen_size: tuple, caption: str = 'Noname') -> None:
        pg.init()
        self.screen = pg.display.set_mode(screen_size)
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()

    def draw_circle(self, x: int, y: int, color: tuple, radius: int) -> None:
        pg.draw.circle(self.screen, color, (x, y), radius)

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color, border_radius: int = 0) -> None:
        pg.draw.rect(self.screen, color, pg.Rect(x, y, width, height), border_radius=border_radius)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color, width: int) -> None:
        pg.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

    @staticmethod
    def load_image(path: str, size: tuple) -> pg.Surface:
        im = pg.image.load(path).convert_alpha()
        return pg.transform.scale(im, size)

    def draw_image(self, x: int, y: int, im: pg.Surface) -> None:
        self.screen.blit(im, (x, y))

    def update_screen(self) -> None:
        pg.display.flip()

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def draw_text(self, x: int, y: int, text: str, color, font_size: int = 24) -> None:
        font = pg.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def image_to_surface(self, image: numpy.ndarray) -> pg.Surface:
        image = numpy.rot90(image)
        image = numpy.flipud(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return pg.surfarray.make_surface(image)

    def putText(self, image, xy: tuple, text: str, font_size: int = 24, color = (0, 0, 0)) -> None:
        return cv2.putText(image, text, xy, cv2.FONT_HERSHEY_SIMPLEX, font_size, color)

    def text_size(self, text: str, font_size: int) -> tuple:
        font = pg.font.Font(None, font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        return text_surface.get_size()

class Button():
    def __init__(self, topleft: tuple, size: tuple, text: str, border_radius: int, font_size: int, text_color, text_color_hover, button_color, button_color_hover, facade, callback):
        self.rect = pg.Rect(topleft + size)
        self.border_radius = border_radius
        self.font_size = font_size
        self.text_color = text_color
        self.text_color_hover = text_color_hover
        self.button_color = button_color
        self.button_color_hover = button_color_hover
        self.text = text
        self.facade = facade
        self.hover = False
        self.callback = callback
        self.textw, self.texth = self.facade.text_size(self.text, self.font_size)

    def update(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEMOTION:
            self.hover = self.rect.collidepoint(pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.callback
        return None

    def draw(self):
        button_color = self.button_color_hover if self.hover else self.button_color
        self.facade.draw_rectangle(self.rect.x, self.rect.y, self.rect.size[0], self.rect.size[1], button_color, self.border_radius)
        text_color = self.text_color_hover if self.hover else self.text_color
        self.facade.draw_text(self.rect.topleft[0] + (self.rect.size[0] - self.textw) // 2, self.rect.topleft[1] + (self.rect.size[1] - self.texth) // 2, self.text, text_color, self.font_size)

class ToggleSwitch():
    def __init__(self, topleft: tuple, size: tuple, button_color, button_color_acitve, circle_color, facade):
        self.facade = facade
        self.topleft = topleft
        self.size = size
        self.button_color = button_color
        self.button_color_acitve = button_color_acitve
        self.circle_color = circle_color
        self.is_active = False
        self.circle_radius = self.size[1] // 2
        self.circle_x, self.circle_y = self.topleft[0] + self.circle_radius, self.topleft[1] + self.circle_radius
        self.rect = pg.Rect(topleft + size)
        self.speed = 10
        self.border_radius = self.size[1] // 2 - 4
        self.target_x = self.circle_x

    def update(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle()
                return True
        return False

    def toggle(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.target_x = self.rect.x + self.size[0] - self.circle_radius
        else:
            self.target_x = self.rect.x + self.circle_radius

    def draw(self):
        if abs(self.circle_x - self.target_x) >= 1:
            if self.target_x < self.circle_x:
                self.circle_x = max(self.target_x, self.circle_x - self.speed)
            else:
                self.circle_x = min(self.target_x, self.circle_x + self.speed)

        cur_button_color = self.button_color_acitve if self.is_active else self.button_color
        self.facade.draw_rectangle(self.rect.x, self.rect.y, self.size[0], self.size[1], cur_button_color, self.border_radius)
        self.facade.draw_circle(self.circle_x, self.circle_y, self.circle_color, self.circle_radius)
