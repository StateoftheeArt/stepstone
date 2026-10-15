"""Check the generated walking artwork and attachment boundaries."""
import json
import re
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import pip_profiles as profiles
from pip_drawings import MAKERS
from pixel_art import INK


class PipProfiles(unittest.TestCase):
    def test_generated_profiles_match_source_and_carry_their_faces(self):
        text = (ROOT/'public'/'pip-profile-art.js').read_text(encoding='utf-8')
        art = json.loads(text.split('const ART=', 1)[1].split(';\n', 1)[0])
        for maker in MAKERS:
            name = maker.__name__
            with self.subTest(species=name):
                draw = (profiles.fur_profile if name in profiles.FUR else
                        profiles.bird_profile if name in ('owl', 'duck', 'penguin') else
                        profiles.flying_profile if name in ('bee', 'bat', 'moth') else profiles.small_profile)
                self.assertEqual(art[name], profiles.rig_head(draw(name)[0]))
                svg = ET.fromstring('<svg>'+art[name]+'</svg>')
                head = next(n for n in svg if 'sprite-head' in n.get('class', '').split())
                face = {'sprite-eyes', 'sprite-smile', 'sprite-beak', 'sprite-whiskers', 'sprite-ears'}
                self.assertTrue(any('sprite-eyes' in n.get('class', '').split() for n in head.iter()))
                self.assertFalse(any(face.intersection(n.get('class', '').split()) for n in svg))
                self.assertEqual(art[name].count('<!--pip-headwear-->'), 1)

    def test_paw_highlights_do_not_extend_the_silhouette_as_boxes(self):
        for name, (base, dark, light, _) in profiles.FUR.items():
            with self.subTest(species=name):
                feet = ET.fromstring(profiles.profile_paws((base, dark, light), name))
                for foot in feet:
                    cells = {}
                    for path in foot:
                        for x, y, width, end_x in re.findall(r'M(\d+) (\d+)h(\d+)v1H(\d+)Z', path.get('d')):
                            for px in range(int(x), int(x)+int(width)):
                                cells[px, int(y)] = path.get('fill')
                    self.assertTrue(cells)
                    for (x, y), colour in cells.items():
                        if colour != INK:
                            self.assertTrue(all((x+dx, y+dy) in cells for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]),
                                            'A highlight must stay inside the outlined paw.')


if __name__ == '__main__':
    unittest.main()
