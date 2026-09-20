#!/usr/bin/env python3
"""Render ZMK keymap layers (charybdis.keymap) as PNG diagrams."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fm.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK KR"

# --- helpers -----------------------------------------------------------
BASE = "#f4f4f2"
OVERRIDE = "#ffe08a"
ACCENT = "#a8d5ff"
COMBO = "#ffb3b3"
COMBO2 = "#ffcc99"
EMPTY = "#e6e6e6"
TEXT = "#1c1c1c"

def key(label, kind="base"):
    color = {"base": BASE, "override": OVERRIDE, "accent": ACCENT,
             "combo": COMBO, "combo2": COMBO2, "empty": EMPTY}[kind]
    return (label, color)

NONE = None

def draw_layer(title, subtitle, rows, thumbs, out_path, legend=None, extra_note=None):
    """
    rows: list of 4 lists, each with 12 (label, color) or None entries
    thumbs: list of dicts {col: (label, color)} for thumb row(s), keyed by
            logical column 0-11; list index = thumb row (0,1)
    """
    ncols = 12
    nrows = 4 + len(thumbs)
    cell = 1.0
    gap_col = 6  # visual gap between col 5 and col 6

    fig_w = ncols * cell + 1.2
    fig_h = nrows * cell + 2.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(-0.5, ncols * cell + 1.0)
    ax.set_ylim(-(nrows * cell + 0.5), 1.3)
    ax.axis("off")
    ax.set_aspect("equal")

    def xpos(c):
        return c * cell + (0.6 if c >= gap_col else 0)

    def draw_key(col, row_from_top, entry, small=False):
        if entry is None:
            return
        label, color = entry
        x = xpos(col)
        y = -(row_from_top * cell)
        pad = 0.06
        box = FancyBboxPatch(
            (x + pad, y - cell + pad), cell - 2 * pad, cell - 2 * pad,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.1, edgecolor="#555555", facecolor=color, zorder=2,
        )
        ax.add_patch(box)
        fontsize = 8.3 if not small else 7.6
        ax.text(x + cell / 2, y - cell / 2, label, ha="center", va="center",
                fontsize=fontsize, color=TEXT, zorder=3, wrap=True,
                linespacing=1.15)

    for r, row in enumerate(rows):
        for c, entry in enumerate(row):
            draw_key(c, r, entry)

    for ti, trow in enumerate(thumbs):
        r = 4 + ti
        for c, entry in trow.items():
            draw_key(c, r, entry)

    ax.text((ncols * cell + 1.0) / 2 - 0.25, 1.15, title, ha="center", va="top",
            fontsize=17, fontweight="bold", color=TEXT)
    if subtitle:
        ax.text((ncols * cell + 1.0) / 2 - 0.25, 0.62, subtitle, ha="center", va="top",
                fontsize=10.5, color="#444444")

    y0 = -(nrows * cell + 0.15)
    if legend:
        lx = -0.4
        for lbl, color in legend:
            ax.add_patch(FancyBboxPatch((lx, y0 - 0.32), 0.32, 0.32,
                                         boxstyle="round,pad=0.01,rounding_size=0.06",
                                         linewidth=1, edgecolor="#555555",
                                         facecolor=color))
            ax.text(lx + 0.42, y0 - 0.16, lbl, ha="left", va="center", fontsize=9.5)
            lx += 0.42 + 0.11 * len(lbl) + 0.55
        y0 -= 0.6

    if extra_note:
        ax.text(-0.4, y0 - 0.05, extra_note, ha="left", va="top", fontsize=9,
                color="#333333", wrap=True)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote", out_path)


# --- Layer 0 : Base -----------------------------------------------------
row0 = [key("Esc"), key("1"), key("2"), key("3"), key("4"), key("5"),
        key("6"), key("7"), key("8"), key("9"), key("0"), key("Backsp")]
row1 = [key("Tab"), key("Q"), key("W"), key("E"), key("R"), key("T"),
        key("Y"), key("U"), key("I"), key("O"), key("P"), key("\\")]
row2 = [key("Shift"), key("A"), key("S"), key("D"), key("F"), key("G"),
        key("H"), key("J"), key("K"), key("L"), key(";"), key("'")]
row3 = [key("Ctrl"), key("Z\n(Ctrl+Z)", "accent"), key("X\n(Ctrl+X)", "accent"),
        key("C\n(Ctrl+C)", "accent"), key("V\n(Ctrl+V)", "accent"), key("B"),
        key("N"), key("M"), key(","), key("."), key("/"), key("TOG L5", "accent")]

thumb0 = [
    {3: key("Alt"), 4: key("Backsp"), 5: key("LT3/\nCapsLock", "accent"),
     6: key("Win"), 7: key("Space")},
    {4: key("Click L", "accent"), 5: key("RClick /\nHold→Scroll(L5)", "accent"),
     6: key("LT5/\nEnter", "accent")},
]

draw_layer(
    "Layer 0 — Base",
    "기본 레이어 (타이핑 + 트랙볼)",
    [row0, row1, row2, row3], thumb0,
    "layer0_base.png",
    legend=[("mod-tap / hold-tap", ACCENT)],
    extra_note=("• J+L 동시누름 콤보: 한/영 전환 (LANG1)\n"
                "• Q+W 동시누름 콤보: 스크린샷 (Win+Shift+S)\n"
                "• 트랙볼 우클릭 홀드 → 레이어 5로 전환되면서 트랙볼이 스크롤로 변환"),
)

# --- Layer 2 : Mac overlay ------------------------------------------------
row0m = [key("Esc"), key("1"), key("2"), key("3"), key("4"), key("5"),
         key("6"), key("7"), key("8"), key("9"), key("0"), key("Backsp")]
row1m = [key("Tab"), key("Q"), key("W"), key("E"), key("R"), key("T"),
         key("Y"), key("U"), key("I"), key("O"), key("P"), key("\\")]
row2m = [key("Shift"), key("A"), key("S"), key("D"), key("F"), key("G"),
         key("H"), key("J"), key("K"), key("L"), key(";"), key("'")]
row3m = [key("Ctrl"), key("Z\n(Cmd+Z)", "override"), key("X\n(Cmd+X)", "override"),
          key("C\n(Cmd+C)", "override"), key("V\n(Cmd+V)", "override"), key("B"),
          key("N"), key("M"), key(","), key("."), key("/"), key("TOG L5", "accent")]
thumb2 = thumb0

draw_layer(
    "Layer 2 — Mac 모드 (overlay)",
    "켜기: Fn + M  (&tog 2, 토글) — 회색 키는 Base와 동일(&trans)",
    [row0m, row1m, row2m, row3m], thumb2,
    "layer2_mac.png",
    legend=[("Mac 전용 변경", OVERRIDE), ("기타 mod-tap", ACCENT)],
    extra_note=("• J+L 콤보 → Ctrl+Space (이전 입력 소스)\n"
                "• Q+W 콤보 → Cmd+Shift+4 (영역 스크린샷)\n"
                "이 레이어에서 바뀌지 않는 키는 모두 회색으로 표시(기본 레이어와 동일)."),
)

# --- Layer 3 : Numpad / BT ------------------------------------------------
row0n = [key("Esc"), key("1"), key("2"), key("3"), key("4"), key("5"),
         key("6"), key("7", "override"), key("8", "override"),
         key("9", "override"), key("+", "override"), key("Backsp")]
row1n = [key("Tab"), key("Q"), key("BT clr", "override"), key("BT 0", "override"),
         key("BT 1", "override"), key("BT 2", "override"),
         key("Y"), key("4", "override"), key("5", "override"),
         key("6", "override"), key("−", "override"), key("\\")]
row2n = [key("Shift"), key("A"), key("S"), key("D"), key("F"), key("G"),
         key("H"), key("1", "override"), key("2", "override"),
         key("3", "override"), key("=", "override"), key("'")]
row3n = [key("Ctrl"), key("Z", "accent"), key("X", "accent"), key("C", "accent"),
         key("V", "accent"), key("B"),
         key("N"), key("M"), key("0", "override"), key(".", "override"),
         key("/"), key("TOG L5", "accent")]
thumb3 = thumb0

draw_layer(
    "Layer 3 — 넙패드 / 블루투스",
    "켜기: 왼쪽 가운데 엄지 홀드  (&lt 3 CAPSLOCK)",
    [row0n, row1n, row2n, row3n], thumb3,
    "layer3_numpad_bt.png",
    legend=[("이 레이어에서 변경된 키", OVERRIDE)],
    extra_note="• 오른손 전체가 넙패드로 바뀌고(7 8 9 + / 4 5 6 − / 1 2 3 = / 0 . /), 왼손 상단에 블루투스 선택/해제 키가 놀인다.",
)

# --- Layer 5 : Fn + trackball scroll --------------------------------------
row0f = [key("F1"), key("F2"), key("F3"), key("F4"), key("F5"), key("F6"),
         key("F7"), key("F8"), key("F9"), key("F10"), key("F11"), key("F12")]
row1f = [key("Caps", "override"), key("Q"), key("W"), key("E"), key("R"), key("T"),
         key("Y"), key("U"), key("↑", "override"), key("O"), key("P"), key("\\")]
row2f = [key("Shift"), key("A"), key("S"), key("D"), key("F"), key("G"),
         key("H"), key("←", "override"), key("↓", "override"),
         key("→", "override"), key(";"), key("'")]
row3f = [key("Ctrl"), key("Z", "accent"), key("X", "accent"), key("C", "accent"),
         key("V", "accent"), key("B"),
         key("N"), key("TOG L2\n(Mac)", "override"), key(","), key("."), key("/"),
         key("TOG L5", "accent")]
thumb5 = [
    {3: key("Alt"), 4: key("Space", "override"), 5: key("LT3/\nCapsLock", "accent"),
     6: key("Win"), 7: key("Space")},
    {4: key("Click L", "accent"), 5: key("Click R", "override"),
     6: key("Enter", "override")},
]

draw_layer(
    "Layer 5 — Fn / 트랙볼 스크롤",
    "켜기: ① 아포스트로피 아래 키 토글(&tog 5) ② 엄지 Enter 홀드(&lt 5 RETURN) ③ 트랙볼 우클릭 홀드",
    [row0f, row1f, row2f, row3f], thumb5,
    "layer5_fn_scroll.png",
    legend=[("이 레이어에서 변경된 키", OVERRIDE), ("mod-tap", ACCENT)],
    extra_note="• 트랙볼이 이 레이어에서 스크롤로 동작(드라이버가 최상위 활성 레이어를 비교하므로 이 레이어 번호를 Mac 모드(2)보다 높게 유지).\n• F1~F12는 숫자 열 전체에 배치되어 있다.",
)

# --- Combos overview (drawn on base layer) --------------------------------
rowc0 = [key("Esc"), key("1"), key("2"), key("3"), key("4"), key("5"),
         key("6"), key("7"), key("8"), key("9"), key("0"), key("Backsp")]
rowc1 = [key("Tab"), key("Q", "combo2"), key("W", "combo2"), key("E"), key("R"), key("T"),
         key("Y"), key("U"), key("I"), key("O"), key("P"), key("\\")]
rowc2 = [key("Shift"), key("A"), key("S"), key("D"), key("F"), key("G"),
         key("H"), key("J", "combo"), key("K"), key("L", "combo"), key(";"), key("'")]
rowc3 = [key("Ctrl"), key("Z"), key("X"), key("C"), key("V"), key("B"),
         key("N"), key("M"), key(","), key("."), key("/"), key("TOG L5")]

draw_layer(
    "Combos",
    "타이밍: timeout 50ms, require-prior-idle 150ms",
    [rowc0, rowc1, rowc2, rowc3], [{}],
    "combos.png",
    legend=[("J + L", COMBO), ("Q + W", COMBO2)],
    extra_note=("• J + L (pos 31,33) → Win: 한/영 전환(LANG1)  /  Mac 모드: Ctrl+Space\n"
                "• Q + W (pos 13,14) → Win: Win+Shift+S 스크린샷  /  Mac 모드: Cmd+Shift+4"),
)

print("done")
