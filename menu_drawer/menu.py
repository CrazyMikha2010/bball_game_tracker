from pygame_facade import PygameFacade
import pygame as pg


class Menu():
    def __init__(self, screen_size: tuple):
        self.surface = pg.display.set_mode(screen_size)
        self.W = screen_size[0]
        self.H = screen_size[1]
        self.pg_facade = PygameFacade(screen_size)
        self.cur = "main"
        self.buttons = {}
        self.actions = {
            "main": self.draw_menu,
            "help": self.menu_help,
            "settings": self.menu_settings
        }

    def draw_buttons(self):
        self.cur = "main"
        self.buttons = {
            "start": self.pg_facade.draw_button(480, 300, 320, 80, "START", (235, 66, 0), (0, 0, 0), 120),
            "help": self.pg_facade.draw_button(480, 410, 320, 80, "HELP", (235, 66, 0), (0, 0, 0), 120),
            "settings": self.pg_facade.draw_button(480, 520, 320, 80, "SETTINGS", (235, 66, 0), (0, 0, 0), 90)
        }


    def menu_back(self):
        self.buttons["back"] = self.pg_facade.draw_button(15, 15, 200, 60, "BACK", (235, 66, 0), (0, 0, 0), 80)

    def menu_start(self):
        print("starting")

    def menu_help(self):
        self.cur = "help"
        self.pg_facade.clear_screen()
        self.pg_facade.draw_rectangle(100, 100, 1080, 520, (235, 66, 0))

        rules = ["-Поставьте камеру чтобы было видно корт и кольцо",
                 "-Постарайтесь играть одним мячом и быть единственным",
                 "игроком на площадке",
                 "-Программа будет регестрировать забитые и промахи",
                 "-После игры ваша статистика сохранится"]

        for i in range(len(rules)):
            self.pg_facade.draw_text(120, 120 + i * 70, rules[i], (0, 0, 0), 52)
        self.menu_back()

    def menu_settings(self):
        self.cur = "settings"
        self.pg_facade.clear_screen()
        self.pg_facade.draw_rectangle(100, 100, 1080, 520, (235, 66, 0))

        settings = [
            "Показывать объект игрока",
            "Показывать объект мяча",
            "Показывать объект кольца",
            "Показывать точки на корте",
            "Пкоазывать корт в левом верхнем углу"
        ]
        for i, setting in enumerate(settings):
            self.pg_facade.draw_text(120, 120 + i * 70, setting, (0, 0, 0), 52)
        self.menu_back()

    def handle_click(self, mouse_pos: tuple):
        if self.cur == "main":
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    if button_name == 'start':
                        return self.menu_start()
                    elif button_name == 'help':
                        self.menu_help()
                        break
                    elif button_name == 'settings':
                        self.menu_settings()
                        break

        elif self.cur in ["help", "settings"]:
            if self.buttons['back'].collidepoint(mouse_pos):
                self.cur = "main"
                self.draw_menu()


    def draw_menu(self):
        self.pg_facade.clear_screen()
        self.draw_buttons()


    def update(self, mouse: tuple):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                return self.handle_click(event.pos)

        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(mouse):
                pass

        return False

    def draw(self):
        self.actions[self.cur]()
        self.pg_facade.update_screen()


if __name__ == '__main__':
    pg.init()
    menu = Menu((1280, 720))
    clock = pg.time.Clock()
    clock.tick(60)
    running = True

    while running:
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                menu.handle_click(event.pos)

        menu.pg_facade.clear_screen()
        menu.draw()

    pg.quit()