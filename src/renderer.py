"""
src/renderer.py
Handles dynamic email personalization using Jinja2 or built-in regex templating.
"""
from pathlib import Path
from typing import Dict, Any, Tuple
import re
from .config import TEMPLATES_DIR

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

class EmailRenderer:
    def __init__(self, template_dir: Path = TEMPLATES_DIR):
        self.template_dir = template_dir
        if HAS_JINJA:
            self.env = Environment(
                loader=FileSystemLoader(str(template_dir)),
                autoescape=select_autoescape(['html', 'xml'])
            )

    def _fallback_render(self, template_str: str, context: Dict[str, Any]) -> str:
        """Simple {{ variable }} interpolation using regex for zero-dependency operation."""
        def replacer(match):
            key = match.group(1).strip()
            return str(context.get(key, ""))
        return re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", replacer, template_str)

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Loads a template file and renders it with context variables."""
        if HAS_JINJA:
            template = self.env.get_template(template_name)
            return template.render(**context)
        else:
            filepath = self.template_dir / template_name
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return self._fallback_render(content, context)

    def render_markdown(self, markdown_text: str, context: Dict[str, Any]) -> str:
        """Renders raw markdown string with context, then converts to HTML."""
        if HAS_JINJA:
            template = self.env.from_string(markdown_text)
            rendered_md = template.render(**context)
        else:
            rendered_md = self._fallback_render(markdown_text, context)

        if HAS_MARKDOWN:
            return markdown.markdown(rendered_md, extensions=['extra', 'tables'])
        else:
            return f"<pre>{rendered_md}</pre>"

    def render_subject_and_body(
        self, subject_template: str, template_filename: str, context: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Renders both subject line and HTML body."""
        if HAS_JINJA:
            subj_tmpl = self.env.from_string(subject_template)
            rendered_subject = subj_tmpl.render(**context)
        else:
            rendered_subject = self._fallback_render(subject_template, context)

        rendered_html = self.render_template(template_filename, context)
        return rendered_subject, rendered_html
