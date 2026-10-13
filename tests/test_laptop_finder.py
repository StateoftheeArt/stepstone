import unittest
import laptop_finder as finder


class LaptopFinderTests(unittest.TestCase):
    def candidate(self,**extra):
        return dict(title='Test laptop',url='https://www.dell.com/en-ca/shop/test',priceCents=59999,
                    specs=['Intel Core i5-1235U','16 GB DDR4','512 GB SSD','Windows 11 Home','15.6 inch FHD (1920x1080)'],
                    store='Dell Canada',sku='one-exact-sku',inStock=True)|extra
    def test_rejects_unverified_configuration_condition_and_old_processors(self):
        self.assertIsNotNone(finder.qualify(self.candidate()))
        for specs in [
            ['Intel Core i5-8250U','16 GB DDR4','512 GB SSD','Windows 11','1920x1080'],
            ['AMD Ryzen 5 7520U','16 GB RAM','512 GB SSD','Windows 11','FHD'],
            ['Intel Core i5-1235U','8 GB RAM','512 GB SSD','Windows 11','FHD'],
            ['Intel Core i5-1235U','16 GB RAM','256 GB SSD','Windows 11','FHD'],
            ['Intel Core i5-1235U','16 GB RAM','1 TB HDD','Windows 11','FHD'],
            ['Intel Core i5-1235U','16 GB RAM','512 GB SSD','Windows 11','HD (1366x768)']]:
            self.assertIsNone(finder.qualify(self.candidate(specs=specs)),specs)
        for title in ('Refurbished test','Open box laptop','Renewed laptop','Used laptop'):
            self.assertIsNone(finder.qualify(self.candidate(title=title)))
        self.assertIsNone(finder.qualify(self.candidate(inStock=False)))
        self.assertIsNone(finder.qualify(self.candidate(url='https://untrusted.invalid/test')))
    def test_recent_processor_floor_is_explicit(self):
        for cpu in ('Intel Core Ultra 5 - 225U','Intel Core Ultra 5 - 325','Intel Core i5 - 1334U','Intel Core i5-1235U','Intel Core 5 120U','AMD Ryzen 5 5500U','AMD Ryzen 7 250','AMD Ryzen AI 5 340','Intel Core 7 350U'):
            self.assertTrue(finder.comparable_processor(cpu),cpu)
        for cpu in ('Intel Celeron N4500','Intel Core i5','AMD Ryzen 5','Snapdragon X','Intel Core i7-10510U'):
            self.assertFalse(finder.comparable_processor(cpu),cpu)
    def test_manufacturer_punctuation_keeps_memory_and_storage_attached_to_the_offer(self):
        item=self.candidate(specs=['Intel Core i5 - 1335U','16 GB: LPDDR5, 4800 MT/s (onboard)',
                                  '512 GB, M.2, PCIe NVMe, SSD','Windows 11 Home','FHD+ 1920x1200'])
        result=finder.qualify(item)
        self.assertEqual((result['ramGB'],result['storageGB']),(16,512))
        self.assertIsNone(finder.qualify(item|{'specs':['Intel Core i5 - 1335U','8 GB: DDR5','1 TB HDD',
                                                      '4 GB GDDR6 graphics','Windows 11 Home','FHD']}))
    def test_failures_are_reported_without_inventing_a_price(self):
        def fail(url):raise OSError('network unavailable')
        report=finder.compare(fail)
        self.assertEqual(report['offers'],[])
        self.assertTrue(all(s['status']=='unavailable' for s in report['stores']))
        for url in ('http://www.dell.com/x','https://www.dell.com.evil/x','https://user@www.hp.com/x','https://127.0.0.1/x','https://www.hp.com:8090/x'):
            self.assertFalse(finder.safe_url(url))
