from game import GameEngine
import engine

# definir cores
red   = (255, 0, 0)
green = (0, 255, 0)
blue  = (0, 0, 255)

class MyGame(GameEngine):
    def __init__(self, width, height):
        super().__init__(width, height)
        # Inicialize os elementos do jogo aqui
	
    def update(self):
        # Atualize a lógica do jogo específico aqui
        super().update()

    def render(self):
        super().render()
        # Renderize os elementos do jogo específico aqui
        self.screen.fill(red)  # Usando a cor RGB para azul
        engine.pygame.draw.rect(self.screen, (green), (40, 50, 70, 80))
        engine.pygame.display.flip()  # Atualiza a tela
	
def main():
    game = MyGame(300, 480)
    game.run()




