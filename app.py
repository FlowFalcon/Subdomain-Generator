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
    domains = list(zones.keys())
    return render_template('index.html', domains=domains)

@app.route('/create_subdomain', methods=['POST'])
def create_subdomain():
    try:
        data = request.get_json()
        zones = load_zones()
        
        subdomain = data['subdomain']
        domain = data['domain']
        record_type = data['type']
        content = data['content']
        proxied = data['proxied']
        
        if domain not in zones:
            return jsonify({
                'success': False,
                'message': f'Domain {domain} tidak ditemukan'
            }), 400
            
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
        
        print(f"Sending request to Cloudflare: {dns_record}")  # Debug print
        
        response = requests.post(url, headers=headers, json=dns_record)
        response_json = response.json()
        
        print(f"Cloudflare response: {response_json}")  # Debug print
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': f'Subdomain {subdomain}.{domain} berhasil dibuat!'
            })
        else:
            return jsonify({
                'success': False,
                'message': response_json.get('errors', [{'message': 'Unknown error'}])[0]['message']
            }), response.status_code
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
