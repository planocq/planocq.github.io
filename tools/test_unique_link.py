import unittest
from unittest.mock import patch
import unique_link as g


class GeneratorTests(unittest.TestCase):
    def home(self):
        values = {key: 'Espacio & luz "CQ"' for key in g.KEYS}
        values.update({'og:image': g.BASE + '/approved.jpg', 'twitter:image': g.BASE + '/approved.jpg'})
        return ''.join(f'<meta property="{k}" content="{g.escape(v, quote=True)}">' for k, v in values.items())

    def test_metadata_roundtrip_and_identity(self):
        page = g.render(self.home(), '51')
        actual = g.Metadata(page.split('<body>')[0]).values
        expected = g.Metadata(self.home()).values
        for key in g.KEYS:
            self.assertEqual(actual[key], expected[key])
        self.assertEqual(actual['og:url'], g.BASE + '/1/51/')
        self.assertEqual(actual['canonical'], actual['og:url'])
        self.assertIn('fetch("/")', page)
        self.assertNotIn('location.replace', page)
        self.assertNotIn('location.href =', page)

    def test_invalid_ids(self):
        for value in ['../2', '01', '0', '-1', '1/2', 'x']:
            with self.assertRaises(ValueError):
                g.render(self.home(), value)

    def test_missing_metadata(self):
        with self.assertRaises(ValueError):
            g.render('<html></html>', '1')

    def test_relative_image_rejected(self):
        with self.assertRaises(ValueError):
            g.render(self.home().replace(g.BASE + '/approved.jpg', '/approved.jpg'), '1')

    @patch.object(g, 'api')
    def test_existing_id_never_overwritten(self, api):
        api.side_effect = [{'object': {'sha': 'head'}}, {'tree': {'sha': 'tree'}},
                           {'tree': [{'path': '1/51/index.html'}]}]
        with self.assertRaisesRegex(ValueError, 'ya existe'):
            g.create('51')
        self.assertEqual(api.call_count, 3)

    @patch.object(g, 'api')
    def test_truncated_tree_aborts(self, api):
        api.side_effect = [{'object': {'sha': 'head'}}, {'tree': {'sha': 'tree'}},
                           {'tree': [], 'truncated': True}]
        with self.assertRaisesRegex(ValueError, 'truncado'):
            g.create()


if __name__ == '__main__':
    unittest.main()
