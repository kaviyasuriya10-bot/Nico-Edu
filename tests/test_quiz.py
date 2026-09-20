def test_quiz_score_math():
 answers={'1':'A','2':'B'};correct={'1':'A','2':'C'}
 assert sum(answers[k]==v for k,v in correct.items())==1
