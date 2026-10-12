import pyxel


WIDTH = 160
HEIGHT = 120
PLAYER_Y = 106

player_x = 76
player_bullets = []
alien_bullets = []
aliens = []
score = 0
lives = 3
wave = 1
state = "title"
timer = 0
alien_direction = 1
alien_speed = 0.35
shot_cooldown = 0
stars = [(8, 18), (37, 11), (65, 20), (91, 9), (121, 17), (148, 12),
         (20, 59), (51, 48), (79, 64), (111, 55), (140, 70),
         (9, 91), (43, 83), (71, 101), (101, 89), (132, 96), (154, 43)]


def create_wave():
    global aliens, alien_bullets, player_bullets, alien_direction, alien_speed
    aliens = []
    for row in range(4):
        for column in range(8):
            aliens.append({
                "x": 20 + column * 15,
                "y": 25 + row * 11,
                "row": row,
                "alive": True,
            })
    alien_bullets = []
    player_bullets = []
    alien_direction = 1
    alien_speed = min(0.35 + (wave - 1) * 0.08, 1.2)


def start_game():
    global player_x, score, lives, wave, state, timer, shot_cooldown
    player_x = 76
    score = 0
    lives = 3
    wave = 1
    timer = 0
    shot_cooldown = 0
    create_wave()
    state = "playing"


def update():
    global player_x, score, lives, state, timer, alien_direction
    global shot_cooldown, wave

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    if state == "title":
        if (
            pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.KEY_RETURN)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
        ):
            start_game()
        return

    if state in ("gameover", "clear"):
        timer += 1
        if state == "clear" and timer >= 45:
            wave += 1
            create_wave()
            state = "playing"
        elif state == "gameover" and (
            pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.KEY_RETURN)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
        ):
            start_game()
        return

    if (
        pyxel.btn(pyxel.KEY_LEFT)
        or pyxel.btn(pyxel.KEY_A)
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
    ):
        player_x = max(4, player_x - 2)
    if (
        pyxel.btn(pyxel.KEY_RIGHT)
        or pyxel.btn(pyxel.KEY_D)
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
    ):
        player_x = min(WIDTH - 12, player_x + 2)

    shot_cooldown = max(0, shot_cooldown - 1)
    if (
        pyxel.btn(pyxel.KEY_SPACE)
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)
    ) and shot_cooldown == 0:
        player_bullets.append([player_x + 4, PLAYER_Y - 2])
        shot_cooldown = 12

    for bullet in player_bullets:
        bullet[1] -= 3
    player_bullets[:] = [bullet for bullet in player_bullets if bullet[1] > 4]

    living_aliens = [alien for alien in aliens if alien["alive"]]
    if not living_aliens:
        state = "clear"
        timer = 0
        return

    hit_edge = any(
        alien["x"] + alien_direction * alien_speed < 5
        or alien["x"] + alien_direction * alien_speed > WIDTH - 13
        for alien in living_aliens
    )
    if hit_edge:
        alien_direction *= -1
        for alien in living_aliens:
            alien["y"] += 3
            if alien["y"] >= PLAYER_Y - 8:
                state = "gameover"
                timer = 0
                return

    for alien in living_aliens:
        alien["x"] += alien_direction * alien_speed

    for bullet in player_bullets[:]:
        for alien in living_aliens:
            if (
                alien["alive"]
                and alien["x"] <= bullet[0] <= alien["x"] + 8
                and alien["y"] <= bullet[1] <= alien["y"] + 6
            ):
                alien["alive"] = False
                player_bullets.remove(bullet)
                score += (4 - alien["row"]) * 10
                break

    if pyxel.frame_count % max(18, 52 - wave * 3) == 0:
        shooter = living_aliens[pyxel.rndi(0, len(living_aliens) - 1)]
        alien_bullets.append([shooter["x"] + 4, shooter["y"] + 7])

    for bullet in alien_bullets:
        bullet[1] += 2 + min(wave // 3, 2)
    alien_bullets[:] = [bullet for bullet in alien_bullets if bullet[1] < HEIGHT]

    for bullet in alien_bullets[:]:
        if (
            player_x - 1 <= bullet[0] <= player_x + 9
            and PLAYER_Y - 2 <= bullet[1] <= PLAYER_Y + 5
        ):
            alien_bullets.remove(bullet)
            lives -= 1
            if lives <= 0:
                state = "gameover"
                timer = 0
                return


def draw_alien(x, y, color, kind):
    x = int(x)
    y = int(y)
    pyxel.rect(x + 2, y, 4, 1, color)
    pyxel.rect(x + 1, y + 1, 6, 2, color)
    pyxel.rect(x, y + 3, 8, 2, color)
    pyxel.rect(x + 1, y + 5, 2, 1, color)
    pyxel.rect(x + 5, y + 5, 2, 1, color)
    pyxel.pset(x + 2, y + 2, 0)
    pyxel.pset(x + 5, y + 2, 0)
    if kind % 2 == 0:
        pyxel.rect(x - 1, y + 3, 1, 2, color)
        pyxel.rect(x + 8, y + 3, 1, 2, color)


def draw_player(x, y):
    pyxel.rect(x + 3, y, 2, 2, 11)
    pyxel.rect(x + 2, y + 2, 4, 2, 11)
    pyxel.rect(x, y + 4, 8, 2, 11)
    pyxel.rect(x + 2, y + 6, 1, 1, 11)
    pyxel.rect(x + 5, y + 6, 1, 1, 11)


def draw():
    pyxel.cls(1)
    for x, y in stars:
        pyxel.pset(x, y, 5)

    if state == "title":
        pyxel.text(48, 22, "SPACE INVADERS", 10)
        draw_alien(76, 43, 8, 0)
        draw_player(76, 72)
        pyxel.text(33, 91, "SPACE / A: START", 7)
        pyxel.text(19, 103, "ARROWS / A,D OR D-PAD", 6)
        return

    pyxel.text(5, 5, "SCORE", 7)
    pyxel.text(5, 13, str(score).rjust(5, "0"), 10)
    pyxel.text(66, 5, "WAVE " + str(wave), 7)
    pyxel.text(127, 5, "LIFE", 7)
    for index in range(lives):
        draw_player(130 + index * 9, 15)

    for alien in aliens:
        if alien["alive"]:
            colors = (8, 11, 9, 10)
            draw_alien(alien["x"], alien["y"], colors[alien["row"]], alien["row"])

    draw_player(player_x, PLAYER_Y)
    for x, y in player_bullets:
        pyxel.rect(x, y, 1, 4, 10)
    for x, y in alien_bullets:
        pyxel.rect(x, y, 2, 4, 8)
    pyxel.line(0, 116, WIDTH - 1, 116, 5)

    if state == "clear":
        pyxel.rect(35, 51, 90, 19, 1)
        pyxel.rectb(35, 51, 90, 19, 10)
        pyxel.text(62, 58, "WAVE CLEAR!", 10)
    elif state == "gameover":
        pyxel.rect(31, 48, 98, 27, 1)
        pyxel.rectb(31, 48, 98, 27, 8)
        pyxel.text(57, 54, "GAME OVER", 8)
        pyxel.text(31, 65, "SPACE / A TO RESTART", 7)


pyxel.init(WIDTH, HEIGHT, title="Space Invaders")
pyxel.run(update, draw)
