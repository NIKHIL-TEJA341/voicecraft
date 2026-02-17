from flask import Flask, render_template, request, make_response, jsonify
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/editor')
def editor():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text')
    gender = data.get('gender', 'male')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        # Select voice language/accent based on gender (approximation)
        # gTTS doesn't support specific "male/female" voices directly in the standard API,
        # but we can use different top-level domains (TLDs) to get different accents/tones.
        # usually 'com' is US female, 'co.uk' is UK female.
        # There isn't a direct "Male" voice in standard gTTS without paid APIs.
        # However, for this free requirement, we will stick to standard gTTS which is high quality.
        # To strictly better the experience, we can use different accents.
        
        tld = 'com'
        if gender == 'male':
            # gTTS is limited in gender selection for free endpoint.
            # Using a different accent to distinguish, or just standard voice.
            # NOTE: gTTS provides primarily a female voice. 
            # To get a male voice for *free* is hard without pyttsx3 (local) or EdgeTTS.
            # For now, we will use 'co.uk' for one and 'com' for another to differ.
            tld = 'co.uk' 
        
        tts = gTTS(text=text, lang='en', tld=tld, slow=False)
        
        # Save to memory buffer
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        response = make_response(mp3_fp.read())
        response.headers['Content-Type'] = 'audio/mpeg'
        response.headers['Content-Disposition'] = 'attachment; filename=speech.mp3'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
