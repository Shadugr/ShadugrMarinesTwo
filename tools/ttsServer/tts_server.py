from flask import Flask, json
from flask import request
from local_coqui import tts_creator

api = Flask(__name__)

host = "127.0.0.1"
port = 5000

# Initialize TTS creator once at startup
print("Initializing Coqui TTS model (this may take a moment)...")
tts_module = tts_creator()
print("TTS model loaded successfully!")

# Print available speakers
speakers = tts_module.get_available_speakers()
if speakers:
    print(f"Available speakers: {speakers[:10]}...")  # Show first 10
    print(f"Total speakers available: {len(speakers)}")


# Packaging response into Silero API-like format for compatibility
def build_response(audio):
    results = [{'chunk_len': 0, 'chunk_text': "string", "audio": audio, "world_align": [None]}]
    original_sha1 = "string"
    remote_id = "string"
    timings = {"003_tts_time": 0.5}  # Dummy timing for compatibility
    payload = {
        'results': results,
        'original_sha1': original_sha1,
        'remote_id': remote_id,
        'timings': timings
    }
    return payload


# Get request, consume text, make tts, build response, return to sender.
@api.route('/tts/', methods=['POST'])
def process_tts():
    request_data = request.get_json()
    text = request_data['text']
    speaker = request_data.get('speaker', None)
    sample_rate = request_data.get('sample_rate', 24000)

    print(f'Got request with text "{text}" and speaker: "{speaker}"')

    try:
        audio = tts_module.make_ogg_base64(text=text, speaker=speaker, sample_rate=sample_rate)
        payload = build_response(audio)
        return json.dumps(payload)
    except Exception as e:
        print(f"TTS Error: {e}")
        return json.dumps({"error": str(e)}), 500


@api.route('/speakers/', methods=['GET'])
def get_speakers():
    """Endpoint to list available speakers."""
    speakers = tts_module.get_available_speakers()
    return json.dumps({"speakers": speakers})


if __name__ == '__main__':
    # Note: if you don't change host and port, default setting to import to config will be "http://127.0.0.1:5000/tts/"
    print(f'Server is starting up. TTS URL: "http://{host}:{port}/tts/"')
    print(f'Speaker list URL: "http://{host}:{port}/speakers/"')
    api.run(host=host, port=port)
