import unittest
import logging
from parsing.lexer import TemplateT, Lexer
from pathlib import Path

logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestLexer(unittest.TestCase):
    def test_template(self):
        text = "{{h{{ell{{o}}{{wo}}}}{{rld}}}}"
        match = TemplateT().match(text, 0)
        print(match)
        self.assertIsNotNone(match)

    def test_tokenize(self, name='wikitext'):
        """

        Test tokenizer

        """
        with (DATA_FOLDER / name).open(encoding="utf8") as f:
            text = f.read()
            lexer = Lexer()
            tokens = lexer.tokenize(text)
            logging.info(tokens)
            logging.info('TEXT_LENGTH: {0}'.format(len(text)))
            self.assertGreater(len(tokens), 0)

    # def test_text(self):
    #     TEXT_TOKEN = text_token()
    #     self.assertRegex('The anarchism of [[', TEXT_TOKEN.regex, 'Assert regex dont match')
    #     self.assertEqual(TEXT_TOKEN.match('The anarchism of [[').group(0), 'The anarchism of ')


if __name__ == '__main__':
    unittest.main()
