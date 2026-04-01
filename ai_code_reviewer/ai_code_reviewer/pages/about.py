import reflex as rx
from ..navbar import navbar

# ── Design tokens ──────────────────────────────────────
BG_BASE      = "#0a0a0f"
BG_SURFACE   = "#111118"
BG_ELEVATED  = "#18181f"
BG_BORDER    = "#2a2a35"
BG_BORDER_LT = "#3a3a48"
ACCENT       = "#3b82f6"
TEXT_PRIMARY   = "#f1f1f5"
TEXT_SECONDARY = "#8b8b9e"
TEXT_MUTED     = "#52525f"
FONT_DISPLAY   = "'Syne', sans-serif"
FONT_MONO      = "'JetBrains Mono', 'Fira Code', monospace"


def _divider() -> rx.Component:
    return rx.box(height="1px", width="100%", background=BG_BORDER)


def _feature_row(icon: str, title: str, desc: str) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.text(icon, font_size="16px", line_height="1"),
            width="40px",
            height="40px",
            min_width="40px",
            background=BG_SURFACE,
            border=f"1px solid {BG_BORDER}",
            border_radius="10px",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(title, font_family=FONT_DISPLAY, font_size="14px",
                    font_weight="600", color=TEXT_PRIMARY, line_height="1"),
            rx.text(desc, font_family=FONT_DISPLAY, font_size="13px",
                    color=TEXT_SECONDARY, line_height="1.6"),
            spacing="1",
            align="start",
            width="100%",
        ),
        spacing="4",
        align="start",
        width="100%",
    )


def _step(n: int, text: str) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.text(
                str(n),
                font_family=FONT_MONO,
                font_size="11px",
                font_weight="700",
                color=ACCENT,
            ),
            width="28px",
            height="28px",
            min_width="28px",
            background="rgba(59,130,246,0.10)",
            border="1px solid rgba(59,130,246,0.30)",
            border_radius="50%",
            flex_shrink="0",
        ),
        rx.text(text, font_family=FONT_DISPLAY, font_size="13px",
                color=TEXT_SECONDARY, line_height="1.65"),
        spacing="4",
        align="center",
        width="100%",
    )


def about() -> rx.Component:
    return rx.box(
        navbar(),

        rx.center(
            rx.vstack(

                # ── Header ──────────────────────────────
                rx.vstack(
                    rx.box(
                        rx.text(
                            "ABOUT",
                            font_family=FONT_MONO,
                            font_size="10px",
                            font_weight="700",
                            color=ACCENT,
                            letter_spacing="0.12em",
                        ),
                        padding="4px 12px",
                        background="rgba(59,130,246,0.08)",
                        border="1px solid rgba(59,130,246,0.25)",
                        border_radius="4px",
                        display="inline-block",
                    ),
                    rx.text(
                        "AI Code Reviewer",
                        font_family=FONT_DISPLAY,
                        font_size="30px",
                        font_weight="800",
                        color=TEXT_PRIMARY,
                        letter_spacing="-0.025em",
                        line_height="1.1",
                    ),
                    rx.text(
                        "An intelligent static analysis tool combining AST-based parsing "
                        "with Claude AI — built to help Python developers catch bugs "
                        "faster and write cleaner code.",
                        font_family=FONT_DISPLAY,
                        font_size="14px",
                        color=TEXT_SECONDARY,
                        line_height="1.75",
                        max_width="500px",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),

                _divider(),

                # ── What it checks ───────────────────────
                rx.vstack(
                    rx.text(
                        "// what_it_checks",
                        font_family=FONT_MONO,
                        font_size="12px",
                        font_weight="600",
                        color=TEXT_MUTED,
                    ),
                    rx.vstack(
                        _feature_row("🔍", "Syntax Error Detection",
                            "Python's AST module parses code and reports exact line and column numbers."),
                        _feature_row("🔄", "Infinite Loop Detection",
                            "Identifies while loops without a reachable break that may hang execution."),
                        _feature_row("🧹", "Unused Variables & Imports",
                            "Flags names declared or imported but never referenced in scope."),
                        _feature_row("🤖", "AI-Powered Suggestions",
                            "Claude reads your code and the found issues, then writes targeted advice."),
                        _feature_row("🔀", "Side-by-Side Code Diff",
                            "Original and AI-improved code shown in two aligned columns after analysis."),
                        spacing="5",
                        align="start",
                        width="100%",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                ),

                _divider(),

                # ── How it works ─────────────────────────
                rx.vstack(
                    rx.text(
                        "// how_it_works",
                        font_family=FONT_MONO,
                        font_size="12px",
                        font_weight="600",
                        color=TEXT_MUTED,
                    ),
                    rx.vstack(
                        _step(1, "Paste your Python code into the editor on the Analyzer page."),
                        _step(2, "The AST parser validates syntax and builds a parse tree."),
                        _step(3, "The error detector walks the tree looking for common issues."),
                        _step(4, "Claude receives your code and detected issues, then generates specific suggestions."),
                        _step(5, "Results appear in the panels and the improved code shows in the right column."),
                        spacing="4",
                        align="start",
                        width="100%",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                ),

                _divider(),

                # ── Tech stack ───────────────────────────
                rx.vstack(
                    rx.text(
                        "// tech_stack",
                        font_family=FONT_MONO,
                        font_size="12px",
                        font_weight="600",
                        color=TEXT_MUTED,
                    ),
                    rx.hstack(
                        *[
                            rx.box(
                                rx.text(
                                    tech,
                                    font_family=FONT_MONO,
                                    font_size="12px",
                                    color=TEXT_SECONDARY,
                                    font_weight="500",
                                ),
                                padding="6px 14px",
                                background=BG_ELEVATED,
                                border=f"1px solid {BG_BORDER}",
                                border_radius="6px",
                                transition="all 0.18s",
                                _hover={"border_color": BG_BORDER_LT, "color": TEXT_PRIMARY},
                            )
                            for tech in ["Reflex", "Python AST", "Claude AI", "Syne", "JetBrains Mono"]
                        ],
                        flex_wrap="wrap",
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                ),

                _divider(),

                # ── CTA strip ────────────────────────────
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Ready to review your code?",
                            font_family=FONT_DISPLAY,
                            font_size="16px",
                            font_weight="700",
                            color=TEXT_PRIMARY,
                            letter_spacing="-0.01em",
                        ),
                        rx.text(
                            "No account required. Results in under 2 seconds.",
                            font_family=FONT_DISPLAY,
                            font_size="13px",
                            color=TEXT_MUTED,
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.box(
                            rx.text(
                                "→ Open Analyzer",
                                font_family=FONT_MONO,
                                font_size="12px",
                                font_weight="600",
                                color="white",
                            ),
                            padding="10px 20px",
                            background=ACCENT,
                            border_radius="9px",
                            transition="all 0.18s",
                            _hover={"background": "#2563eb"},
                        ),
                        href="/analyzer",
                        text_decoration="none",
                    ),
                    align="center",
                    width="100%",
                    padding="22px 24px",
                    background=BG_SURFACE,
                    border=f"1px solid {BG_BORDER}",
                    border_radius="14px",
                ),

                spacing="6",
                align="start",
                width="100%",
            ),
            padding_x="32px",
            padding_y="52px",
            width="100%",
            max_width="720px",
        ),

        background=BG_BASE,
        width="100%",
        min_height="100vh",
    )