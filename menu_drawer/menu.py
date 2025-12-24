import pygame as pg
from .pygame_facade import Button, ToggleSwitch

class Menu():
    def __init__(self, screen_size: tuple, facade):
        self.surface = pg.display.set_mode(screen_size)
        self.W = screen_size[0]
        self.H = screen_size[1]
        self.pg_facade = facade
        self.cur = "main"
        self.buttons = {
            "start": Button((480, 300), (320, 80), "START", 20, 120, (0, 0, 0), (255, 255, 255), (235, 66, 0), (145, 41, 0),self.pg_facade, self.menu_start),
            "help": Button((480, 410), (320, 80), "HELP", 20, 120, (0, 0, 0), (255, 255, 255), (235, 66, 0), (145, 41, 0),self.pg_facade, self.menu_help),
            "settings": Button((480, 520), (320, 80), "SETTINGS", 20, 90, (0, 0, 0), (255, 255, 255), (235, 66, 0),(145, 41, 0), self.pg_facade, self.menu_settings),
            "back": Button((15, 15), (200, 60), "BACK", 20, 80, (0, 0, 0), (255, 255, 255), (235, 66, 0), (145, 41, 0),self.pg_facade, self.menu_back)
        }
        self.switches = []
        for i in range(5):
            self.switches.append(ToggleSwitch((240, 140 + i * 75), (100, 50), (176, 176, 176), (52, 235, 64), (255, 255, 255), self.pg_facade))
        self.is_start = False
        self.settings = []

    def draw(self):
        self.pg_facade.clear_screen()
        if self.cur == "main":
            for button_name in ["start", "help", "settings"]:
                self.buttons[button_name].draw()
        else:
            self.buttons["back"].draw()

        if self.cur == "help":
            self.draw_menu_help()
        elif self.cur == "settings":
            self.draw_menu_settings()

        self.pg_facade.update_screen()

    def menu_back(self):
        self.cur = "main"

    def draw_menu_start(self):
        ...

    def menu_start(self):
        for switch in self.switches:
            self.settings.append(switch.is_active)
        self.is_start = True

    def draw_menu_help(self):
        self.pg_facade.draw_rectangle(100, 100, 1080, 520, (235, 66, 0))

        rules = ["-Поставьте камеру чтобы было видно корт и кольцо",
                 "-Постарайтесь играть одним мячом и быть единственным",
                 "игроком на площадке",
                 "-Программа будет регестрировать забитые и промахи",
                 "-После игры ваша статистика сохранится"]

        for i in range(len(rules)):
            self.pg_facade.draw_text(120, 120 + i * 70, rules[i], (0, 0, 0), 52)

    def menu_help(self):
        self.cur = "help"

    def draw_menu_settings(self):
        self.pg_facade.draw_rectangle(100, 100, 1080, 520, (235, 66, 0))

        settings = [
            "Показывать объект игрока",
            "Показывать объект мяча",
            "Показывать объект кольца",
            "Показывать точки на корте",
            "Показывать корт в левом верхнем углу"
        ]
        for switch in self.switches:
            switch.draw()
        for i, setting in enumerate(settings):
            self.pg_facade.draw_text(360, 140 + i * 75, setting, (0, 0, 0), 52)

    def menu_settings(self):
        self.cur = "settings"

    def update(self, event):
        if self.cur == "main":
            for button_name in ["start", "help", "settings"]:
                callback = self.buttons[button_name].update(event)
                if callable(callback):
                    callback()
        else:
            callback = self.buttons["back"].update(event)
            if callable(callback):
                callback()
            if self.cur == "settings":
                for switch in self.switches:
                    switch.update(event)


if __name__ == '__main__':
    pg.init()
    menu = Menu((1280, 720))
    clock = pg.time.Clock()
    clock.tick(60)
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            menu.update(event)
        menu.draw()


    pg.quit()