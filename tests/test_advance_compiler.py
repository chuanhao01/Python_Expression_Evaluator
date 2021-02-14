import pytest

from src.advance.expression_evaluator import Evaluator

class TestAdvancedCompiler:
    @pytest.mark.parametrize('text, eval', [
        ('1 + 1', 2),
        ('1', 1),
        ('2 - 3', -1),
        ("'aa' + 'bb'", 'aabb'),
        ('5 // 2', 2),
        ('5 / 2', 2.5),
        ('5 - 2 * 3', -1),
        ('(5 - 2) * 3', 9),
        ('5 - 7%4', 2),
        ('+-+-+-3', -3),
        ('3 - -+-++--2 * 2', -1),
        ('4**5%7', 2),
        ('perm(5, 2)', 20),
    ])
    def test_success(self, text, eval):
        evaluator = Evaluator()
        test_evaluation = evaluator.evaluate(text)
        assert test_evaluation == eval