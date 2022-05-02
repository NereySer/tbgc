import main

def test_work():
    tester = main.app.test_client()
    
    response = tester.get('/')
    
    assert response.status >= 200 and response.status <= 299
