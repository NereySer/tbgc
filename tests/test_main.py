import main

def test_work():
    tester = main.app.test_client()
    
    response = tester.get('/')
    
    assert response.data is None
