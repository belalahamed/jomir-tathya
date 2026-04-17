from pathlib import Path

app_icon = Path(__file__).parent / "assets" / "images" / "app_icon.ico"
app_logo = Path(__file__).parent / "assets" / "images" / "app_logo.png"

__all__ = ["app_icon", "app_logo"]