from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

@app.route('/cookie_login', methods=['POST'])
def cookie_login():
    data = request.get_json()
    required_fields = ['tdid', 'ssid', 'sub', 'csid', 'clid']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    tdid = data['tdid']
    ssid = data['ssid']
    sub = data['sub']
    csid = data['csid']
    clid = data['clid']

    params = {
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'client_id': 'play-valorant-web-prod',
        'response_type': 'token id_token',
        'nonce': '1',
        'scope': 'account openid'
    }

    try:
        response = requests.get('https://auth.riotgames.com/authorize',params=params,cookies={'tdid': tdid,'ssid': ssid,'sub': sub,'csid': csid,'clid': clid},allow_redirects=False)
        if 'access_token' not in response.headers.get('Location', ''):
            return jsonify({'error': 'Invalid Cookie or Redirect'}), 401
        
        access_token = parse_qs(urlparse(response.headers.get('Location', '')).fragment).get('access_token', [None])[0]

        if not access_token:
            return jsonify({'error': 'Failed to get access token'}), 500

        return jsonify({'success': True, 'access_token': access_token})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
