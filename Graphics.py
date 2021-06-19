import time
import pygame
import CSP


class Graphics:
    def __init__(self, tablesList, steps, n):
        self.tablesList = tablesList
        self.steps = steps
        self.__one = pygame.image.load("./pictures/1.png")
        self.__right = pygame.image.load("./pictures/right.png")
        self.__noAnswer = pygame.image.load("./pictures/noAnswer.jpg")
        self.__left = pygame.image.load("./pictures/left.png")
        self.__zero = pygame.image.load("./pictures/0.png")
        self.__empty = pygame.image.load("./pictures/-.png")
        self.__background = pygame.image.load("./pictures/bg.jpg")
        self.__transparent = pygame.image.load("./pictures/yellow.png")
        self.__n = n
        self.__height = 700
        self.__lenght = 460
        self.__scale = 380 // n
        self.__screen = None

    def display(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__lenght, self.__height))
        self.__background = pygame.transform.scale(self.__background, (self.__lenght, self.__height))
        self.__one = pygame.transform.scale(self.__one, (self.__scale, self.__scale))
        self.__left = pygame.transform.scale(self.__left, (80, 40))
        self.__noAnswer = pygame.transform.scale(self.__noAnswer, (300, 100))
        self.__right = pygame.transform.scale(self.__right, (80, 40))
        self.__zero = pygame.transform.scale(self.__zero, (self.__scale, self.__scale))
        self.__empty = pygame.transform.scale(self.__empty, (self.__scale, self.__scale))
        self.__transparent = pygame.transform.scale(self.__transparent, (self.__scale, self.__scale))
        x = 0.5 * (self.__lenght - self.__n * self.__scale)
        y = 0.5 * (self.__height - self.__n * self.__scale)
        buttonLeft = pygame.Rect(50, 600, 80, 40)
        buttonRight = pygame.Rect(340, 600, 80, 40)
        # win = pygame.display.set_mode((200, 600))

        step = 0
        changed = True
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if buttonLeft.collidepoint(mouse_pos):
                        print('button Left was pressed at {0}'.format(mouse_pos))
                        if step > 0:
                            step = step - 1
                        changed = True

                    elif buttonRight.collidepoint(mouse_pos):
                        print('button Right was pressed at {0}'.format(mouse_pos))
                        if step < len(self.tablesList) - 1:
                            step = step + 1
                        changed = True

            if changed:
                self.__screen.blit(self.__background, (0, 0))
                if len(self.tablesList)==1:
                    self.__screen.blit(self.__noAnswer, (80, 50))
                pygame.draw.rect(self.__screen, [71, 75, 122], buttonLeft)
                pygame.draw.rect(self.__screen, [71, 75, 122], buttonRight)
                self.__screen.blit(self.__left, (50, 600))
                self.__screen.blit(self.__right, (340, 600))

                for row in range(len(self.tablesList[step])):
                    for item in range(len(self.tablesList[step][row])):

                        if 'R' in self.steps[step] and int(self.steps[step][1:]) == row:
                            self.__screen.blit(self.__transparent, (x + item * self.__scale, y + row * self.__scale))
                        elif 'C' in self.steps[step] and int(self.steps[step][1:]) == item:
                            self.__screen.blit(self.__transparent, (x + item * self.__scale, y + row * self.__scale))
                        else:
                            pass
                        if self.tablesList[step][row][item] == '-':
                            self.__screen.blit(self.__empty, (x + item * self.__scale, y + row * self.__scale))
                        elif self.tablesList[step][row][item] == 1 or self.tablesList[step][row][item] == '1':
                            self.__screen.blit(self.__one, (x + item * self.__scale, y + row * self.__scale))
                        elif self.tablesList[step][row][item] == 0 or self.tablesList[step][row][item] == '0':
                            self.__screen.blit(self.__zero, (x + item * self.__scale, y + row * self.__scale))

                        pygame.display.update()
                pygame.time.Clock().tick(200)
                changed = False