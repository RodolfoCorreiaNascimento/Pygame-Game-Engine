import pygame

class GameEngine:
    def __init__(self, width, height):
        pygame.init()  # Inicializa todos os módulos do Pygame
        self.screen = pygame.display.set_mode((width, height))  # Configura a tela com a largura e altura especificadas
        pygame.display.set_caption('Game Engine')  # Define o título da janela
        self.clock = pygame.time.Clock()  # Cria um objeto de controle de tempo
        self.running = True  # Define um indicador de execução do jogo

    def handle_events(self):
        # Processa todos os eventos (por exemplo, pressionar o botão fechar da janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o evento for de saída (fechar a janela)
                self.running = False  # Define running como False para sair do loop principal

    def update(self):
        # Placeholder para a lógica de atualização do jogo
        pass

    def render(self):
        # Placeholder para a lógica de renderização do jogo
        pass

    def run(self):
        # Loop principal do jogo
        while self.running:
            self.handle_events()  # Lida com eventos do usuário
            self.update()  # Atualiza o estado do jogo
            self.render()  # Renderiza o estado atualizado do jogo
            self.clock.tick(60)  # Controla a taxa de quadros para 60 FPS
        pygame.quit()  # Encerra todos os módulos do Pygame
