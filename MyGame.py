from engine import GameEngine
import pygame

# Definir cores
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class MyGame(GameEngine):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.x = 30  # Inicializa como atributo de instância
        self.y = 30  # Inicializa como atributo de instância

    def update(self):
        super().update()
        self.x += 1  # Atualize a posição do jogador
        self.y += 1

    def render(self):
        super().render()
        self.screen.fill(red)  # Usando a cor vermelha
        pygame.draw.rect(self.screen, blue, (self.x, self.y, 70, 80))  # Desenha um retângulo verde
        pygame.display.flip()  # Atualiza a tela

def main():
    game = MyGame(300, 480)
    game.run()

if __name__ == "__main__":
    main()





