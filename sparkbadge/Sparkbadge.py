from pybadges import badge
from .sparkline import trend, browser_preview
import tempfile
import os


class Sparkbadge:
    def __init__(
        self,
        metric_data: list[float],
        metric_name: str,
        right_text: str,
        line_color: str = "green",
        line_width: int = 2,
        middle_color: str = "#555",
        left_color: str = "#555",
        right_color: str = "#007ec6",
        whole_link: str | None = None,
    ):
        """Initializes with a badge containing a sparkline for the given metric data"""

        self._sparkline = trend(
            samples=metric_data, stroke_color=line_color, stroke_width=line_width
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg") as line:
            line.write(self._sparkline)
            line.flush()
            self.badge = badge(
                center_image=line.name,
                center_color=middle_color,
                left_text=metric_name,
                left_color=left_color,
                right_text=right_text,
                right_color=right_color,
                whole_link=whole_link,
                embed_center_image=True,
            )

    def preview(self) -> None:
        """Previews the badge in webbrowser"""
        browser_preview(self.badge)

    def save_as_svg(self, dir_path: str) -> None:
        full_path = os.path.join(dir_path, "sparkbadge.svg")
        with open(full_path, "w") as file:
            file.write(self.badge)
