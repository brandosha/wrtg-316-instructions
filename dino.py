import curses
import os
import random
import time

HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dino_highscore.txt")

MIN_HEIGHT, MIN_WIDTH = 16, 50
DINO_X = 4
GRAVITY = 0.11
JUMP_SPEED = 1.3
FAST_FALL = 0.5  # extra pull down when you press DOWN in the air
DUCK_TICKS = 10  # how long one tap of DOWN keeps you ducked

JUMP_KEYS = {ord(" "), curses.KEY_UP, ord("w"), ord("W")}
DUCK_KEYS = {curses.KEY_DOWN, ord("s"), ord("S")}
PAUSE_KEYS = {ord("p"), ord("P")}
QUIT_KEYS = {ord("q"), ord("Q")}

# ---------- Pictures (spaces are see-through) ----------
DINO_RUN = [
    ["    __ ", "\\__/ o)", "  /  \\ "],
    ["    __ ", "\\__/ o)", "   ||  "],
]
DINO_DUCK = [
    ["\\___.-o)", "  /  \\  "],
    ["\\___.-o)", "   ||   "],
]
CACTUS_SMALL = ["\\|/", " | "]
CACTUS_TALL = ["\\| ", " |/", " | "]
BIRD = [["\\v/"], ["-v-"]]
CLOUD = [" .-~-. ", "(_____)"]

LETTERS = {
    "D": [" ___  ", "|   \\ ", "| |) |", "|___/ "],
    "I": [" ___ ", "|_ _|", " | | ", "|___|"],
    "N": [" _  _ ", "| \\| |", "| .` |", "|_|\\_|"],
    "O": ["  ___  ", " / _ \\ ", "| (_) |", " \\___/ "],
    "R": [" ___ ", "| _ \\", "|   /", "|_|_\\"],
    "U": [" _   _ ", "| | | |", "| |_| |", " \\___/ "],
    " ": ["  ", "  ", "  ", "  "],
}
BANNER = [" ".join(LETTERS[ch][row] for ch in "DINO RUN") for row in range(4)]

COLORS = {}


# ---------- Helpers ----------
def setup_colors():
    colors = {
        "dino": curses.COLOR_CYAN,
        "cactus": curses.COLOR_GREEN,
        "bird": curses.COLOR_MAGENTA,
        "danger": curses.COLOR_RED,
        "title": curses.COLOR_GREEN,
        "flash": curses.COLOR_MAGENTA,
    }
    extra = {"dino": curses.A_BOLD, "cactus": curses.A_BOLD, "danger": curses.A_BOLD,
             "title": curses.A_BOLD, "flash": curses.A_BOLD}
    use_color = curses.has_colors()
    if use_color:
        curses.start_color()
        background = -1
        try:
            curses.use_default_colors()
        except curses.error:
            background = curses.COLOR_BLACK
    for i, (name, fg) in enumerate(colors.items(), start=1):
        attr = extra.get(name, 0)
        if use_color:
            curses.init_pair(i, fg, background)
            attr |= curses.color_pair(i)
        COLORS[name] = attr
    COLORS["cloud"] = curses.A_DIM
    COLORS["ground"] = 0
    COLORS["score"] = curses.A_BOLD


def text(screen, y, x, s, attr=0):
    """Write a line of text, cutting off anything that falls off the screen."""
    h, w = screen.getmaxyx()
    if 0 <= y < h and x < w - 1:
        if x < 0:
            s, x = s[-x:], 0
        try:
            screen.addstr(y, x, s[: w - 1 - x], attr)
        except curses.error:
            pass


def draw(screen, y, x, rows, attr=0):
    """Draw a picture, skipping spaces so things behind it still show."""
    h, w = screen.getmaxyx()
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            yy, xx = y + dy, x + dx
            if ch != " " and 0 <= yy < h and 0 <= xx < w - 1:
                try:
                    screen.addstr(yy, xx, ch, attr)
                except curses.error:
                    pass


def cells(y, x, rows):
    """Every screen spot a picture covers, used to check for crashes."""
    return {(y + dy, x + dx) for dy, row in enumerate(rows) for dx, ch in enumerate(row) if ch != " "}


