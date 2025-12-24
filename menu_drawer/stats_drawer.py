import pygame as pg

class statsDrawer():
    def __init__(self, facade):
        self.facade = facade
        self.font_size = 32

    def draw_score(self, score: int):
        self.facade.draw_rectangle(1170, 650, 100, 50, (235, 66, 0), 10)
        self.facade.draw_text(1180, 665, f"Score: {score}", (0, 0, 0), self.font_size)

    def draw_stats(self, stats):
        """
        FGM field goals made
        FGA field goals attempted
        FG% field goal percentage (FGM / FGA) * 100
        2PM 2-point field goal made
        2PA 2-point field goal attempted
        2P% 2-point field goal percentage
        3PM 3-point field goal made
        3PA 3-point field goal attempted
        3P% 3-point field goal percentage
        """
        for i in range(3):
            self.facade.draw_rectangle(1170, 10 + i * 200, 100, 150, (235, 66, 0), 10)
        for i, (stat, name) in enumerate(zip(stats, ["FGM", "FGA", "FG%", "2PM", "2PA", "2P%", "3PM", "3PA", "3P%"])):
            self.facade.draw_text(1180, 35 + (i//3) * 200 + (i%3) * 40, f"{name} {stat}", (0, 0, 0), self.font_size)

    def draw_in3pts(self, yes: bool):
        self.facade.draw_text(1180, 620, f"{2+1*yes}pts", (255, 255, 255), self.font_size)

    def draw_flying(self, yes: bool):
        self.facade.draw_text(1180, 580, f'{"in air" if yes else "dribbled"}', (255, 255, 255), self.font_size)
