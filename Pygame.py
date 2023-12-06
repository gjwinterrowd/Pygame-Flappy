import sys
import pygame
import random
def draw_floor():
    screen.blit(floor_surface,(floor_x_position,720))
    screen.blit(floor_surface,(floor_x_position + 576,720))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos -175))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.top <= 0:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
        else:
            screen.blit(pipe_surface,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 720:
        return False
    return True
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(238, 685))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
screen = pygame.display.set_mode((576,800))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('comicsansms',40)

# Game Variables
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,400))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1500)
pipe_height = [300,350,400,450,500]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,400)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())


    screen.blit(bg_surface,(0,-100))
    screen.blit(floor_surface,(floor_x_position,720))

    if game_active:
    # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)

    # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
    else:
        high_score = update_score(score,high_score)
        score_display('game_over')

    # Floor
    floor_x_position -= .5
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)