def center(screen, y, s, attr=0):
    text(screen, y, (screen.getmaxyx()[1] - len(s)) // 2, s, attr)


def too_small(screen):
    h, w = screen.getmaxyx()
    if h >= MIN_HEIGHT and w >= MIN_WIDTH:
        return False
    screen.erase()
    center(screen, h // 2, "Make the window bigger!", COLORS["danger"])
    center(screen, h // 2 + 1, f"(need {MIN_WIDTH}x{MIN_HEIGHT}, have {w}x{h})")
    screen.refresh()
    return True


def load_best():
    try:
        with open(HIGHSCORE_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_best(best):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(best))
    except OSError:
        pass


def new_obstacle(x, score):
    kinds = ["small", "small", "tall"]
    if score > 150:
        kinds.append("group")
    if score > 300:
        kinds += ["bird", "bird"]
    kind = random.choice(kinds)

    if kind == "small":
        frames, elev, color = [CACTUS_SMALL], 0, "cactus"
    elif kind == "tall":
        frames, elev, color = [CACTUS_TALL], 0, "cactus"
    elif kind == "group":
        n = random.choice([2, 3])
        frames, elev, color = [[" ".join([row] * n) for row in CACTUS_SMALL]], 0, "cactus"
    else:
        # height 1 = jump over it, 2 = duck under it, 4 = don't jump into it
        frames, elev, color = BIRD, random.choice([1, 2, 2, 4]), "bird"
    return {"x": x, "elev": elev, "frames": frames, "color": color, "width": len(frames[0][0])}


# ---------- Screens ----------
def title_screen(screen, best):
    screen.nodelay(True)
    tick = 0
    while True:
        key = screen.getch()
        if key in QUIT_KEYS:
            return False
        if key in JUMP_KEYS:
            return True
        if too_small(screen):
            time.sleep(0.1)
            continue

        h, w = screen.getmaxyx()
        ground = h - 4
        screen.erase()
        banner = BANNER if w > len(BANNER[0]) + 2 else ["DINO RUN"]
        y = max(1, ground // 2 - 5)
        for i, row in enumerate(banner):
            center(screen, y + i, row, COLORS["title"])
        y += len(banner) + 1
        center(screen, y, "Jump over cacti. Duck under birds.")
        if (tick // 10) % 2 == 0:
            center(screen, y + 2, ">>  Press SPACE to start  <<", COLORS["score"])
        if best:
            center(screen, y + 3, f"High score: {best:05d}", COLORS["flash"])

        text(screen, ground + 1, 0, "-" * w, COLORS["ground"])
        draw(screen, ground - 2, DINO_X, DINO_RUN[(tick // 3) % 2], COLORS["dino"])
        draw(screen, ground - 2, w - 12, CACTUS_TALL, COLORS["cactus"])
        text(screen, h - 1, 1, "SPACE/UP jump   DOWN duck   P pause   Q quit", curses.A_DIM)
        screen.refresh()
        time.sleep(0.05)
        tick += 1


def pause(screen):
    h = screen.getmaxyx()[0]
    center(screen, h // 3, "  PAUSED - press P to keep going  ", curses.A_REVERSE)
    screen.refresh()
    screen.nodelay(False)
    try:
        while True:
            key = screen.getch()
            if key in PAUSE_KEYS:
                return True
            if key in QUIT_KEYS:
                return False
    finally:
        screen.nodelay(True)


def game_over(screen, score, best, new_record):
    lines = [("G A M E   O V E R", COLORS["danger"]), ("", 0),
             (f"Score {score:05d}     Best {best:05d}", COLORS["score"])]
    if new_record:
        lines.append(("*** NEW HIGH SCORE! ***", COLORS["flash"]))
    lines += [("", 0), ("SPACE = play again    Q = quit", 0)]

    h, w = screen.getmaxyx()
    box_w = max(len(s) for s, _ in lines) + 6
    x = (w - box_w) // 2
    y = max(1, (h - 4) // 2 - len(lines))
    text(screen, y, x, "+" + "-" * (box_w - 2) + "+")
    for i, (s, attr) in enumerate(lines, start=1):
        text(screen, y + i, x, "|" + " " * (box_w - 2) + "|")
        center(screen, y + i, s, attr)
    text(screen, y + len(lines) + 1, x, "+" + "-" * (box_w - 2) + "+")
    screen.refresh()

    time.sleep(0.7)  # so a panicked jump press doesn't instantly restart
    curses.flushinp()
    screen.nodelay(False)
    try:
        while True:
            key = screen.getch()
            if key in QUIT_KEYS:
                return False
            if key in JUMP_KEYS:
                return True
    finally:
        screen.nodelay(True)


# ---------- The game ----------
def run_game(screen, best):
    height, vel = 0.0, 0.0  # dino's height above the ground and upward speed
    duck = 0
    obstacles = []
    clouds = []
    gap = 25
    score, tick, flash = 0, 0, 0
    ground_line, dirt = [], []
    screen.nodelay(True)
    curses.flushinp()

    while True:
        if too_small(screen):
            if screen.getch() in QUIT_KEYS:
                return None
            time.sleep(0.1)
            continue
        h, w = screen.getmaxyx()
        ground = h - 4

        # --- Keys ---
        jump = False
        while True:
            key = screen.getch()
            if key == -1:
                break
            if key in QUIT_KEYS:
                return None
            if key in JUMP_KEYS:
                jump = True
            if key in DUCK_KEYS:
                duck = DUCK_TICKS
            if key in PAUSE_KEYS and not pause(screen):
                return None

        # --- Jumping and ducking ---
        on_ground = height == 0 and vel == 0
        if jump and on_ground:
            vel, duck, on_ground = JUMP_SPEED, 0, False
        if not on_ground:
            height += vel
            vel -= GRAVITY + (FAST_FALL if duck else 0)
            if height <= 0:
                height, vel = 0.0, 0.0
        if duck:
            duck -= 1
        ducking = duck > 0 and height == 0

        # --- Move the world ---
        for o in obstacles:
            o["x"] -= 1
        obstacles = [o for o in obstacles if o["x"] + o["width"] > 0]
        gap -= 1
        if gap <= 0:
            o = new_obstacle(w - 1, score)
            obstacles.append(o)
            gap = o["width"] + random.randint(28, 55)

        if not clouds:
            clouds = [[random.randint(10, w), random.randint(2, max(2, ground - 9))] for _ in range(2)]
        if tick % 3 == 0:
            for c in clouds:
                c[0] -= 1
        clouds = [c for c in clouds if c[0] > -len(CLOUD[0])]
        if len(clouds) < w // 25 and random.random() < 0.02:
            clouds.append([w - 1, random.randint(2, max(2, ground - 9))])

        if len(ground_line) != w - 1:
            ground_line = [random.choice("-" * 15 + "=") for _ in range(w - 1)]
            dirt = [random.choice(" " * 12 + ".,`'-") for _ in range(w - 1)]
        ground_line = ground_line[1:] + [random.choice("-" * 15 + "=")]
        dirt = dirt[1:] + [random.choice(" " * 12 + ".,`'-")]

        # --- Crash check ---
        frame = (tick // 3) % 2
        if height > 0:
            dino = DINO_RUN[0]
        elif ducking:
            dino = DINO_DUCK[frame]
        else:
            dino = DINO_RUN[frame]
        dino_top = ground - int(height) - (len(dino) - 1)
        dino_cells = cells(dino_top, DINO_X, dino)
        dead = False
        for o in obstacles:
            rows = o["frames"][(tick // 4) % len(o["frames"])]
            o["top"], o["rows"] = ground - o["elev"] - (len(rows) - 1), rows
            if dino_cells & cells(o["top"], o["x"], rows):
                dead = True

        # --- Draw ---
        screen.erase()
        for cx, cy in clouds:
            draw(screen, cy, cx, CLOUD, COLORS["cloud"])
        text(screen, ground + 1, 0, "".join(ground_line), COLORS["ground"])
        draw(screen, ground + 2, 0, ["".join(dirt)], COLORS["ground"])
        for o in obstacles:
            draw(screen, o["top"], o["x"], o["rows"], COLORS[o["color"]])
        if dead:
            dino = [row.replace("o", "x") for row in dino]
        draw(screen, dino_top, DINO_X, dino, COLORS["dino"])

        level = score // 100 + 1
        text(screen, 0, 1, f"LEVEL {level}", COLORS["score"])
        if flash == 0 or (flash // 4) % 2 == 0:
            hud = f"HI {max(best, score):05d}   {score:05d}"
            text(screen, 0, w - len(hud) - 2, hud, COLORS["score"])
        if flash:
            center(screen, 2, "SPEED UP!", COLORS["flash"])
            flash -= 1
        text(screen, h - 1, 1, "SPACE/UP jump   DOWN duck   P pause   Q quit", curses.A_DIM)
        screen.refresh()

        if dead:
            curses.beep()
            return score

        score += 1
        tick += 1
        if score % 100 == 0:
            flash = 24
            curses.beep()
        time.sleep(max(0.022, 0.05 - (score // 100) * 0.0025))  # faster every 100 points


def play(screen):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    setup_colors()
    best = load_best()
    if not title_screen(screen, best):
        return
    while True:
        score = run_game(screen, best)
        if score is None:
            return
        new_record = score > best
        if new_record:
            best = score
            save_best(best)
        if not game_over(screen, score, best, new_record):
            return


def main():
    try:
        curses.wrapper(play)
    except KeyboardInterrupt:
        pass
    print("Thanks for playing Dino Run!")


if __name__ == "__main__":
    main()
