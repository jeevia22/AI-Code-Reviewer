import reflex as rx

# ── Load .env for local development ──────────────────────────────────────────
# python-dotenv is a dev dependency only.  On reflex deploy the secret is
# injected directly into os.environ via --env, so load_dotenv() is a no-op
# (it never overwrites existing env vars).  Safe to call unconditionally.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed in prod image — that's fine

# ── Reflex config ─────────────────────────────────────────────────────────────
config = rx.Config(
    app_name="ai_code_reviewer",
    plugins=[rx.plugins.SitemapPlugin()],
)