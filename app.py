from flask import Flask, render_template, request, make_response, jsonify
import edge_tts
import asyncio
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
        # Determine Voice, Rate, and Pitch based on user requirements
        # Male: "base and slow" -> Christopher (Deep), Slow Rate, Lower Pitch
        # Female: "sweet and slow" -> Aria (Sweet/Standard), Slow Rate
        
        voice = 'en-US-ChristopherNeural'
        rate = '-20%' 
        pitch = '-10Hz'

        if gender == 'female':
            voice = 'en-US-AriaNeural'
            rate = '-10%'
            pitch = '+0Hz'

        async def generate_audio():
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            out = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    out.write(chunk["data"])
            out.seek(0)
            return out

        # Run async function in sync route
        mp3_fp = asyncio.run(generate_audio())
        
        response = make_response(mp3_fp.read())
        response.headers['Content-Type'] = 'audio/mpeg'
        response.headers['Content-Disposition'] = 'attachment; filename=speech.mp3'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
