import reflex as rx

# ── Design tokens (inline) ─────────────────────────────
BG_BORDER   = "#2a2a35"
ACCENT      = "#3b82f6"
TEXT_PRIMARY   = "#f1f1f5"
TEXT_SECONDARY = "#8b8b9e"
TEXT_MUTED     = "#52525f"
FONT_DISPLAY   = "'Syne', sans-serif"
FONT_MONO      = "'JetBrains Mono', 'Fira Code', monospace"


def _nav_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        font_family=FONT_DISPLAY,
        font_size="13px",
        font_weight="500",
        color=TEXT_SECONDARY,
        text_decoration="none",
        padding="6px 14px",
        border_radius="10px",
        transition="all 0.18s ease",
        _hover={
            "color": TEXT_PRIMARY,
            "background": "rgba(255,255,255,0.06)",
        },
    )


def navbar() -> rx.Component:
    return rx.box(
        # Thin gradient accent line at the very top
        rx.box(
            height="2px",
            width="100%",
            background="linear-gradient(90deg, transparent 0%, #3b82f6 40%, #8b5cf6 70%, transparent 100%)",
        ),
        # Main nav bar
        rx.hstack(
            # Logo
            rx.hstack(
                rx.box(
                    rx.text(
                        "//",
                        font_family=FONT_MONO,
                        font_size="14px",
                        font_weight="700",
                        color=ACCENT,
                    ),
                    padding="4px 8px",
                    border="1px solid #3b82f6",
                    border_radius="6px",
                    background="rgba(59,130,246,0.08)",
                ),
                rx.text(
                    "CodeReview",
                    font_family=FONT_DISPLAY,
                    font_size="15px",
                    font_weight="700",
                    color=TEXT_PRIMARY,
                    letter_spacing="-0.01em",
                ),
                rx.text(
                    ".ai",
                    font_family=FONT_MONO,
                    font_size="13px",
                    color=ACCENT,
                ),
                spacing="2",
                align="center",
            ),

            rx.spacer(),

            # Nav links
            rx.hstack(
                _nav_link("Home", "/"),
                _nav_link("Analyzer", "/analyzer"),
                _nav_link("About", "/about"),
                spacing="1",
                align="center",
            ),

            rx.spacer(),

            # CTA
            rx.link(
                rx.box(
                    rx.text(
                        "→ Analyze Code",
                        font_family=FONT_MONO,
                        font_size="11px",
                        font_weight="600",
                        color=ACCENT,
                        letter_spacing="0.02em",
                    ),
                    padding="7px 16px",
                    border="1px solid rgba(59,130,246,0.40)",
                    border_radius="8px",
                    background="rgba(59,130,246,0.07)",
                    transition="all 0.18s ease",
                    _hover={
                        "background": "rgba(59,130,246,0.16)",
                        "border_color": "#3b82f6",
                    },
                ),
                href="/analyzer",
                text_decoration="none",
            ),

            width="100%",
            align="center",
            padding="12px 40px",
        ),
        width="100%",
        background="rgba(10,10,15,0.88)",
        border_bottom="1px solid #2a2a35",
        position="sticky",
        top="0",
        z_index="200",
        backdrop_filter="blur(16px)",
    )