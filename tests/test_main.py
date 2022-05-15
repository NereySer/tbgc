import main, os

def test_raising():
    tester = main.app.test_client()
    
    response = tester.get('/check_events?key=WRONG_KEY')
    assert response.status_code == 404
    
    response = tester.get('/check_events?key='+os.getenv('CHECK_KEY'))
    assert response.status_code >= 200 and response.status_code <= 299

def test_notifications():
    tester = main.app.test_client()
    
    response = tester.get('/')
    assert response.status_code >= 200 and response.status_code <= 299
    
    print(response.text)
    assert false
