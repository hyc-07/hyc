import pygame
import random
import time
import sys
import os.path
import ctypes

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# 初始化全局变量
start_time = 0
click_t = 0
FPS = 80
choice = "C"
mode = "original"  # 默认模式为"original"，可选"endless"

# 颜色定义
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

width = 1000
height = 600

# 游戏变量
play_time = 0  # 初始化游玩时间
level_tp = 20
shot = 0.15
last_shot = 0
kill = 0
score = 0
win_time = 83

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("hyc_game")

# 字体
big_font = pygame.font.SysFont("Arial",60)
font = pygame.font.SysFont("Arial", 48)
small_font = pygame.font.SysFont("Arial", 35)

# 加载音效（确保路径正确）
sound_e = pygame.mixer.Sound(get_resource_path("sounds/6.wav"))
sound_e.set_volume(0.3)

# 玩家设置
player_size = 60
player_x = width // 2 - player_size // 2
player_y = height - player_size
player_speed = 10
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
player_h = 3

# 敌机和子弹
all_e = []
e_size = 45
e_speed = 12
e_y = -e_size

all_eg = []
eg_size = 45
eg_speed = 12
eg_y = -eg_size

all_b = []
b_w = 8
b_h = 15
b_speed = 18
b_y = height - player_size

P_get_EG = 250
P_get_E = 25

# 游戏状态
running = True
draw = True
wait_2 = True
wait_3 = True
menu_wait = True
spawn_eg = True
spawn_e = True
blit_win = False
hint_text = None

