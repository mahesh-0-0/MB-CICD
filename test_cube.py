from cube import get_cube 

def test_get_cube():
    a = 5
    res = get_cube(a)
    assert res == 125