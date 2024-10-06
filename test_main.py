import pytest
import pandas as pd
from main import process_data

@pytest.fixture
def ai_submissions_df():
    return pd.read_csv('ai-submissions.csv')

def test_process_data(ai_submissions_df):
    result = process_data(ai_submissions_df)
    
    assert isinstance(result, pd.DataFrame)
    
    assert all(isinstance(year, int) for year in result.index)
    assert min(result.index) >= 1995
    assert max(result.index) <= 2024
    
    assert (result.values >= 0).all()
    assert (result.values.astype(int) == result.values).all()
    
    assert (result.values > 0).any()

def test_process_data_empty():
    empty_df = pd.DataFrame(columns=[
        'Date of Final Decision', 'Submission Number', 'Device', 'Company',
        'Panel (lead)', 'Primary Product Code'
    ])
    result = process_data(empty_df)
    
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_process_data_invalid_dates(ai_submissions_df):
    ai_submissions_df.loc[0, 'Date of Final Decision'] = 'Invalid Date'
    ai_submissions_df.loc[1, 'Date of Final Decision'] = '13/13/2023'
    
    result = process_data(ai_submissions_df)
    
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result.index.min() <= 2023
