"""Application theming."""

# Python built-in modules:
import os
from rich.console import Console
from rich.theme import Theme

# Local modules:
import settings

cfg = settings.Settings()

# Theme colors.
rich_theme = Theme(cfg.text_colors(), inherit=False)

# Emojis.
theme_emoji = cfg.emojis()

# Create console instance.
console = Console(theme=rich_theme)


def rich_msg(msg: str, msg_type: str):
    """Creates a themed message."""
    msg_list = ["info", "error", "success"]
    theme_type = msg_type.lower().strip()
    if theme_type == "app":
        console.print(f"{msg}", style="app")
    elif theme_type in msg_list:
        console.print(f"{theme_emoji[theme_type]} {msg}", style=theme_type)
    else:
        raise ValueError(f"Please check arguments! msg => '{msg}' ,msg_type => '{msg_type}'")


def rich_header(header_text: str, clear_screen=True):
    """Creates themed application header."""
    if clear_screen:
        if os.name == "posix":
            os.system("clear")
        else:
            os.system("cls")
    console.rule(f"[bold {rich_theme.styles['app']}]{header_text}", characters="=", style="app")
    print("")
