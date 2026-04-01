import reflex as rx
from ..state import State
from ..navbar import navbar

# ── Design tokens ──────────────────────────────────────
BG_BASE      = "#0a0a0f"
BG_SURFACE   = "#111118"
BG_ELEVATED  = "#18181f"
BG_BORDER    = "#2a2a35"
BG_BORDER_LT = "#3a3a48"
ACCENT       = "#3b82f6"
GREEN        = "#22c55e"
GREEN_BG     = "rgba(34,197,94,0.08)"
GREEN_BORDER = "rgba(34,197,94,0.28)"
AMBER        = "#f59e0b"
AMBER_BG     = "rgba(245,158,11,0.08)"
AMBER_BORDER = "rgba(245,158,11,0.28)"
RED_BG       = "rgba(239,68,68,0.08)"
RED_BORDER   = "rgba(239,68,68,0.28)"
TEXT_PRIMARY   = "#f1f1f5"
TEXT_SECONDARY = "#8b8b9e"
TEXT_MUTED     = "#52525f"
FONT_DISPLAY   = "'Syne', sans-serif"
FONT_MONO      = "'JetBrains Mono', 'Fira Code', monospace"

# ── Editor script ───────────────────────────────────────
# Uses rx.el.textarea (raw HTML, no Reflex DebounceInput wrapper)
# so keydown fires before React touches the event.
EDITOR_SCRIPT = """
<style>
#py-editor {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 12px;
  line-height: 1.85;
  width: 100%;
  height: 480px;
  background: #1a0f0f;
  color: #f8f8f2;
  border: none;
  padding: 14px;
  resize: none;
  outline: none;
  caret-color: #3b82f6;
  white-space: pre;
  overflow-wrap: normal;
  overflow-x: auto;
  overflow-y: auto;
  box-sizing: border-box;
}
#py-editor::placeholder { color: #44475a; }
#py-editor:focus { outline: none !important; box-shadow: none !important; }
</style>
<script>
(function () {
  var INDENT = '    '; // 4 spaces

  function setVal(el, v) {
    /* Use React's internal setter so Reflex state stays in sync */
    var setter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype, 'value'
    ).set;
    setter.call(el, v);
    el.dispatchEvent(new Event('input', { bubbles: true }));
  }

  function attachEditor() {
    var ta = document.getElementById('py-editor');
    if (!ta) { setTimeout(attachEditor, 200); return; }
    if (ta._editorReady) return;
    ta._editorReady = true;

    ta.addEventListener('keydown', function (e) {
      var s   = this.selectionStart;
      var end = this.selectionEnd;
      var v   = this.value;

      /* ── TAB  ────────────────────────────────────── */
      if (e.key === 'Tab') {
        e.preventDefault();
        e.stopPropagation();

        if (s !== end) {
          /* Multi-line: indent / unindent selected lines */
          var ls = v.lastIndexOf('\n', s - 1) + 1;
          var le = v.indexOf('\n', end - 1);
          if (le < 0) le = v.length;
          var block = v.substring(ls, le);
          var rep;
          if (e.shiftKey) {
            rep = block.split('\n').map(function (l) {
              return l.startsWith(INDENT) ? l.slice(4)
                   : l.startsWith('\t')   ? l.slice(1)
                   : l;
            }).join('\n');
          } else {
            rep = block.split('\n').map(function (l) {
              return INDENT + l;
            }).join('\n');
          }
          setVal(this, v.substring(0, ls) + rep + v.substring(le));
          this.selectionStart = ls;
          this.selectionEnd   = ls + rep.length;
        } else {
          /* Single cursor — insert 4 spaces */
          setVal(this, v.substring(0, s) + INDENT + v.substring(end));
          this.selectionStart = this.selectionEnd = s + 4;
        }
        return;
      }

      /* ── ENTER — auto-indent  ────────────────────── */
      if (e.key === 'Enter') {
        e.preventDefault();
        e.stopPropagation();
        var lineStart  = v.lastIndexOf('\n', s - 1) + 1;
        var currentLine = v.substring(lineStart, s);
        var indent     = currentLine.match(/^(\s*)/)[1];
        var lastChar   = currentLine.trimEnd().slice(-1);
        var extra      = [':', '(', '[', '{'].indexOf(lastChar) >= 0 ? INDENT : '';
        var ins        = '\n' + indent + extra;
        setVal(this, v.substring(0, s) + ins + v.substring(end));
        this.selectionStart = this.selectionEnd = s + ins.length;
        return;
      }

      /* ── AUTO-CLOSE brackets & quotes  ──────────── */
      var PAIRS = { '(': ')', '[': ']', '{': '}', '"': '"', "'": "'" };
      if (PAIRS[e.key] && s === end) {
        e.preventDefault();
        var close = PAIRS[e.key];
        setVal(this, v.substring(0, s) + e.key + close + v.substring(end));
        this.selectionStart = this.selectionEnd = s + 1;
        return;
      }

      /* ── SKIP over existing closer  ─────────────── */
      var CLOSERS = [')', ']', '}', '"', "'"];
      if (CLOSERS.indexOf(e.key) >= 0 && v[s] === e.key && s === end) {
        e.preventDefault();
        this.selectionStart = this.selectionEnd = s + 1;
        return;
      }

      /* ── BACKSPACE removes paired closer  ────────── */
      if (e.key === 'Backspace' && s === end && s > 0) {
        var OP = { '(': ')', '[': ']', '{': '}', '"': '"', "'": "'" };
        if (OP[v[s - 1]] && OP[v[s - 1]] === v[s]) {
          e.preventDefault();
          setVal(this, v.substring(0, s - 1) + v.substring(s + 1));
          this.selectionStart = this.selectionEnd = s - 1;
        }
      }
    }, true); /* useCapture=true — fires BEFORE React */
  }

  /* Try immediately, then retry after Reflex hydration */
  attachEditor();
  window.addEventListener('load', attachEditor);
  setTimeout(attachEditor, 800);
  setTimeout(attachEditor, 2000);
})();
</script>
"""


