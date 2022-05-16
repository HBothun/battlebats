import pygame
import os

pygame.mixer.init()
pygame.font.init()

BGSOUND = pygame.mixer.Sound(os.path.join('battlebats/assets', 'Background.wav'))

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('battlebats/assets', 'Laser.wav'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('battlebats/assets', 'ouch.wav'))
EXPLOSION = pygame.mixer.Sound(os.path.join('battlebats/assets', 'Explosion.wav'))
EXPLOSION.set_volume(0.5)



pygame.display.set_icon(
    pygame.image.load(os.path.join('battlebats/assets','heart.png'))
    )
pygame.display.set_caption('Battle Bats!')

win = pygame.display.set_mode((900,500))

border = pygame.Rect(445, 0, 10, 500)

healthF = pygame.font.SysFont('comicsans', 40)
winnerF = pygame.font.SysFont('comicsans', 100)

fps = 60 
vel = 5
bvel = 7
maxbull = 10

lefthit = pygame.USEREVENT + 1
righthit = pygame.USEREVENT + 2

BAT1 = pygame.transform.rotate(
    pygame.image.load(os.path.join('battlebats/assets', 'cat.png')), 90)
BAT2 = pygame.transform.rotate(
    pygame.image.load(os.path.join('battlebats/assets', 'cat.png')), 270)
DEATH = pygame.image.load(os.path.join('battlebats/assets', 'fire.png'))

space = pygame.transform.scale(
    pygame.image.load(os.path.join('battlebats/assets', 'dackground.png')),
    (900, 500)
)


def drawindow(left, right, left_bullets, right_bullets, leftheal, rightheal):
    win.blit(space, (0,0))
    BGSOUND.set_volume(0.5)
    BGSOUND.play(-1)
    pygame.draw.rect(win, (150, 255, 125), border)

    leftheal_text = healthF.render('Health: ' + str(leftheal), 1, (0,255,0))
    rightheal_text = healthF.render('Health: ' + str(rightheal), 1, (0,255,0))
    win.blit(leftheal_text, (900 - leftheal_text.get_width() - 10, 10))
    win.blit(rightheal_text, (10, 10))


    win.blit(BAT1, (right.x, right.y))
    win.blit(BAT2, (left.x, left.y))



    for bullet in left_bullets:
        pygame.draw.rect(win, (255, 0, 0), bullet)

    for bullet in right_bullets:
        pygame.draw.rect(win, (0, 0, 255), bullet)

    pygame.display.update()

def leftmove(keyprss, left):
    if keyprss[pygame.K_a] and left.x - vel > 0: # Left
        left.x -= vel
    elif keyprss[pygame.K_d] and left.x + vel + left.width < border.x: # Right
        left.x += vel
    elif keyprss[pygame.K_w] and left.y - vel > 0: # Up
        left.y -= vel
    elif keyprss[pygame.K_s] and left.y + vel + left.height < 495: # Down
        left.y += vel

def rightmove(keyprss, right):
    if keyprss[pygame.K_LEFT] and right.x - vel > border.x + border.width: # Left
        right.x -= vel
    elif keyprss[pygame.K_RIGHT] and right.x + vel + right.width < 895: # Right
        right.x += vel
    elif keyprss[pygame.K_UP] and right.y - vel > 0: # Up
        right.y -= vel
    elif keyprss[pygame.K_DOWN] and right.y + vel + right.height < 495: # RDown
        right.y += vel


def handle_bullets(left_bullets, right_bullets, left, right):
    for bullet in left_bullets:
        bullet.x += bvel
        if right.colliderect(bullet):
            pygame.event.post(pygame.event.Event(righthit))
            left_bullets.remove(bullet)
        elif bullet.x > 900:
            left_bullets.remove(bullet)


    for bullet in right_bullets:
        bullet.x -= bvel
        if left.colliderect(bullet):
            pygame.event.post(pygame.event.Event(lefthit))
            right_bullets.remove(bullet)
        elif bullet.x < 0:
            right_bullets.remove(bullet)

def drawwinner(text):
    WinTe = winnerF.render(text, 1, (0,0,0))
    win.blit(WinTe, 
    (450 - WinTe.get_width()/2, 400 -WinTe.get_height()/2)
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    left = pygame.Rect(50, 225, 64, 64)
    right = pygame.Rect(800, 225, 64, 64)
    
    left_bullets=[]
    right_bullets=[]
    
    leftheal = 10
    rightheal = 10


    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(left_bullets) < maxbull:
                    bullet = pygame.Rect(left.x + left.width, left.y + left.height//2 - 2, 10, 5)
                    left_bullets.append(bullet)
                    pygame.mixer.Channel(1).play(BULLET_FIRE_SOUND)

                if event.key == pygame.K_RCTRL and len(right_bullets) < maxbull:
                    bullet = pygame.Rect(right.x + right.width, right.y + right.height//2 - 2, 10, 5)
                    right_bullets.append(bullet)
                    pygame.mixer.Channel(2).play(BULLET_FIRE_SOUND)
            if event.type == lefthit:
                rightheal -= 1
                pygame.mixer.Channel(3).play(BULLET_HIT_SOUND)

            if event.type == righthit:
                leftheal -= 1
                pygame.mixer.Channel(4).play(BULLET_HIT_SOUND)

        winner = ''
        if leftheal <= 0:
            win.blit(DEATH, (right.x, right.y))
            winner = 'LEFT WIN'
            pygame.mixer.Channel(5).play(EXPLOSION)
        if rightheal <=0:
            win.blit(DEATH, (left.x, left.y))
            winner = 'RIGHT WIN'
            pygame.mixer.Channel(5).play(EXPLOSION)
        if winner != '':
            drawwinner(winner)
            break



        keyprss = pygame.key.get_pressed()
    
        
        leftmove(keyprss, left)
        rightmove(keyprss, right)

        handle_bullets(left_bullets, right_bullets, left, right)

        drawindow(left, right, left_bullets, right_bullets, leftheal, rightheal)


    main()

if __name__ == '__main__':
    main()

