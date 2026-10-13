"""Independent calculations and case separation for revised learning material."""
from decimal import Decimal
from pathlib import Path
import json
import re
import random
import sys
import unittest

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from check_sampling import case,sample_check
CATALOG=json.loads((APP/'public/catalog.json').read_text(encoding='utf-8'))
UNITS={u['id']:u for u in CATALOG['units']}
BANK=json.loads((APP/'content/checkpoints.json').read_text(encoding='utf-8'))


class Learning117Tests(unittest.TestCase):
    def questions(self,unit):
        return UNITS[unit]['practice']+BANK[unit]

    def test_receipt_totals_use_every_quantity_and_one_envelope(self):
        checked=0
        for q in self.questions('math-5'):
            if q['kind']!='number':continue
            text=q['prompt']
            single=re.search(r'One card costs ([\d.]+) dollars\. What do (\d+) cards cost',text)
            mixed=re.search(r'(\d+) cards at ([\d.]+) dollars each and one envelope at ([\d.]+) dollars',text)
            if single:expected=Decimal(single[1])*int(single[2])
            elif mixed:expected=int(mixed[1])*Decimal(mixed[2])+Decimal(mixed[3])
            else:self.fail('Unverified receipt calculation: '+text)
            self.assertEqual(Decimal(str(q['answer'])),expected,q['id']);checked+=1
        self.assertEqual(checked,18)

    def test_ratios_keep_the_parts_in_the_stated_order(self):
        checked=0
        for q in self.questions('math-6'):
            if q['kind']!='number':continue
            scale=re.search(r'(\d+) cups of water for every 1 cup of concentrate.*for (\d+) cups of concentrate',q['prompt'])
            rate=re.search(r'(\d+) cups concentrate and (\d+) cups water',q['prompt'])
            if scale:expected=int(scale[1])*int(scale[2])
            elif rate:expected=Decimal(rate[2])/Decimal(rate[1])
            else:self.fail('Unverified mixture calculation: '+q['prompt'])
            self.assertEqual(Decimal(str(q['answer'])),expected,q['id']);checked+=1
        self.assertEqual(checked,18)

    def test_rate_and_cost_questions_include_the_values_they_use(self):
        checked=0
        for q in self.questions('math-12'):
            if q['kind']!='number':continue
            text=q['prompt']
            if 'per hour?' in text:
                numbers=re.findall(r'\d+',text);expected=Decimal(numbers[0])/Decimal(numbers[1])
            elif 'same average rate' in text:
                numbers=re.findall(r'\d+',text);expected=Decimal(numbers[0])/Decimal(numbers[1])*Decimal(numbers[2])
            elif 'difference between' in text:
                quantity=int(re.search(r'For (\d+) boxes',text)[1]);expected=abs((6+2*quantity)-(2+3*quantity))
            elif 'does B cost' in text:
                quantity=int(re.search(r'For (\d+) boxes',text)[1]);expected=1+3*quantity
            else:self.fail('Unverified rate or quote calculation: '+text)
            self.assertEqual(Decimal(str(q['answer'])),expected,q['id']);checked+=1
        self.assertEqual(checked,18)

    def test_related_answers_cannot_appear_together_in_a_check(self):
        for uid in ['math-5','math-6','math-12']:
            for seed in range(100):
                selected=sample_check(BANK[uid],UNITS[uid]['checkSkills'],random.Random(seed))
                self.assertEqual(len({case(q) for q in selected}),6,uid)
                self.assertEqual({q['lesson'] for q in selected},{1,2},uid)


if __name__=='__main__':unittest.main()
