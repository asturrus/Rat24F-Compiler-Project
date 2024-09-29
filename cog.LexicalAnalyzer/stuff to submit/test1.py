import unittest
from lexer import analyze, classify_token  # Ensure correct imports

class TestLexer(unittest.TestCase):
    
    def test_analyze(self):
        expected_tokens = ['while', '(', 'fahr', '<=', 'upper', ')', 'a', '=', '23.00', ';']
        actual_tokens = analyze("test1.txt")
        self.assertEqual(actual_tokens, expected_tokens)

    def test_classify_token(self):
        tokens = ['while', '(', 'fahr', '<=', 'upper', ')', 'a', '=', '23.00', ';']
        expected_classifications = [
            ('keyword', 'while'),
            ('separator', '('),
            ('identifier', 'fahr'),
            ('operator', '<='),
            ('identifier', 'upper'),
            ('separator', ')'),
            ('identifier', 'a'),
            ('operator', '='),
            ('real', '23.00'),
            ('separator', ';')
        ]
        actual_classifications = classify_token(tokens)
        self.assertEqual(actual_classifications, expected_classifications)

if __name__ == '__main__':
    unittest.main()
