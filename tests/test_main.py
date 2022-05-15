import main, os

def test_raising():
    tester = main.app.test_client()
    
    response = tester.get('/check_events?key=WRONG_KEY')
    assert response.status_code == 404
    
    response = tester.get('/check_events?key='+os.getenv('CHECK_KEY'))
    assert response.status_code >= 200 and response.status_code <= 299

def test_notifications(monkeypatch):
    tester = main.app.test_client()
    
    response = tester.get('/')
    assert response.status_code >= 200 and response.status_code <= 299
    
    print(response.text)

    def mock_g_cal_get_incomig_events():
        return []
    
    monkeypatch.setattr(main.g_cal, 'get_incomig_events', mock_g_cal_get_incomig_events)

    response = tester.get('/')
    assert response.status_code >= 200 and response.status_code <= 299
    
    print(response.text)

    assert false
