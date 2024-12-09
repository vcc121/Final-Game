import pygame, simpleGE, random

class Endpoint(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("green", (40, 40))
        self.position = (50, -500)

class Intro(simpleGE.Scene):
    def __init__(self, score = 0):
        super().__init__()
        
        self.background.fill("grey")
        self.status = "quit"
        self.score = score
        
        self.lblInstructions = simpleGE.MultiLabel()
        self.lblInstructions.textLines = [
            "You're behind the wheel!",
            "Using WASD controls, drive to the",
            "endpoints and avoid the barriers",
                "until you're out of time!"]
        self.lblInstructions.center = (320, 240)
        self.lblInstructions.size = (350, 200)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320, 100)
        self.lblScore.size = (350, 30)
        self.lblScore.text = f"Previous Score: {self.score}"
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.center = (150, 400)
        self.btnPlay.text = "Play"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (500, 400)
        self.btnQuit.text = "Quit"
        
        self.sprites = [
            self.lblScore,
            self.lblInstructions,
            self.btnPlay,
            self.btnQuit
            ]

    def process(self):
        if self.btnPlay.clicked:
            self.status = "play"
            self.stop()
        if self.btnQuit.clicked:
            self.status = "quit"
            self.stop()
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100,20)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (550,20)
        
class LblLevel(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Level: 1"
        self.center = (325,20)


class Wall(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("#9D8162", (0, 0))

class DrivyThing(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("car.png")
        self.setSize(50, 30)
        self.setAngle(45)
        self.width = 50
        self.height = 30
        self.boundAction = self.BOUNCE

    def process(self):
        if self.isKeyPressed(pygame.K_w):
            self.speed += .1
        if self.isKeyPressed(pygame.K_s):
            self.speed -= .1
        if self.isKeyPressed(pygame.K_a):
            self.imageAngle += 5
            self.moveAngle += 5
        if self.isKeyPressed(pygame.K_d):
            self.imageAngle -= 5
            self.moveAngle -= 5

        if self.speed > 5:
            self.speed = 5

        for barrier in self.scene.walls:
            if self.collidesWith(barrier):
                self.x -= self.dx * 2
                self.y -= self.dy * 2
                self.speed = 0

""" All print statements are for debugging purposes"""
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill("grey")
        self.setCaption("Reach the green endpoint!")
        self.drivy = DrivyThing(self)
        self.drivy.position = (600, 50)
        self.score = 0
        self.blip = simpleGE.Sound("blip sound.wav")
        self.lblScore = LblScore()
        self.lblLevel = LblLevel()
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 15
        self.lblTime = LblTime()
        self.endpoint = Endpoint(self)
        self.level = 1
        self.totalWalls = 93
        self.startingWalls = 7
        self.currentWalls = 7
        
        self.walls = []
        for i in range(self.totalWalls):
            self.walls.append(Wall(self))
        

        self.sprites = [self.endpoint, self.drivy, self.walls, self.lblScore, self.lblTime, self.lblLevel]
        self.createInitialBarriers()

    def process(self):
        if self.drivy.collidesWith(self.endpoint):
            self.score += (90 + (10*self.level) + (int(self.timer.getTimeLeft())*5))
            self.timer.totalTime += (4+self.level)
            self.nextLevel()

        self.lblScore.text = f"Score: {self.score}"
        self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2f}"
        self.lblLevel.text = f"Level: {self.level}"
        if self.timer.getTimeLeft() < 0:
            self.stop()

    def createInitialBarriers(self):
        for i in range(self.startingWalls):
            wall = Wall(self)
            wall_width = random.randint(20, 75 + self.level * 5)
            wall_height = random.randint(20, 75 + self.level * 5)
            wall.colorRect("#9D8162", (wall_width, wall_height))
            wall.position = (random.randint(100, 650), random.randint(100, 450))
            wall.visible = True
            self.walls.append(wall)
            self.sprites.append(wall)

        print(f"Total barriers created: {len(self.walls)} walls.")

    def adjustBarriers(self):
        max_wall_size = 75 + self.level * 5

        for i, wall in enumerate(self.walls):
            if i < self.currentWalls:
                wall_width = random.randint(20, max_wall_size)
                wall_height = random.randint(20, max_wall_size)
                wall_x = random.randint(50, 650)
                wall_y = random.randint(50, 450)

                car_area = pygame.Rect(self.drivy.x, self.drivy.y, self.drivy.width+10, self.drivy.height+10)
                wall_area = pygame.Rect(wall_x, wall_y, wall_width, wall_height)

                if not car_area.colliderect(wall_area):
                    wall.colorRect("#9D8162", (wall_width, wall_height))
                    wall.position = (wall_x, wall_y)
                    print(f"Updated barrier {i}: position=({wall_x}, {wall_y}), size=({wall_width}, {wall_height})")
                    

    def nextLevel(self):
        self.blip.play()
        self.level += 1
        self.drivy.position = (600, 50)
        self.drivy.speed = 0
        self.currentWalls += 3
        self.adjustBarriers()


def main():
    keepGoing = True
    score = 0
    
    while keepGoing:
        intro = Intro(score)
        intro.start()
        if intro.status == "quit":
            keepGoing = False
        else:
            game = Game()
            game.start()
            score = game.score


if __name__ == "__main__":
    main()