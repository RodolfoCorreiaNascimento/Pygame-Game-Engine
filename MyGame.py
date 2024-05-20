from game import GameEngine
import engine

# Definir cores
red   = (255, 0, 0)
green = (0, 255, 0)
blue  = (0, 0, 255)

# Atributos do jogador
x = 30
y = 30

class MyGame(GameEngine):
    def __init__(self, width, height):
        super().__init__(width, height)
        # Inicialize os elementos do jogo aqui
	
    def update(self):
        global x  # Informe ao Python que estamos nos referindo à variável global x
        global y
        super().update()
        x += 1  # Atualize a posição do jogador
        y += 1
    
    def render(self):
        super().render()
        # Renderize os elementos do jogo aqui
        self.screen.fill(red)  # Usando a cor vermelha
        engine.pygame.draw.rect(self.screen, green, (x, y, 70, 80))  # Corrigido a posição do retângulo
        engine.pygame.display.flip()  # Atualiza a tela
	
def main():
    game = MyGame(300, 480)
    game.run()

if __name__ == "__main__":
    main()
