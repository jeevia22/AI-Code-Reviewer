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


def _badge(text: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                width="6px", height="6px",
                border_radius="50%",
                background=ACCENT,
                box_shadow="0 0 6px #3b82f6",
            ),
            rx.text(
                text,
                font_family=FONT_MONO,
                font_size="11px",
                font_weight="600",
                color=ACCENT,
                letter_spacing="0.06em",
                text_transform="uppercase",
            ),
            spacing="2",
            align="center",
        ),
        padding="5px 14px",
        border="1px solid rgba(59,130,246,0.35)",
        border_radius="999px",
        background="rgba(59,130,246,0.07)",
        display="inline-flex",
    )


def _feature_card(icon: str, title: str, desc: str, tag: str, glow: str) -> rx.Component:
    return rx.box(
        # Coloured top accent line
        rx.box(
            height="2px",
            width="100%",
            background=f"linear-gradient(90deg, {glow}, transparent)",
        ),
        rx.vstack(
            rx.hstack(
                rx.text(icon, font_size="20px", line_height="1"),
                rx.box(
                    rx.text(tag, font_family=FONT_MONO, font_size="10px", color=TEXT_MUTED),
                    padding="2px 8px",
                    border="1px solid #3a3a48",
                    border_radius="4px",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.text(
                title,
                font_family=FONT_DISPLAY,
                font_size="14px",
                font_weight="700",
                color=TEXT_PRIMARY,
                letter_spacing="-0.01em",
            ),
            rx.text(
                desc,
                font_family=FONT_DISPLAY,
                font_size="13px",
                color=TEXT_SECONDARY,
                line_height="1.6",
            ),
            spacing="3",
            align="start",
            width="100%",
            padding="16px",
        ),
        background=BG_ELEVATED,
        border="1px solid #2a2a35",
        border_radius="14px",
        overflow="hidden",
        width="100%",
        transition="all 0.22s ease",
        _hover={
            "border_color": "#3a3a48",
            "background": "#1f1f28",
            "transform": "translateY(-3px)",
            "box_shadow": "0 12px 32px rgba(0,0,0,0.5)",
        },
    )


def _stat(number: str, label: str) -> rx.Component:
    return rx.vstack(
        rx.text(
            number,
            font_family=FONT_MONO,
            font_size="24px",
            font_weight="700",
            color=TEXT_PRIMARY,
            letter_spacing="-0.03em",
        ),
        rx.text(
            label,
            font_family=FONT_DISPLAY,
            font_size="11px",
            color=TEXT_MUTED,
            text_transform="uppercase",
            letter_spacing="0.06em",
        ),
        spacing="1",
        align="center",
    )


def _code_preview() -> rx.Component:
    def line(color: str, content: str) -> rx.Component:
        return rx.text(
            content,
            font_family=FONT_MONO,
            font_size="12px",
            color=color,
            line_height="1.85",
            white_space="pre",
        )

    return rx.box(
        # Window chrome
        rx.hstack(
            rx.hstack(
                rx.box(width="11px", height="11px", border_radius="50%", background="#ff5f57"),
                rx.box(width="11px", height="11px", border_radius="50%", background="#febc2e"),
                rx.box(width="11px", height="11px", border_radius="50%", background="#28c840"),
                spacing="2",
            ),
            rx.text("code_review.py", font_family=FONT_MONO, font_size="12px", color="#6272a4"),
            rx.spacer(),
            rx.box(
                rx.text("LIVE", font_family=FONT_MONO, font_size="9px",
                        color="#50fa7b", font_weight="700"),
                padding="2px 7px",
                border="1px solid rgba(80,250,123,0.3)",
                border_radius="4px",
                background="rgba(80,250,123,0.08)",
            ),
            align="center",
            width="100%",
            padding="12px 16px",
            background="#1a1b26",
            border_bottom="1px solid #2a2a35",
        ),
        # Code
        rx.box(
            rx.vstack(
                line("#6272a4", "# Python code gets reviewed instantly"),
                line("#ff79c6", "def find_duplicates(items: list) -> list:"),
                line("#f8f8f2", "    seen, dupes = set(), []"),
                line("#f8f8f2", "    for item in items:"),
                line("#f8f8f2", "        if item in seen:"),
                line("#f8f8f2", "            dupes.append(item)"),
                line("#f8f8f2", "        seen.add(item)"),
                line("#ff79c6", "    return dupes"),
                line("#6272a4", ""),
                line("#50fa7b", "# ✓ No syntax errors found"),
                line("#f1fa8c", "# ⚠ Suggestion: use a set comprehension"),
                spacing="0",
                align="start",
                width="100%",
            ),
            padding="16px 20px",
            background="#1a1b26",
            overflow_x="auto",
        ),
        border="1px solid #2a2a35",
        border_radius="12px",
        overflow="hidden",
        box_shadow="0 24px 60px rgba(0,0,0,0.6)",
        width="100%",
    )


def index() -> rx.Component:
    return rx.box(
        navbar(),

        # CSS injected for grid bg + fade-up animations
        rx.html("""
        <style>
        .grid-bg {
            position:absolute; inset:0; z-index:0; pointer-events:none;
            background-image:
                linear-gradient(rgba(59,130,246,0.045) 1px, transparent 1px),
                linear-gradient(90deg,rgba(59,130,246,0.045) 1px,transparent 1px);
            background-size:44px 44px;
            -webkit-mask-image:radial-gradient(ellipse 90% 60% at 50% 0%,black 40%,transparent 100%);
            mask-image:radial-gradient(ellipse 90% 60% at 50% 0%,black 40%,transparent 100%);
        }
        .glow-orb {
            position:absolute; width:700px; height:700px; border-radius:50%; pointer-events:none;
            background:radial-gradient(circle,rgba(59,130,246,0.10) 0%,transparent 70%);
            top:-150px; left:50%; transform:translateX(-50%); z-index:0;
        }
        @keyframes fadeUp {
            from{opacity:0;transform:translateY(20px);}
            to{opacity:1;transform:translateY(0);}
        }
        .a1{animation:fadeUp 0.65s 0.05s ease both;}
        .a2{animation:fadeUp 0.65s 0.18s ease both;}
        .a3{animation:fadeUp 0.65s 0.30s ease both;}
        .a4{animation:fadeUp 0.65s 0.42s ease both;}
        </style>
        <div class="grid-bg"></div>
        <div class="glow-orb"></div>
        """),

        # ── HERO ────────────────────────────────────────
        rx.center(
            rx.hstack(
                # Left: text content
                rx.vstack(
                    rx.box(_badge("v2.0 · AI-Powered Analysis"), class_name="a1"),
                    rx.box(
                        rx.text(
                            "Review Python code",
                            font_family=FONT_DISPLAY,
                            font_size=rx.breakpoints(initial="32px", md="48px"),
                            font_weight="800",
                            color=TEXT_PRIMARY,
                            line_height="1.1",
                            letter_spacing="-0.03em",
                        ),
                        rx.text(
                            "at the speed of thought.",
                            font_family=FONT_DISPLAY,
                            font_size=rx.breakpoints(initial="32px", md="48px"),
                            font_weight="800",
                            color=ACCENT,
                            line_height="1.1",
                            letter_spacing="-0.03em",
                        ),
                        class_name="a2",
                    ),
                    rx.box(
                        rx.text(
                            "Paste any Python snippet — get instant AST analysis, "
                            "logic flaw detection, and Claude-powered suggestions.",
                            font_family=FONT_DISPLAY,
                            font_size="15px",
                            color=TEXT_SECONDARY,
                            line_height="1.75",
                            max_width="420px",
                        ),
                        class_name="a3",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.link(
                                rx.box(
                                    rx.text(
                                        "→ Start Analyzing",
                                        font_family=FONT_MONO,
                                        font_size="13px",
                                        font_weight="600",
                                        color="white",
                                    ),
                                    padding="11px 26px",
                                    background=ACCENT,
                                    border_radius="10px",
                                    transition="all 0.18s",
                                    _hover={"background": "#2563eb", "transform": "translateY(-1px)"},
                                ),
                                href="/analyzer",
                                text_decoration="none",
                            ),
                            rx.link(
                                rx.box(
                                    rx.text(
                                        "Learn more ↗",
                                        font_family=FONT_MONO,
                                        font_size="12px",
                                        font_weight="500",
                                        color=TEXT_SECONDARY,
                                    ),
                                    padding="11px 20px",
                                    background="transparent",
                                    border_radius="10px",
                                    border="1px solid #3a3a48",
                                    transition="all 0.18s",
                                    _hover={"border_color": TEXT_SECONDARY},
                                ),
                                href="/about",
                                text_decoration="none",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        class_name="a4",
                    ),
                    spacing="6",
                    align="start",
                    flex="1",
                    min_width="0",
                ),
                # Right: code preview (hidden on mobile)
                rx.box(
                    _code_preview(),
                    flex="1",
                    min_width="0",
                    display=rx.breakpoints(initial="none", lg="block"),
                    class_name="a3",
                ),
                spacing="9",
                align="center",
                width="100%",
                max_width="1000px",
            ),
            padding_x="32px",
            padding_y="80px",
            width="100%",
            position="relative",
            z_index="1",
        ),

        # ── STATS STRIP ─────────────────────────────────
        rx.center(
            rx.box(
                rx.hstack(
                    _stat("< 2s", "Analysis time"),
                    rx.box(width="1px", height="36px", background=BG_BORDER),
                    _stat("5+", "Check types"),
                    rx.box(width="1px", height="36px", background=BG_BORDER),
                    _stat("AST", "Parser engine"),
                    rx.box(width="1px", height="36px", background=BG_BORDER),
                    _stat("Diff", "Code compare"),
                    spacing="6",
                    align="center",
                    justify="center",
                    flex_wrap="wrap",
                    width="100%",
                ),
                padding="24px 40px",
                background=BG_SURFACE,
                border="1px solid #2a2a35",
                border_radius="14px",
                width="100%",
                max_width="680px",
            ),
            padding_x="32px",
            padding_bottom="72px",
            width="100%",
            position="relative",
            z_index="1",
        ),

        # ── FEATURE GRID ────────────────────────────────
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "What gets checked",
                        font_family=FONT_DISPLAY,
                        font_size="24px",
                        font_weight="700",
                        color=TEXT_PRIMARY,
                        text_align="center",
                        letter_spacing="-0.02em",
                    ),
                    rx.text(
                        "Every run executes all checks in sequence",
                        font_family=FONT_DISPLAY,
                        font_size="13px",
                        color=TEXT_MUTED,
                        text_align="center",
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                ),
                rx.grid(
                    _feature_card("🔍", "Syntax Checking",
                        "AST parsing catches every syntax error with exact line numbers.",
                        "ast.parse()", glow="#3b82f6"),
                    _feature_card("🔄", "Infinite Loop Guard",
                        "Detects while loops with no reachable exit to prevent hangs.",
                        "CFG analysis", glow="#8b5cf6"),
                    _feature_card("🧹", "Dead Code Detection",
                        "Flags unused variables and imports that clutter your namespace.",
                        "scope walk", glow="#22c55e"),
                    _feature_card("🤖", "AI Suggestions",
                        "Claude reads your code and issues, then writes specific advice.",
                        "claude AI", glow="#f59e0b"),
                    _feature_card("🔀", "Side-by-Side Diff",
                        "Original vs AI-improved code shown in two aligned columns.",
                        "diff view", glow="#ef4444"),
                    _feature_card("⚡", "Instant Results",
                        "All checks complete in under two seconds with no spinner.",
                        "< 2s", glow="#06b6d4"),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="4",
                    width="100%",
                ),
                spacing="8",
                align="center",
                width="100%",
                max_width="960px",
            ),
            padding_x="32px",
            padding_bottom="80px",
            width="100%",
            position="relative",
            z_index="1",
        ),

        # ── BOTTOM CTA ──────────────────────────────────
        rx.center(
            rx.box(
                rx.vstack(
                    rx.text(
                        "Ready to write better Python?",
                        font_family=FONT_DISPLAY,
                        font_size="26px",
                        font_weight="700",
                        color=TEXT_PRIMARY,
                        text_align="center",
                        letter_spacing="-0.02em",
                    ),
                    rx.text(
                        "No account required. Paste your code and get results instantly.",
                        font_family=FONT_DISPLAY,
                        font_size="14px",
                        color=TEXT_MUTED,
                        text_align="center",
                    ),
                    rx.link(
                        rx.box(
                            rx.text(
                                "→ Open the Analyzer",
                                font_family=FONT_MONO,
                                font_size="13px",
                                font_weight="600",
                                color="white",
                            ),
                            padding="12px 32px",
                            background=ACCENT,
                            border_radius="10px",
                            transition="all 0.18s",
                            _hover={"background": "#2563eb"},
                        ),
                        href="/analyzer",
                        text_decoration="none",
                    ),
                    spacing="5",
                    align="center",
                ),
                padding="52px 40px",
                background=BG_SURFACE,
                border="1px solid #2a2a35",
                border_radius="20px",
                width="100%",
                max_width="580px",
            ),
            padding_x="32px",
            padding_bottom="80px",
            width="100%",
            position="relative",
            z_index="1",
        ),

        background=BG_BASE,
        width="100%",
        min_height="100vh",
        position="relative",
        overflow="hidden",
    )