def _label(icon, text):
    return rx.hstack(
        rx.text(icon, font_size="12px", line_height="1"),
        rx.text(text, font_family=FONT_MONO, font_size="10px", font_weight="600",
                color=TEXT_MUTED, text_transform="uppercase", letter_spacing="0.10em"),
        spacing="2", align="center",
    )


def _result_panel(icon, label, value, bg, border, text_color):
    return rx.box(
        rx.vstack(
            _label(icon, label),
            rx.box(
                rx.text(value, font_family=FONT_MONO, font_size="13px", color=text_color,
                        line_height="1.7", white_space="pre-wrap", width="100%"),
                padding="12px 14px", background=bg, border_radius="8px",
                width="100%", min_height="60px",
            ),
            spacing="3", align="start", width="100%",
        ),
        padding="16px", background=BG_ELEVATED, border=f"1px solid {border}",
        border_radius="10px", width="100%",
    )


def _line_numbers(count=60):
    return rx.box(
        rx.vstack(
            *[rx.text(str(i), font_family=FONT_MONO, font_size="11px", color=TEXT_MUTED,
                      line_height="1.85", text_align="right") for i in range(1, count + 1)],
            spacing="0", align="end",
        ),
        padding="14px 10px 14px 12px", background="#12121a",
        border_right=f"1px solid {BG_BORDER}", min_width="40px",
        user_select="none", overflow="hidden", flex_shrink="0",
    )


def _col_header(dot_color, title, tag, tag_color, tag_bg, tag_border):
    return rx.hstack(
        rx.hstack(
            rx.box(width="8px", height="8px", border_radius="50%",
                   background=dot_color, box_shadow=f"0 0 6px {dot_color}"),
            rx.text(title, font_family=FONT_DISPLAY, font_size="12px",
                    font_weight="700", color=TEXT_PRIMARY, letter_spacing="-0.01em"),
            spacing="2", align="center",
        ),
        rx.spacer(),
        rx.box(
            rx.text(tag, font_family=FONT_MONO, font_size="10px",
                    color=tag_color, font_weight="600"),
            padding="3px 10px", background=tag_bg,
            border=f"1px solid {tag_border}", border_radius="4px",
        ),
        align="center", width="100%", padding="11px 16px",
        background="#12121a", border_bottom=f"1px solid {BG_BORDER}",
    )


def _original_col():
    return rx.box(
        _col_header("#ef4444", "Original Code", "python editor",
                    "#ef4444", RED_BG, RED_BORDER),
        rx.hstack(
            _line_numbers(60),
            # rx.el.textarea = raw <textarea> HTML element.
            # NO Reflex DebounceInput wrapper → keydown fires first.
            rx.el.textarea(
                State.user_code,
                id="py-editor",
                on_change=State.set_user_code,
                placeholder="# Paste or type Python code here\n# Tab = 4 spaces  |  Enter = auto-indent  |  () [] {} auto-close",
            ),
            spacing="0", align="start", width="100%",
        ),
        border="1px solid rgba(239,68,68,0.28)", border_radius="14px",
        overflow="hidden", flex="1", min_width="0",
    )


def _improved_col():
    return rx.box(
        _col_header(GREEN, "Improved Code", "AI rewritten",
                    GREEN, GREEN_BG, GREEN_BORDER),
        rx.hstack(
            _line_numbers(60),
            rx.text_area(
                value=State.improved_code, is_read_only=True,
                height="480px", width="100%",
                font_family=FONT_MONO, font_size="12px", line_height="1.85",
                resize="none", background="#0d1a0f", color="#f8f8f2",
                border="none", padding="14px", outline="none",
                _focus={"outline": "none", "box_shadow": "none"},
            ),
            spacing="0", align="start", width="100%",
        ),
        border="1px solid rgba(34,197,94,0.28)", border_radius="14px",
        overflow="hidden", flex="1", min_width="0",
    )


def _diff_divider():
    return rx.vstack(
        rx.box(width="1px", background=BG_BORDER, flex="1"),
        rx.center(
            rx.text("→", font_family=FONT_MONO, font_size="13px",
                    color=ACCENT, font_weight="700"),
            width="30px", height="30px", background=BG_ELEVATED,
            border=f"1px solid {BG_BORDER_LT}", border_radius="50%", flex_shrink="0",
        ),
        rx.box(width="1px", background=BG_BORDER, flex="1"),
        align="center", height="100%", min_height="480px",
        spacing="0", flex_shrink="0", padding_x="6px",
    )


