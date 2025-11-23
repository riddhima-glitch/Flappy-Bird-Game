import pygame
import random
import pygame_gui
import sys

pygame.init()

W = 600
H = 800
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird")

clk = pygame.time.Clock()
FPS = 60

# Colors
C_W = (255, 255, 255)
C_B = (0, 0, 0)

# Physics
G = 0.5
F = -10
P_SPD = 3
GAP = 180

ui = pygame_gui.UIManager((W, H))

try:
    # i_b = image_bird, i_p = image_pipe, i_bg = image_background
    i_b = pygame.image.load('bird.png').convert_alpha()
    i_p = pygame.image.load('pipe.png').convert_alpha()
    i_bg = pygame.image.load('background.png').convert()

    i_b = pygame.transform.scale(i_b, (60, 50))
    i_p = pygame.transform.scale(i_p, (70, i_p.get_height()))
    i_bg = pygame.transform.scale(i_bg, (W, H))

except pygame.error:
    print("Error: Images not found.")
    sys.exit()

class B(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = i_b
        self.rect = self.image.get_rect()
        self.rect.center = (100, H // 2)
        self.v = 0

    def j(self):
        self.v = F

    def upd(self):
        self.v += G
        self.rect.y += int(self.v)
        
        if self.v > 15:
            self.v = 15

        if self.rect.top < 0:
            self.rect.top = 0

class P:
    def __init__(self, x):
        self.x = x
        self.h = random.randint(50, H - 300)
        self.r_t = pygame.Rect(x, self.h - i_p.get_height() - (GAP // 2), 70, i_p.get_height())
        self.r_b = pygame.Rect(x, self.h + (GAP // 2), 70, i_p.get_height())
        self.ok = False

    def mv(self):
        self.x -= P_SPD
        self.r_t.x = self.x
        self.r_b.x = self.x

    def dr(self, s):
        s.blit(pygame.transform.flip(i_p, False, True), self.r_t)
        s.blit(i_p, self.r_b)

    def col(self, b):
        return self.r_t.colliderect(b.rect) or self.r_b.colliderect(b.rect)

def rst():
    b = B()
    ps = []
    sc = 0
    return b, ps, sc

def main():
    b, ps, sc = rst()
    over = False
    run = True
    t_last = pygame.time.get_ticks()
    btn = None

    fnt = pygame.font.Font(None, 40)

    while run:
        dt = clk.tick(FPS) / 1000.0
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            
            ui.process_events(e)

            if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE):
                if not over:
                    b.j()
                elif over and btn is None: 
                    b, ps, sc = rst()
                    over = False

            if e.type == pygame_gui.UI_BUTTON_PRESSED:
                if e.ui_element == btn:
                    b, ps, sc = rst()
                    over = False
                    btn.kill()
                    btn = None

        win.blit(i_bg, (0, 0))

        if not over:
            b.upd()

            t_now = pygame.time.get_ticks()
            if t_now - t_last > 1500:
                ps.append(P(W))
                t_last = t_now

            for p in ps:
                p.mv()
                p.dr(win)

                if p.col(b):
                    over = True
                
                if p.x + 70 < b.rect.x and not p.ok:
                    sc += 1
                    p.ok = True

            if ps and ps[0].x < -70:
                ps.pop(0)

            if b.rect.bottom >= H:
                over = True

        else:
            for p in ps:
                p.dr(win)
            
            if btn is None:
                btn = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((W//2 - 100, H//2 + 50), (200, 50)),
                    text='Play Again',
                    manager=ui
                )

            ovl = pygame.Surface((W, H))
            ovl.set_alpha(128)
            ovl.fill(C_B)
            win.blit(ovl, (0,0))
            
            txt = fnt.render(f"Game Over! Score: {sc}", True, C_W)
            win.blit(txt, (W//2 - txt.get_width()//2, H//2 - 50))

        win.blit(b.image, b.rect)
        
        s_txt = fnt.render(f"Score: {sc}", True, C_W)
        win.blit(s_txt, (10, 10))

        ui.update(dt)
        ui.draw_ui(win)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
