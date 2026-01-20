from app.viz_utils import color_rate
import pandas as pd


def test_color_rate():
    df = pd.DataFrame({
        'average_rate': [3.1, 3.2, 3.3]
    })
    assert color_rate(3.3, df) == 'background-color: green; color: white'
    assert color_rate(3.1, df) == 'background-color: red; color: white'
    assert color_rate(3.2, df) == ''
