import cv2
import pygame
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
    """
    Facade for common pygame operations (drawing, image loading, etc).
    """
    def __init__(self, screen_size: tuple, caption: str = 'Noname') -> None:
        """
        Initializes the pygame window and clock.

        Args:
            screen_size (tuple): Size of the window.
            caption (str): Window caption.
        Returns:
            None
        """
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def draw_circle(self, x: int, y: int, color: tuple, radius: int) -> None:
        """
        Draws a circle on the screen.

        Args:
            x (int): X position.
            y (int): Y position.
            color (tuple): Color of the circle.
            radius (int): Radius of the circle.
        Returns:
            None
        """
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color) -> None:
        """
        Draws a rectangle on the screen.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.
            color (tuple): Color of the rectangle.
        Returns:
            None
        """
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color, width: int) -> None:
        """
        Draws a line on the screen.

        Args:
            x1 (int): Start X position.
            y1 (int): Start Y position.
            x2 (int): End X position.
            y2 (int): End Y position.
            color: Color of the line.
            width (int): Width of the line.
        Returns:
            None
        """
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

    @staticmethod
    def load_image(path: str, size: tuple) -> pygame.Surface:
        """
        Loads and scales an image from the given path.

        Args:
            path (str): Path to the image file.
            size (tuple): Size to scale the image to.
        Returns:
            pygame.Surface: The loaded and scaled image surface.
        """
        im = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(im, size)

    def draw_image(self, x: int, y: int, im: pygame.Surface) -> None:
        """
        Draws an image at the given position.

        Args:
            x (int): X position.
            y (int): Y position.
            im (pygame.Surface): Image surface to draw.
        Returns:
            None
        """
        self.screen.blit(im, (x, y))

    def update_screen(self) -> None:
        """
        Updates the display to show all drawn elements.

        Args:
            None
        Returns:
            None
        """
        pygame.display.flip()

    def clear_screen(self) -> None:
        """
        Clears the screen to black.

        Args:
            None
        Returns:
            None
        """
        self.screen.fill((0, 0, 0))

    def draw_text(self, x: int, y: int, text: str, color, font_size: int = 24) -> None:
        """
        Draws text on the screen at the given position.

        Args:
            x (int): X position.
            y (int): Y position.
            text (str): Text to draw.
            color: Color of the text.
            font_size (int): Font size.
        Returns:
            None
        """
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, x: int, y: int, width: int, height: int, text: str, button_color, text_color, font_size: int) -> pygame.Rect:
        """
        Draws button and returns its hitbox.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int): Button width.
            height (int): Button height.
            text (str): Button text.
            button_color: Button color.
            text_color: Text color.
            font_size (int): Font size.
        Returns:
            pygame.Rect: The button's hitbox rectangle.
        """
        self.draw_rectangle(x, y, width, height, button_color)
        self.draw_text(x + 2, y + 2, text, text_color, font_size)
        self.update_screen()
        return pygame.Rect(x, y, width, height)

    def image_to_surface(self, image: numpy.ndarray) -> pygame.Surface:
        image = numpy.rot90(image)
        image = numpy.flipud(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return pygame.surfarray.make_surface(image)

    def putText(self, image, xy: tuple, text: str, font_size: int = 24, color = (0, 0, 0)) -> None:
        return cv2.putText(image, text, xy, cv2.FONT_HERSHEY_SIMPLEX, font_size, color)
