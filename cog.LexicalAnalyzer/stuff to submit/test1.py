import unittest
from lexer import analyze, classify_token

class TestLexer(unittest.TestCase):
    
    def test_analyze(self):
        expected_tokens = ['while', '(', 'maxer', '>', 'lower', ')', 'f', '=', '50.00', ';']
        actual_tokens = analyze("test1.txt")
        self.assertEqual(actual_tokens, expected_tokens)

    def test_classify_token(self):
        tokens = ['while', '(', 'maxer', '>', 'lower', ')', 'f', '=', '50.00', ';']
        expected_classifications = [
            ('keyword', 'while'),
            ('separator', '('),
            ('identifier', 'maxer'),
            ('operator', '>'),
            ('identifier', 'lower'),
            ('separator', ')'),
            ('identifier', 'f'),
            ('operator', '='),
            ('real', '50.00'),
            ('separator', ';')
        ]
        actual_classifications = classify_token(tokens)
        self.assertEqual(actual_classifications, expected_classifications)

if __name__ == '__main__':
    unittest.main()
