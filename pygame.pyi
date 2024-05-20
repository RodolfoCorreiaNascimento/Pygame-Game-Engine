# pygame.pyi

from typing import Tuple

# Módulo pygame
def init() -> None: ...
def display_set_mode(size: Tuple[int, int], *args, **kwargs) -> Surface: ...
# Adicione outras funções e métodos do módulo display do Pygame

# Módulo pygame.surface
class Surface: ...
# Adicione outras classes e métodos do Pygame, se necessário
