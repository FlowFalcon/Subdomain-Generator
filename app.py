from flask import Flask, render_template, request, jsonify
import json
import requests
import os

app = Flask(__name__)

def load_zones():
    try:
        with open('zones.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading zones: {e}")
        return {}

@app.route('/')
def index():
    zones = load_zones()
    # Convert dict_keys to list untuk menghindari error serialisasi
    domains = list(zones.keys())
    return render_template('index.html', domains=domains)

@app.route('/create_subdomain', methods=['POST'])
def create_subdomain():
    try:
        data = request.get_json()
        
        subdomain = data['subdomain']
        domain = data['domain']
        record_type = data['type']
        content = data['content']
        proxied = data['proxied']
        
        zones = load_zones()
        
        if domain not in zones:
            return jsonify({'success': False, 'message': 'Domain tidak ditemukan'}), 400
            
        zone_id = zones[domain]['zone_id']
        api_key = zones[domain]['api_key']
        
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        dns_record = {
            'type': record_type,
            'name': f'{subdomain}.{domain}',
            'content': content,
            'proxied': proxied
        }
        
        response = requests.post(url, headers=headers, json=dns_record)
        return jsonify(response.json())
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