# 全文字
wait_2_text = font.render("hyc_v1.3.2", True, black)
wait_2_text_rect = wait_2_text.get_rect(center=(width // 2, (height // 2) - 60))
wait_2_text2 = small_font.render("start", True, black)
wait_2_text2_rect = wait_2_text2.get_rect(center=((width // 2) - 50, (height // 2)))
wait_3_text = small_font.render("setting", True, black)
wait_3_text_rect = wait_2_text2.get_rect(center=((width // 2) - 50, (height // 2) + 5 * 8))
wait_2_text3 = small_font.render("v1.3.2", True, black)
wait_2_text3_rect = wait_2_text3.get_rect(bottomright=(width, height - 40))
wait_2_text4 = small_font.render("Creator:hyc", True, black)
wait_2_text4_rect = wait_2_text4.get_rect(bottomright=(width, height - 5))
clock = pygame.time.Clock()

pygame.mixer.music.load(get_resource_path("sounds/menu.mp3"))
pygame.mixer.music.set_volume(1.3)
pygame.mixer.music.play(-1)

while running:
    menu_wait = True
    while wait_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                wait_2 = False
                draw = False
                break

        keys = pygame.key.get_pressed()
        (m_1, m_2, m_3) = pygame.mouse.get_pressed()
        if m_1:
            (m_x, m_y) = pygame.mouse.get_pos()
            if wait_2_text2_rect.collidepoint(m_x, m_y):
                start_time = time.time()
                wait_2 = False
                P_get_EG = 250
                if choice == "A":
                    pygame.mixer.music.load(get_resource_path("sounds/1x.mp3"))
                    pygame.mixer.music.set_volume(1.5)
                elif choice == "B":
                    pygame.mixer.music.load(get_resource_path("sounds/nrun.mp3"))
                    pygame.mixer.music.set_volume(1.7)
                else:
                    pygame.mixer.music.load(get_resource_path("sounds/plead.mp3"))
                    pygame.mixer.music.set_volume(1.3)

                # 根据模式设置音乐循环
                if mode == "endless":
                    pygame.mixer.music.play(-1)  # 无尽模式循环播放
                else:
                    pygame.mixer.music.play(1)  # 原始模式播放一次
                break  # 退出并进入游戏循环
            if wait_3_text_rect.collidepoint(m_x, m_y):
                wait_3 = True
                while wait_3:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    wait_3_text1 = small_font.render(f"music: {choice}", True, black)
                    wait_3_text1_rect = wait_3_text1.get_rect(topleft=(10, height // 8))
                    wait_3_text4 = small_font.render(f"mode: {mode}", True, black)  # 新增：模式选择
                    wait_3_text4_rect = wait_3_text4.get_rect(topleft=(10, (height // 8) + 50))
                    wait_3_text2 = small_font.render("Click to change", True, black)
                    wait_3_text2_rect = wait_3_text2.get_rect(topleft=(10, (height // 8) + 100))
                    wait_3_text3 = small_font.render("Press Q to quit", True, black)
                    wait_3_text3_rect = wait_3_text3.get_rect(topleft=(10, (height // 8) + 150))

                    screen.fill(white)
                    screen.blit(wait_3_text1, wait_3_text1_rect)
                    screen.blit(wait_3_text2, wait_3_text2_rect)
                    screen.blit(wait_3_text3, wait_3_text3_rect)
                    screen.blit(wait_3_text4, wait_3_text4_rect)  # 新增：显示模式选择

                    (m_1, m_2, m_3) = pygame.mouse.get_pressed()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_q]:
                        wait_3 = False
                        break
                    if m_1 and click_t + 0.3 < time.time():
                        (m_x, m_y) = pygame.mouse.get_pos()
                        if wait_3_text1_rect.collidepoint(m_x, m_y):
                            click_t = time.time()
                            if choice == "A":
                                choice = "B"
                            elif choice == "B":
                                choice = "C"
                            else:
                                choice = "A"
                        elif wait_3_text4_rect.collidepoint(m_x, m_y):  # 新增：模式切换
                            click_t = time.time()
                            mode = "endless" if mode == "original" else "original"
                    clock.tick(FPS)
                    pygame.display.update()
        screen.fill(white)
        screen.blit(wait_2_text, wait_2_text_rect)
        screen.blit(wait_2_text2, wait_2_text2_rect)
        screen.blit(wait_2_text3, wait_2_text3_rect)
        screen.blit(wait_3_text, wait_3_text_rect)
        screen.blit(wait_2_text4, wait_2_text4_rect)
        pygame.display.update()
        clock.tick(FPS)

    # 游戏循环
    if play_time > level_tp and P_get_E >= 16:
        level_tp += 35
        P_get_E -= 9

    # 修改胜利文本显示逻辑 - 只在原始模式下显示
    if mode == "original" and win_time + 1 <= play_time:
        text = "you "
        if play_time >= 1.7 + win_time:
            text += "are "
        if play_time >= 2.3 + win_time:
            text += "win"
        if play_time >= 4 + win_time:
            text = "and now "
        if play_time >= 5 + win_time:
            text = "get out of my game"
            # 添加返回主界面的提示
            hint_text = small_font.render("Press N to return to menu", True, black)
            hint_rect = hint_text.get_rect(center=(width // 2, height // 2 + 50))
        if play_time >= 7 + win_time:
            text = "3"
        if play_time >= 8.2 + win_time:
            text = "2"
        if play_time >= 9.4 + win_time:
            text = "1"
        if play_time >= 10.4 + win_time:
            text = "fine"
        if play_time >= 11.7 + win_time:
            text = "good bye,hahaha"
        if play_time >= 14 + win_time:
            pygame.quit()
            if os.name == "nt":
                ctypes.windll.user32.MessageBoxW(0,"application error","error",0x10,)
                for i in range(3):
                    ctypes.windll.user32.MessageBoxW(0,"you are an idiot","error",0x10,)
                    ctypes.windll.user32.MessageBoxW(0,"hahahahaha","error",0x30,)
            sys.exit()
        win_text = font.render(text, True, black)
        win_text_rect = win_text.get_rect(center=(width // 2, height // 2))
        blit_win = True
        # 检测是否按下M键返回主界面
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            # 重置音乐
            pygame.mixer.music.stop()
            # 重置游戏状态
            hint_text = None
            running = True
            draw = True
            menu_wait = False
            wait_2 = True
            wait_3 = True
            kill = 0
            score = 0
            start_time = time.time()
            play_time = 0
            player_x = width // 2 - player_size // 2
            player_h = 3
            all_e = []
            all_b = []
            all_eg = []
            pygame.mixer.music.load(get_resource_path("sounds/menu.mp3"))
            pygame.mixer.music.set_volume(1.2)
            pygame.mixer.music.play(-1)
            continue  # 跳过当前循环，返回主菜单
    elif mode == "original" and play_time >= win_time:
        spawn_e, spawn_eg = False, False
    else:
        blit_win = False

    t_now = time.time()
    play_time = t_now - start_time  # 计算游玩时间
    player_h_text = font.render(f"HP:{player_h}", True, black)
    player_h_text_rect = player_h_text.get_rect()
    if play_time <= win_time or mode == "endless":  # 无尽模式持续计分
        score = int(t_now - start_time) + 2 * kill
    score_text = font.render(f"score:{score}", True, black)
    score_text_rect = score_text.get_rect()
    score_text_rect.topleft = player_h_text_rect.bottomleft

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 键盘控制保留（用于调试）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
        pygame.mixer.music.stop()

    # === 新版移动控制 ===
    # 左移控制（带边界检测）
    if keys[pygame.K_a]:
        player_x = max(0, player_x - player_speed)

    # 右移控制（带边界检测）
    if keys[pygame.K_d]:
        player_x = min(width - player_size, player_x + player_speed)

    # 强制边界约束（最终保障）
    player_x = max(0, min(width - player_size, player_x))
    player_rect.x = player_x

    # 射击控制
    if keys[pygame.K_SPACE] and t_now - last_shot >= shot:
        pygame.mixer.Sound(get_resource_path("sounds/1.wav")).play()
        b_x = player_x + player_size // 2 - b_w // 2
        all_b.append(pygame.Rect(b_x, b_y, b_w, b_h))
        last_shot = t_now

    # 敌机生成逻辑
    if random.randint(1, P_get_EG) == 1 and (spawn_eg or mode == "endless"):  # 无尽模式持续生成敌机
        eg_x = random.randint(0, width - eg_size)
        all_eg.append(pygame.Rect(eg_x, eg_y, eg_size, eg_size))
    if random.randint(1, P_get_E) == 1 and (spawn_e or mode == "endless"):  # 无尽模式持续生成敌机
        e_x = random.randint(0, width - e_size)
        all_e.append(pygame.Rect(e_x, e_y, e_size, e_size))

    player_rect.x = player_x
    screen.fill(white)

    # 更新子弹
    for b_self in all_b[:]:
        pygame.draw.rect(screen, blue, b_self)
        b_self.y -= b_speed
        if b_self.y < -b_h:
            all_b.remove(b_self)
        for eg_self in all_eg[:]:
            if b_self.colliderect(eg_self):
                player_h += 1
                all_eg.remove(eg_self)
                pygame.mixer.Sound(get_resource_path("sounds/5.wav")).play()

    # 更新绿色敌机
    for eg_self in all_eg[:]:
        pygame.draw.rect(screen, green, eg_self)
        eg_self.y += eg_speed * (1 / FPS) * 60
        if eg_self.top > height:
            all_eg.remove(eg_self)
        elif eg_self.colliderect(player_rect):
            player_h += 1
            all_eg.remove(eg_self)
            pygame.mixer.Sound(get_resource_path("sounds/5.wav")).play()

    # 更新红色敌机
    for e_self in all_e[:]:
        pygame.draw.rect(screen, red, e_self)
        e_self.y += e_speed * (1 / FPS) * 60
        if e_self.top > height:
            all_e.remove(e_self)
        elif e_self.colliderect(player_rect):
            if player_h == 1:
                player_h -= 1
                pygame.mixer.Sound(get_resource_path("sounds/3.wav")).play()
                pygame.mixer.music.stop()
                running = False
                wait = True
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            wait = False
                            draw = False
                            running = False
                            pygame.quit()
                            sys.exit()
                    wait_replay_text = big_font.render("DAMAGE!", True, black)
                    wait_replay_text_rect = wait_replay_text.get_rect(center=(width // 2, (height // 2) - 80))
                    wait_score_text = font.render(f"score:{score}",True,black)
                    wait_score_text_rect = wait_score_text.get_rect(center=(width//2,(height//2)-20))
                    replay_text = small_font.render("respawn", True, black)
                    replay_text_rect = replay_text.get_rect(center=(width // 2, (height // 2)+83))
                    ret_text = small_font.render("main menu", True, black)
                    ret_text_rect = ret_text.get_rect(center=(width // 2, (height // 2)+45))
                    (m_1, m_2, m_3) = pygame.mouse.get_pressed()
                    if m_1:
                        (m_x, m_y) = pygame.mouse.get_pos()
                        if ret_text_rect.collidepoint(m_x, m_y):
                            running = True
                            draw = True
                            menu_wait = False
                            wait_1 = True
                            wait_2 = True
                            wait_3 = True
                            kill = 0
                            score = 0
                            start_time = time.time()
                            play_time = 0
                            player_x = width // 2 - player_size // 2
                            player_h = 3
                            all_e = []
                            all_b = []
                            all_eg = []
                            pygame.mixer.music.load(get_resource_path("sounds/menu.mp3"))
                            pygame.mixer.music.set_volume(1.2)
                            pygame.mixer.music.play(-1)
                            break
                        if replay_text_rect.collidepoint(m_x,m_y):
                            # 重置游戏状态,replay
                            player_h = 3
                            all_e = []
                            all_b = []
                            last_shot = 0
                            kill = 0
                            start_time = time.time()
                            player_x = width // 2 - player_size // 2
                            score = 0
                            pygame.mixer.music.play(-1)
                            running = True
                            wait = False
                            menu_wait = False

                    screen.fill(white)
                    screen.blit(wait_replay_text,wait_replay_text_rect)
                    screen.blit(replay_text, replay_text_rect)
                    screen.blit(ret_text, ret_text_rect)
                    screen.blit(wait_score_text,wait_score_text_rect)
                    pygame.display.update()
                    clock.tick(FPS)
            else:
                player_h -= 1
                all_e.remove(e_self)
                pygame.mixer.Sound(get_resource_path("sounds/2.wav")).play()

    # 检测子弹碰撞
    for e_self in all_e[:]:
        for b_self in all_b[:]:
            if b_self.colliderect(e_self):
                all_e.remove(e_self)
                kill += 1
                sound_e.play()
                break

    if draw and menu_wait:
        pygame.draw.rect(screen, black, player_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(player_h_text, player_h_text_rect)
        if blit_win:
            screen.blit(win_text, win_text_rect)
            if hint_text is not None:
                screen.blit(hint_text, hint_rect)
        pygame.display.update()
    clock.tick(FPS)
pygame.quit()