def analyzer():
    return rx.box(
        navbar(),
        rx.html(EDITOR_SCRIPT),

        rx.center(
            rx.vstack(

                # Page header
                rx.hstack(
                    rx.vstack(
                        rx.text("Code Analyzer", font_family=FONT_DISPLAY,
                                font_size="26px", font_weight="700", color=TEXT_PRIMARY,
                                letter_spacing="-0.02em", line_height="1"),
                        rx.text(
                            "Paste Python → Analyze → compare original vs improved side by side",
                            font_family=FONT_DISPLAY, font_size="13px", color=TEXT_MUTED),
                        spacing="1", align="start",
                    ),
                    rx.spacer(),
                    rx.box(
                        rx.text("● READY", font_family=FONT_MONO, font_size="10px",
                                font_weight="700", color=GREEN, letter_spacing="0.06em"),
                        padding="5px 12px", background=GREEN_BG,
                        border=f"1px solid {GREEN_BORDER}", border_radius="6px",
                    ),
                    align="center", width="100%",
                ),

                rx.box(height="1px", width="100%", background=BG_BORDER),

                # Side-by-side diff
                rx.hstack(
                    _original_col(), _diff_divider(), _improved_col(),
                    spacing="0", align="stretch", width="100%",
                ),

                # Action bar
                rx.hstack(
                    rx.button(
                        rx.text("▶  Analyze Code", font_family=FONT_MONO,
                                font_size="13px", font_weight="600", color="white"),
                        on_click=State.analyze_code,
                        background=ACCENT, border="none", border_radius="9px",
                        height="40px", padding_x="22px", cursor="pointer",
                        transition="all 0.18s",
                        _hover={"background": "#2563eb", "transform": "translateY(-1px)"},
                    ),
                    rx.button(
                        rx.text("↺  Reset", font_family=FONT_MONO,
                                font_size="12px", font_weight="500", color=TEXT_SECONDARY),
                        on_click=State.reset_editor,
                        background="transparent", border=f"1px solid {BG_BORDER_LT}",
                        border_radius="9px", height="40px", padding_x="18px",
                        cursor="pointer", transition="all 0.18s",
                        _hover={"border_color": "#ef4444", "color": "#ef4444"},
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.box(rx.text("Tab", font_family=FONT_MONO, font_size="9px",
                                       color=TEXT_MUTED),
                               padding="2px 7px", border=f"1px solid {BG_BORDER_LT}",
                               border_radius="4px", background=BG_ELEVATED),
                        rx.text("indent", font_family=FONT_MONO,
                                font_size="10px", color=TEXT_MUTED),
                        rx.box(rx.text("Enter", font_family=FONT_MONO, font_size="9px",
                                       color=TEXT_MUTED),
                               padding="2px 7px", border=f"1px solid {BG_BORDER_LT}",
                               border_radius="4px", background=BG_ELEVATED),
                        rx.text("auto-indent  ·  Powered by Claude AI",
                                font_family=FONT_MONO, font_size="10px", color=TEXT_MUTED),
                        spacing="2", align="center",
                    ),
                    spacing="3", align="center", width="100%",
                ),

                rx.box(height="1px", width="100%", background=BG_BORDER),

                # Syntax + Issues
                rx.grid(
                    _result_panel("✓", "Syntax Check", State.syntax_output,
                                  GREEN_BG, GREEN_BORDER, GREEN),
                    _result_panel("⚠", "Detected Issues", State.errors_output,
                                  AMBER_BG, AMBER_BORDER, AMBER),
                    columns="2", spacing="4", width="100%",
                ),

                # AI Suggestions
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            _label("◈", "AI Suggestions"),
                            rx.spacer(),
                            rx.box(
                                rx.text("claude AI", font_family=FONT_MONO,
                                        font_size="10px", color=ACCENT),
                                padding="2px 10px",
                                background="rgba(59,130,246,0.08)",
                                border="1px solid rgba(59,130,246,0.25)",
                                border_radius="4px",
                            ),
                            align="center", width="100%",
                        ),
                        rx.text_area(
                            value=State.ai_output, is_read_only=True,
                            height="180px", width="100%",
                            font_family=FONT_MONO, font_size="13px", line_height="1.75",
                            color="#bfdbfe", background="rgba(30,58,95,0.35)",
                            border="none", border_radius="8px", padding="14px",
                            resize="none", outline="none",
                            _focus={"outline": "none"},
                        ),
                        spacing="3", align="start", width="100%",
                    ),
                    padding="16px", background=BG_ELEVATED,
                    border="1px solid rgba(59,130,246,0.22)",
                    border_radius="10px", width="100%",
                ),

                spacing="5", align="start", width="100%",
            ),
            padding_x="32px", padding_y="44px", width="100%", max_width="1280px",
        ),

        background=BG_BASE, width="100%", min_height="100vh",
    )