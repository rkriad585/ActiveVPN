# vpnActive/core/logo.py
import random
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import pyfiglet
from config import APP_NAME, VERSION, AUTHOR

def print_banner(console: Console):
    """
    Generates and prints a colorful ASCII banner.
    """
    # Available fonts in pyfiglet
    fonts = ["slant", "doom", "cyberlarge", "ansi_shadow", "small"]
    selected_font = "slant" # Keeping it readable
    
    # Generate ASCII art
    ascii_art = pyfiglet.figlet_format(APP_NAME, font=selected_font)
    
    # Dynamic list of nice gradients/colors
    colors = ["magenta", "cyan", "green", "bright_blue", "violet"]
    color = random.choice(colors)
    
    # Create the text object
    banner_text = Text(ascii_art, style=color)
    
    # Create a sub-text with version info
    info_text = f"Version: {VERSION} | Author: {AUTHOR}"
    
    # Combine into a panel
    panel = Panel(
        Align.center(banner_text + "\n" + info_text),
        border_style=color,
        expand=False
    )
    
    console.print(panel)
    console.print("\n")
