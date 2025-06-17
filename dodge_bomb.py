import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect)->tuple[bool,bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：縦方向、横方向の画面内判定
    画面内ならTrue,外ならFalse
    """
    yoko,tate=True,True #初期値は画面の中
    if rct.left < 0 or WIDTH < rct.right: #画面の外に行ったとき(横方向)
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:#画面の外に行ったとき(縦方向)
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面上に「Game Over」
    と表示し、泣いているこうかとん画像を張り付ける
    """
    bc_img=pg.image.load("fig/8.png")

    black_img=pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT)) 
    black_img.set_alpha(150) #半透明
    black_rct = black_img.get_rect()
    screen.blit(black_img, black_rct)

    screen.blit(bc_img, [350,300])#右こうかとん
    screen.blit(bc_img,[720,300])#左こうかとん

    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    screen.blit(txt, [400, 300]) #文字
    pg.display.update() #表示
    time.sleep(5) #5秒間表示させる

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """
    sbb_accs = [a for a in range(1, 11)]
    acceleration=[]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        acceleration.append(bb_img)
    return acceleration,sbb_accs

# def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
#     """
#     移動量の合計値タプルに対応する向きの画像Surfaceを返す
#     """
#     if sum_mv[0]<0:
#         bg_img =pg.transform.flip(bg_img,True,False)

#def calc_orientation(org: pg.Rect, dst: pg.Rect,
#    current_xy: tuple[float, float]) -> tuple[float, float]:
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img=pg.Surface((20,20))  #爆弾用空のサーフェースを作る
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx=random.randint(0,WIDTH)
    bb_rct.centery=random.randint(0,HEIGHT)
    vx, vy = +5, +5  # 爆弾の移動速度
    bb_imgs, bb_accs = init_bb_imgs()
    print(bb_imgs, bb_accs)
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items(): #こうかとんの動き
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))
        
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx,avy)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
