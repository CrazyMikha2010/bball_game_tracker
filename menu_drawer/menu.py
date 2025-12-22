from pygame_facade import PygameFacade
import pygame as pg

class Menu():
    def __init__(self, screen_size: tuple):
        self.surface = pg.display.set_mode(screen_size)
        self.W = screen_size[0]
        self.H = screen_size[1]
        self.pg_facade = PygameFacade(screen_size)
        self.is_back = False

    def draw_buttons(self):
        self.is_back = False
        self.start = self.pg_facade.draw_button(480, 300, 320, 80, "START", (235, 66, 0), (0, 0, 0), 120)
        self.help = self.pg_facade.draw_button(480, 410, 320, 80, "HELP", (235, 66, 0), (0, 0, 0), 120)
        self.settings = self.pg_facade.draw_button(480, 520, 320, 80, "SETTINGS", (235, 66, 0), (0, 0, 0), 90)
        self.cur = self.start

    def menu_back(self):
        self.is_back = True
        self.back = self.pg_facade.draw_button(15, 15, 200, 60, "BACK", (235, 66, 0), (0, 0, 0), 80)

    def menu_start(self):
        return True

    def menu_help(self):
        self.cur = self.help
        rules = ["-Поставьте камеру чтобы было видно корт и кольцо",
                 "-Постарайтесь играть одним мячом и быть единственным", "игроком на площадке",
                 "-Программа будет регестрировать забитые и промахи",
                 "-После игры ваша статистика сохранится"]
        self.pg_facade.draw_rectangle(100, 100, 1080, 520, (235, 66, 0))
        for i in range(len(rules)):
            self.pg_facade.draw_text(120, 120 + i * 70, rules[i], (0, 0, 0), 52)

    def update(self, mouse: tuple):
        for button in [self.start, self.help, self.settings, self.back]:
            if button.collidepoint(mouse):
                if button == self.start:
                    if self.is_back:
                        continue
                    else:
                        self.menu_


if __name__ == '__main__':
    menu = Menu((1280, 720))

    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                menu.update((event.pos[0], event.pos[1]))
        menu.pg_facade.clear_screen()
        menu.menu_help()
        menu.pg_facade.update_screen()
