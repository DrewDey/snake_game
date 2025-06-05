# Terminal-based Snake Game using curses
# The game runs in the terminal and supports arrow key controls.
# Player tries to eat food (@) without hitting walls or itself.
# Score is displayed along with high score persisted in a file.

import curses
import random
import os

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except Exception:
        return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]

    # Draw game border
    for x in range(box[0][1], box[1][1]):
        stdscr.addstr(box[0][0], x, '#')
        stdscr.addstr(box[1][0], x, '#')
    for y in range(box[0][0], box[1][0]):
        stdscr.addstr(y, box[0][1], '#')
        stdscr.addstr(y, box[1][1], '#')

    snake = [
        [sh // 2, sw // 2 + 1],
        [sh // 2, sw // 2],
        [sh // 2, sw // 2 - 1],
    ]
    direction = curses.KEY_RIGHT

    food = [random.randint(box[0][0] + 1, box[1][0] - 1),
            random.randint(box[0][1] + 1, box[1][1] - 1)]
    stdscr.addstr(food[0], food[1], '@')

    score = 0
    high_score = load_high_score()

    while True:
        stdscr.addstr(1, 2, f"Score: {score}  High Score: {high_score}")
        key = stdscr.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]:
            direction = key
        elif key == ord('q'):
            break

        head = snake[0].copy()
        if direction == curses.KEY_RIGHT:
            head[1] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1

        snake.insert(0, head)

        if head == food:
            score += 1
            while True:
                food = [
                    random.randint(box[0][0] + 1, box[1][0] - 1),
                    random.randint(box[0][1] + 1, box[1][1] - 1),
                ]
                if food not in snake:
                    break
            stdscr.addstr(food[0], food[1], '@')
        else:
            tail = snake.pop()
            stdscr.addstr(tail[0], tail[1], ' ')

        stdscr.addstr(head[0], head[1], 'O')

        if (head[0] in [box[0][0], box[1][0]] or
                head[1] in [box[0][1], box[1][1]] or
                head in snake[1:]):
            msg = "Game Over! Press 'r' to restart or 'q' to quit."
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.nodelay(False)
            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    save_high_score(max(score, high_score))
                    return
                if key == ord('r'):
                    save_high_score(max(score, high_score))
                    stdscr.clear()
                    main(stdscr)
                    return

        stdscr.refresh()

        if score > high_score:
            high_score = score


if __name__ == "__main__":
    curses.wrapper(main)
