from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/kullanici', methods=['GET'])
def kullanici_sorgula():
    """GET /api/kullanici?ad=eymen&soyad=yavuz"""
    ad = request.args.get('ad', '').strip()
    soyad = request.args.get('soyad', '').strip()
    
    if not ad or not soyad:
        return jsonify({
            "success": False,
            "error": "ad ve soyad parametreleri gerekli",
            "ornek": "/api/kullanici?ad=eymen&soyad=yavuz"
        }), 400
    
    try:
        url = "https://arastir.vip/api/adsoyad.php"
        params = {"adi": ad, "soyadi": soyad}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        return jsonify({
            "success": True,
            "ad": ad,
            "soyad": soyad,
            "data": response.text
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "İstek zaman aşımına uğradı"}), 504
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "api": "Kullanıcı Sorgulama API",
        "endpoint": "/api/kullanici?ad=eymen&soyad=yavuz",
        "method": "GET"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
