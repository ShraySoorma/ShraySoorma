"""Generate the self-contained Windows-style profile artwork."""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent.parent


def bevel(x, y, w, h, inset=False):
    light, dark = ('#808080', '#ffffff') if inset else ('#ffffff', '#404040')
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#c0c0c0"/>
    <path d="M{x},{y+h} V{y} H{x+w}" fill="none" stroke="{light}" stroke-width="2"/>
    <path d="M{x+w},{y} V{y+h} H{x}" fill="none" stroke="{dark}" stroke-width="2"/>'''


def svg(w, h, body, export_width=None):
    output_width = export_width or w
    output_height = round(h * output_width / w)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{output_width}" height="{output_height}" viewBox="0 0 {w} {h}">
    <style>text {{ font-family: Arial, Helvetica, sans-serif; fill: #171717; }} .mono {{ font-family: 'Courier New', monospace; }}</style>
    {body}</svg>'''


# Desktop and a classic Properties dialog.
body = '<rect width="820" height="460" fill="#008080"/>'
body += '<rect x="30" y="22" width="772" height="388" fill="#004c4c"/>'
body += bevel(24, 16, 772, 388)
body += '''<defs><linearGradient id="title"><stop stop-color="#000080"/><stop offset="1" stop-color="#1084d0"/></linearGradient></defs>
<rect x="29" y="21" width="762" height="25" fill="url(#title)"/>
<rect x="36" y="27" width="16" height="13" fill="#c0c0c0" stroke="white"/>
<rect x="38" y="29" width="12" height="3" fill="#000080"/>
<text x="60" y="39" font-size="14" font-weight="bold" style="fill:white">System Properties</text>'''
for x, label in [(743, '?'), (767, '×')]:
    body += bevel(x, 25, 19, 17)
    body += f'<text x="{x+9.5}" y="39" text-anchor="middle" font-size="15" font-weight="bold">{label}</text>'
# Draw the panel and open-bottom tabs as continuous borders.
body += '<rect x="40" y="84" width="740" height="255" fill="#c0c0c0"/>'
for x, width, label in [(119, 75, 'Details'), (194, 87, 'Internet')]:
    body += f'<path d="M{x} 84 V63 L{x+2} 61 H{x+width-2} L{x+width} 63 V84" fill="#c0c0c0" stroke="#808080"/>'
    body += f'<path d="M{x+1} 83 V64 L{x+3} 62 H{x+width-2}" fill="none" stroke="white"/>'
    body += f'<text x="{x+width/2}" y="78" text-anchor="middle" font-size="13">{label}</text>'
body += '''<path d="M40 338 V61 L43 58 H116 L119 61 V84 H779" fill="none" stroke="white" stroke-width="2"/>
<path d="M119 61 V83" fill="none" stroke="#808080" stroke-width="2"/>
<path d="M780 84 V339 H40" fill="none" stroke="#404040" stroke-width="2"/>
<text x="79" y="77" text-anchor="middle" font-size="13">General</text>'''
body += bevel(59, 106, 169, 193, True)
art = base64.b64encode((ROOT / 'assets/developer-robot-coding.jpg').read_bytes()).decode()
body += f'<image href="data:image/jpeg;base64,{art}" x="62" y="109" width="163" height="187" preserveAspectRatio="xMidYMid slice"/>'
body += '''<text x="258" y="135" font-size="27" font-weight="bold">Shray Soorma</text>
<path d="M258 156 H755" stroke="#808080"/><path d="M258 157 H755" stroke="white"/>'''
for y, label, value in [
    (188, 'Role:', 'Software Engineer'),
    (220, 'Company:', 'Kyndryl'),
    (252, 'Website:', 'shraysoorma.github.io'),
    (284, 'LinkedIn:', '/in/shray-soorma'),
]:
    body += f'<text x="258" y="{y}" font-size="13">{label}</text>'
    body += f'<text x="352" y="{y}" font-size="13">{value}</text>'
for x, label in [(503, 'OK'), (597, 'Cancel'), (691, 'Apply')]:
    if label == 'OK':
        body += '<rect x="501" y="352" width="86" height="30" fill="none" stroke="#000"/>'
    body += bevel(x, 354, 82, 26)
    color = '#808080' if label == 'Apply' else '#171717'
    body += f'<text x="{x+41}" y="372" text-anchor="middle" font-size="13" style="fill:{color}">{label}</text>'
# Windows taskbar, Start button, and an active application entry.
body += bevel(0, 424, 820, 35)
body += bevel(5, 429, 76, 25)
for x, y, color in [(13, 435, '#f22'), (22, 435, '#00a000'), (13, 444, '#004dff'), (22, 444, '#ffdf00')]:
    body += f'<rect x="{x}" y="{y}" width="7" height="7" fill="{color}"/>'
body += '<text x="36" y="447" font-size="14" font-weight="bold">Start</text>'
body += '<path d="M89 429 V454" stroke="#808080"/><path d="M90 429 V454" stroke="white"/>'
body += bevel(99, 429, 226, 25, True)
body += '<text x="111" y="446" font-size="12" font-weight="bold">System Properties</text>'
body += bevel(683, 429, 130, 25, True)
body += '<text x="748" y="446" text-anchor="middle" font-size="12">Local system</text>'
(ROOT / 'windows-profile.svg').write_text(svg(820, 460, body, export_width=7680))

for filename, label, icon in [('btn-site.svg', 'Terminal', 'terminal'), ('btn-linkedin.svg', 'LinkedIn', 'linkedin')]:
    body = bevel(2, 2, 166, 42)
    body += '<rect x="7" y="7" width="156" height="32" fill="none" stroke="#666" stroke-dasharray="1 2"/>'
    if icon == 'terminal':
        body += '<rect x="21" y="14" width="22" height="18" fill="#111"/><path d="M25 19 L29 23 L25 27 M32 27 H38" stroke="#fff" fill="none" stroke-width="1.5"/>'
    else:
        body += '<rect x="21" y="12" width="22" height="22" fill="#000080"/><text x="32" y="29" text-anchor="middle" font-size="17" font-weight="bold" style="fill:white">in</text>'
    body += f'<text x="56" y="29" font-size="16">{label}</text>'
    (ROOT / filename).write_text(svg(170, 46, body))
