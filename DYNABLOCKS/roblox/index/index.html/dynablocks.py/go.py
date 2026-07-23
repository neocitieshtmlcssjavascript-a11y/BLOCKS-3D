import sys
import pygame

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DynaBlocks (Roblox 2004 Prototype) on Python")
clock = pygame.time.Clock()

# Цвета оригинального интерфейса 2004 года
COLOR_SKY = (175, 215, 255)
COLOR_GROUND = (60, 140, 60)
COLOR_BLOCK = (240, 200, 40)
COLOR_TEXT = (0, 0, 0)
COLOR_PANEL = (210, 210, 210)

# Физические параметры
GRAVITY = 0.5
blocks = []


# Класс для строительных блоков
class Block:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vy = 0
        self.is_grounded = False

    def update(self):
        if not self.is_grounded:
            self.vy += GRAVITY
            self.rect.y += self.vy

            # Проверка столкновения с землей (высота 500)
            if self.rect.bottom >= 500:
                self.rect.bottom = 500
                self.vy = 0
                self.is_grounded = True

            # Проверка столкновения с другими блоками сверху
            for other in blocks:
                if other != self and self.rect.colliderect(other.rect):
                    if self.vy > 0 and self.rect.bottom >= other.rect.top:
                        self.rect.bottom = other.rect.top
                        self.vy = 0
                        self.is_grounded = True


# Главный цикл
font = pygame.font.SysFont("Arial", 20)
running = True

while running:
    clock.tick(60)

    # Управление событиями
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Клик мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Левый клик: Спавн блока (только в зоне неба)
            if event.button == 1 and my < 500:
                # Выравнивание по сетке для стиля 2004 года
                grid_x = (mx // 40) * 40
                grid_y = (my // 40) * 40
                blocks.append(Block(grid_x, grid_y))

            # Правый клик: Удаление/разрушение блока
            elif event.button == 3:
                for b in blocks[:]:
                    if b.rect.collidepoint(mx, my):
                        blocks.remove(b)

    # Обновление физики блоков
    for block in blocks:
        block.update()

    # Отрисовка мира
    screen.fill(COLOR_SKY)  # Небо
    pygame.draw.rect(screen, COLOR_GROUND, (0, 500, WIDTH, 100))  # Земля

    # Рисуем все блоки
    for block in blocks:
        pygame.draw.rect(screen, COLOR_BLOCK, block.rect)
        pygame.draw.rect(screen, (0, 0, 0), block.rect, 2)  # Черная обводка

    # Интерфейс в стиле меню Альфа-версии 2004
    pygame.draw.rect(screen, COLOR_PANEL, (0, 0, WIDTH, 40))
    pygame.draw.line(screen, (100, 100, 100), (0, 40), (WIDTH, 40), 2)

    # Текст подсказок
    ui_text = "DYNABLOCKS 2004   |   ЛКМ: Создать блок   |   ПКМ: Удалить блок"
    text_surface = font.render(ui_text, True, COLOR_TEXT)
    screen.blit(text_surface, (15, 8))

    # Счетчик блоков
    count_text = font.render(f"Блоков: {len(blocks)}", True, COLOR_TEXT)
    screen.blit(count_text, (WIDTH - 120, 8))

    pygame.display.flip()

pygame.quit()
sys.exit()
