import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# Налаштування вікна та системи координат
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.4)  # Місце для повзунків
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.grid(True, linestyle='--', alpha=0.7)
ax.axhline(0, color='black', lw=1.5)
ax.axvline(0, color='black', lw=1.5)
ax.set_aspect('equal')
ax.set_title("Інтерактивне додавання та скалювання векторів", pad=20)

arrows = []


def draw_vector(start, end, color, label, alpha=1.0, ls='-'):
    # Малюємо стрілку
    arrow = ax.annotate('', xy=end, xytext=start,
                        arrowprops=dict(facecolor=color, edgecolor=color,
                                        width=2, headwidth=8, alpha=alpha, ls=ls),
                        annotation_clip=False)
    # Додаємо підпис
    txt = ax.text(end[0] + 0.3, end[1] + 0.3, label, color=color, fontsize=11, fontweight='bold', alpha=alpha)
    return arrow, txt


def update(val):
    global arrows
    # Очищуємо попередні стрілки
    for arrow, txt in arrows:
        arrow.remove()
        txt.remove()
    arrows.clear()

    vx, vy = s_vx.val, s_vy.val
    wx, wy = s_wx.val, s_wy.val
    c = s_c.val

    # 1. Синій вектор (v)
    arrows.append(draw_vector([0, 0], [vx, vy], 'blue', 'v'))

    # 2. Червоний вектор (w)
    arrows.append(draw_vector([0, 0], [wx, wy], 'red', 'w'))

    # 3. Переносимо червоний вектор (w) на кінчик синього (пунктиром)
    arrows.append(draw_vector([vx, vy], [vx + wx, vy + wy], 'red', 'w (перенес.)', alpha=0.4, ls='--'))

    # 4. Результуюча сума v+w (зелений вектор)
    arrows.append(draw_vector([0, 0], [vx + wx, vy + wy], 'green', 'v+w'))

    # 5. Скалювання c * v (фіолетовий, ледь зміщений, щоб не перекривав синій повністю)
    arrows.append(draw_vector([0, 0.1], [c * vx, c * vy + 0.1], 'purple', f'{c:.1f}*v', alpha=0.8))

    fig.canvas.draw_idle()


# Створюємо повзунки
axcolor = 'lightgoldenrodyellow'
ax_vx = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_vy = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_wx = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_wy = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)
ax_c = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)

s_vx = Slider(ax_vx, 'v (x)', -10.0, 10.0, valinit=3.0)
s_vy = Slider(ax_vy, 'v (y)', -10.0, 10.0, valinit=2.0)
s_wx = Slider(ax_wx, 'w (x)', -10.0, 10.0, valinit=-1.0)
s_wy = Slider(ax_wy, 'w (y)', -10.0, 10.0, valinit=4.0)
s_c = Slider(ax_c, 'Скаляр c (множення)', -3.0, 3.0, valinit=-1.5)

# Оновлюємо графік при зміні повзунків
s_vx.on_changed(update)
s_vy.on_changed(update)
s_wx.on_changed(update)
s_wy.on_changed(update)
s_c.on_changed(update)

update(None)
plt.show()