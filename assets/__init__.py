from pathlib import Path

app_icon = Path(__file__).parent / "images" / "app_icon.ico"
app_logo = Path(__file__).parent / "images" / "app_logo.png"
back_icon = Path(__file__).parent / "images" / "left_arrow.png"

__all__ = ["app_icon", "app_logo", "left_arrow"]