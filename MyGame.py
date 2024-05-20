from game import GameEngine
import engine

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
        #engine.pygame.screen.fill((0, 0, 255))  # Usando a cor RGB para azul
        engine.pygame.display.flip()  # Atualiza a tela
	

def main():
    game = MyGame(300, 480)
    game.run()



