"""Draw original value diagrams; these do not reproduce Canadian currency art.

Copyright 2026 Stepstone contributors. MIT, as in the root LICENSE.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='tools' else Path(__file__).parent/'repository'
OUT=ROOT/'public/money'

def svg(name,width,height,body,title,description):
    # Only geometric primitives and our text are used. No photos, logos, copied
    # portraits, engraved currency designs, external fonts or linked resources.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description} Original Stepstone value diagram.</desc>
<g font-family="sans-serif" text-anchor="middle">{body}</g></svg>\n'''

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    items={
      'cad-10-value119.svg':svg('ten',150,300,
        '<rect x="4" y="4" width="142" height="292" rx="16" fill="#e8ddfa" stroke="#50346b" stroke-width="5"/><path d="M20 58H130M20 238H130" stroke="#50346b" stroke-width="3"/><text x="75" y="38" font-size="22" fill="#39224e">CAD</text><text x="75" y="158" font-size="61" font-weight="700" fill="#39224e">$10</text><text x="75" y="203" font-size="22" fill="#39224e">ten dollars</text><text x="75" y="271" font-size="14" fill="#39224e">value diagram</text>',
        'Ten Canadian dollars','$10, ten dollars, represented by a purple rectangular value diagram.'),
      'cad-5-value119.svg':svg('five',260,144,
        '<rect x="4" y="4" width="252" height="136" rx="15" fill="#d4e9ff" stroke="#205276" stroke-width="5"/><text x="42" y="30" font-size="19" fill="#173d59">CAD</text><text x="130" y="86" font-size="58" font-weight="700" fill="#173d59">$5</text><text x="130" y="117" font-size="18" fill="#173d59">five dollars · value diagram</text>',
        'Five Canadian dollars','$5, five dollars, represented by a blue rectangular value diagram.'),
      'cad-toonie-value119.svg':svg('toonie',100,100,
        '<circle cx="50" cy="50" r="46" fill="#e0e6e8" stroke="#39434b" stroke-width="4"/><circle cx="50" cy="50" r="34" fill="#f4d68a" stroke="#655024" stroke-width="2"/><text x="50" y="28" font-size="13" fill="#35280f">CAD</text><text x="50" y="62" font-size="34" font-weight="700" fill="#35280f">$2</text><text x="50" y="82" font-size="12" fill="#35280f">toonie</text>',
        'Two Canadian dollars','$2, two dollars, the value of a toonie, represented by a circular value diagram.'),
      'cad-loonie-value119.svg':svg('loonie',100,100,
        '<circle cx="50" cy="50" r="46" fill="#f4d68a" stroke="#655024" stroke-width="4"/><circle cx="50" cy="50" r="39" fill="none" stroke="#655024" stroke-width="1.5"/><text x="50" y="28" font-size="13" fill="#35280f">CAD</text><text x="50" y="62" font-size="35" font-weight="700" fill="#35280f">$1</text><text x="50" y="82" font-size="12" fill="#35280f">loonie</text>',
        'One Canadian dollar','$1, one dollar, the value of a loonie, represented by a circular value diagram.'),
      'cad-quarter-value119.svg':svg('quarter',100,100,
        '<circle cx="50" cy="50" r="46" fill="#e0e6e8" stroke="#39434b" stroke-width="4"/><circle cx="50" cy="50" r="39" fill="none" stroke="#39434b" stroke-width="1.5"/><text x="50" y="28" font-size="13" fill="#263138">CAD</text><text x="50" y="62" font-size="32" font-weight="700" fill="#263138">25¢</text><text x="50" y="82" font-size="12" fill="#263138">quarter</text>',
        'Twenty-five Canadian cents','25 cents, one quarter of a dollar, represented by a circular value diagram.')
    }
    for name,markup in items.items():(OUT/name).write_text(markup,encoding='utf-8',newline='\n')
    print(f'Built {len(items)} original Canadian-dollar value diagrams.')

if __name__=='__main__':build()
