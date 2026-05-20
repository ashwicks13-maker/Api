from flask import Flask, request, jsonify
import cloudscraper

app = Flask(__name__)

# Cloudscraper ile session oluştur
scraper = cloudscraper.create_scraper()

@app.route('/api/kullanici', methods=['GET'])
def kullanici_sorgula():
    ad = request.args.get('ad', '').strip()
    soyad = request.args.get('soyad', '').strip()
    
    if not ad or not soyad:
        return jsonify({
            "success": False,
            "error": "ad ve soyad parametreleri gerekli"
        }), 400
    
    try:
        url = "https://arastir.vip/api/adsoyad.php"
        params = {"adi": ad, "soyadi": soyad}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Cloudscraper ile istek yap
        response = scraper.get(url, params=params, headers=headers, timeout=30)
        
        # JSON mı dönüyor kontrol et
        try:
            data = response.json()
            return jsonify({
                "success": True,
                "ad": ad,
                "soyad": soyad,
                "data": data
            })
        except:
            return jsonify({
                "success": True,
                "ad": ad,
                "soyad": soyad,
                "data": response.text
            })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "api": "Kullanıcı Sorgulama API",
        "endpoint": "/api/kullanici?ad=eymen&soyad=yavuz"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
