"""Software framebuffer.

Everything the game draws goes through this class. A ``Canvas`` is just
a ``bytearray`` of 32 bit pixels (B, G, R, A byte order), which every
backend can blit to a window as a single image. That is the same model
as an MLX image, so the game never needs more than "put one image in
the window".
"""

from __future__ import annotations

import math

from .font import GLYPH_H, GLYPH_W, GLYPHS

Color = int  # 0xRRGGBB


def pixel(color: Color) -> bytes:
    """Return the 4 bytes (B, G, R, A) that encode ``color``."""
    return bytes((color & 0xFF, (color >> 8) & 0xFF,
                  (color >> 16) & 0xFF, 0xFF))


class Canvas:
    """A fixed size 32 bit pixel buffer with a few drawing primitives."""

    def __init__(self, width: int, height: int) -> None:
        """Create a black canvas of ``width`` x ``height`` pixels."""
        self.width = width
        self.height = height
        self.stride = width * 4
        self.buf = bytearray(width * height * 4)
        self.clear(0x000000)

    # -- basic operations -------------------------------------------------

    def clear(self, color: Color) -> None:
        """Fill the whole canvas with ``color``."""
        self.buf[:] = pixel(color) * (self.width * self.height)

    def copy_from(self, other: "Canvas") -> None:
        """Copy every pixel of ``other`` (same size) into this canvas."""
        self.buf[:] = other.buf

    def copy_rect_from(self, other: "Canvas", x: int, y: int,
                       w: int, h: int) -> None:
        """Copy the rectangle ``(x, y, w, h)`` from ``other``."""
        x0, y0 = max(x, 0), max(y, 0)
        x1, y1 = min(x + w, self.width), min(y + h, self.height)
        if x0 >= x1 or y0 >= y1:
            return
        for yy in range(y0, y1):
            start = yy * self.stride + x0 * 4
            end = yy * self.stride + x1 * 4
            self.buf[start:end] = other.buf[start:end]

    def blit_top(self, other: "Canvas") -> None:
        """Copy a full width canvas into the first rows of this one."""
        self.buf[0:len(other.buf)] = other.buf

    # -- primitives ---------------------------------------------------------

    def fill_rect(self, x: int, y: int, w: int, h: int,
                  color: Color) -> None:
        """Fill a rectangle, clipped to the canvas."""
        x0, y0 = max(x, 0), max(y, 0)
        x1, y1 = min(x + w, self.width), min(y + h, self.height)
        if x0 >= x1 or y0 >= y1:
            return
        row = pixel(color) * (x1 - x0)
        size = len(row)
        offset = y0 * self.stride + x0 * 4
        buf = self.buf
        for _ in range(y1 - y0):
            buf[offset:offset + size] = row
            offset += self.stride

    def fill_circle(self, cx: int, cy: int, r: int, color: Color) -> None:
        """Fill a disc centred on ``(cx, cy)``."""
        if r <= 0:
            self.fill_rect(cx, cy, 1, 1, color)
            return
        limit = (r + 0.5) ** 2
        for dy in range(-r, r + 1):
            half = int(math.sqrt(max(limit - dy * dy, 0.0)))
            self.fill_rect(cx - half, cy + dy, 2 * half + 1, 1, color)

    def fill_pacman(self, cx: int, cy: int, r: int, direction: int,
                    mouth_deg: float, color: Color) -> None:
        """Draw a disc with a wedge removed.

        ``direction`` is 0=N, 1=E, 2=S, 3=W and ``mouth_deg`` the half
        opening of the mouth in degrees (0 draws a full disc).
        """
        if mouth_deg <= 0.5:
            self.fill_circle(cx, cy, r, color)
            return
        tan_a = math.tan(math.radians(min(mouth_deg, 80.0)))
        limit = (r + 0.5) ** 2
        for dy in range(-r, r + 1):
            half = int(math.sqrt(max(limit - dy * dy, 0.0)))
            if direction in (1, 3):
                cut = int(abs(dy) / tan_a)
                if cut >= half:
                    left, right = -half, half
                elif direction == 1:
                    left, right = -half, cut
                else:
                    left, right = -cut, half
                self.fill_rect(cx + left, cy + dy, right - left + 1, 1,
                               color)
                continue
            inside = dy < 0 if direction == 0 else dy > 0
            if not inside:
                self.fill_rect(cx - half, cy + dy, 2 * half + 1, 1, color)
                continue
            cut = int(math.ceil(abs(dy) * tan_a))
            if cut > half:
                continue
            self.fill_rect(cx - half, cy + dy, half - cut + 1, 1, color)
            self.fill_rect(cx + cut, cy + dy, half - cut + 1, 1, color)

    # -- text ---------------------------------------------------------------

    @staticmethod
    def text_width(text: str, scale: int = 1) -> int:
        """Width in pixels of ``text`` drawn at ``scale``."""
        if not text:
            return 0
        return len(text) * (GLYPH_W + 1) * scale - scale

    @staticmethod
    def text_height(scale: int = 1) -> int:
        """Height in pixels of one line of text at ``scale``."""
        return GLYPH_H * scale

    def draw_text(self, x: int, y: int, text: str, color: Color,
                  scale: int = 1) -> int:
        """Draw ``text`` (upper-cased) and return its pixel width."""
        cursor = x
        for char in text.upper():
            runs = GLYPHS.get(char, GLYPHS["?"])
            for col, row, length in runs:
                self.fill_rect(cursor + col * scale, y + row * scale,
                               length * scale, scale, color)
            cursor += (GLYPH_W + 1) * scale
        return self.text_width(text, scale)

    def draw_text_centered(self, cx: int, y: int, text: str, color: Color,
                           scale: int = 1) -> None:
        """Draw ``text`` horizontally centred on ``cx``."""
        self.draw_text(cx - self.text_width(text, scale) // 2, y, text,
                       color, scale)
