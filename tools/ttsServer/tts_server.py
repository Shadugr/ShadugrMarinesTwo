from flask import Flask, json
from flask import request
from local_coqui import tts_creator, SOUND_EFFECT_NONE
import threading
import queue
import uuid
import time

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

# Request queue for sequential TTS processing
tts_queue = queue.Queue()
results = {}  # Store results by request ID
results_lock = threading.Lock()

# Queue statistics
queue_stats = {
    "processed": 0,
    "failed": 0,
    "start_time": time.time()
}


def tts_worker():
    """Worker thread that processes TTS requests sequentially."""
    while True:
        try:
            # Get next request from queue
            request_id, text, speaker, sample_rate, effect = tts_queue.get()

            print(f"[Queue] Processing request {request_id[:8]}... (queue size: {tts_queue.qsize()})")

            try:
                audio = tts_module.make_ogg_base64(
                    text=text,
                    speaker=speaker,
                    sample_rate=sample_rate,
                    effect=effect
                )
                with results_lock:
                    results[request_id] = {"status": "done", "audio": audio}
                    queue_stats["processed"] += 1
                print(f"[Queue] Completed request {request_id[:8]}")
            except Exception as e:
                print(f"[Queue] Error processing {request_id[:8]}: {e}")
                with results_lock:
                    results[request_id] = {"status": "error", "error": str(e)}
                    queue_stats["failed"] += 1

            tts_queue.task_done()

        except Exception as e:
            print(f"[Queue Worker] Unexpected error: {e}")


# Start the worker thread
worker_thread = threading.Thread(target=tts_worker, daemon=True)
worker_thread.start()
print("TTS queue worker started")


# Packaging response into Silero API-like format for compatibility
def build_response(audio):
    results_data = [{'chunk_len': 0, 'chunk_text': "string", "audio": audio, "world_align": [None]}]
    original_sha1 = "string"
    remote_id = "string"
    timings = {"003_tts_time": 0.5}  # Dummy timing for compatibility
    payload = {
        'results': results_data,
        'original_sha1': original_sha1,
        'remote_id': remote_id,
        'timings': timings
    }
    return payload


@api.route('/tts/', methods=['POST'])
def process_tts():
    request_data = request.get_json()
    text = request_data['text']
    speaker = request_data.get('speaker', None)
    sample_rate = request_data.get('sample_rate', 24000)
    effect = request_data.get('effect', SOUND_EFFECT_NONE)

    # Convert effect to int if it's a string
    if isinstance(effect, str):
        effect = int(effect) if effect.isdigit() else SOUND_EFFECT_NONE

    # Generate unique request ID
    request_id = str(uuid.uuid4())

    print(f'[Queue] Received request {request_id[:8]}: text="{text[:30]}...", speaker="{speaker}", effect={effect}')

    # Add to queue
    tts_queue.put((request_id, text, speaker, sample_rate, effect))

    # Wait for result (with timeout)
    timeout = 120  # 2 minutes max wait
    start_time = time.time()

    while time.time() - start_time < timeout:
        with results_lock:
            if request_id in results:
                result = results.pop(request_id)
                if result["status"] == "done":
                    return json.dumps(build_response(result["audio"]))
                else:
                    return json.dumps({"error": result["error"]}), 500
        time.sleep(0.1)  # Check every 100ms

    # Timeout
    return json.dumps({"error": "TTS request timed out"}), 504


@api.route('/speakers/', methods=['GET'])
def get_speakers():
    """Endpoint to list available speakers."""
    speakers_list = tts_module.get_available_speakers()
    return json.dumps({"speakers": speakers_list})


@api.route('/status/', methods=['GET'])
def get_status():
    """Endpoint to check queue status."""
    uptime = time.time() - queue_stats["start_time"]
    return json.dumps({
        "queue_size": tts_queue.qsize(),
        "processed": queue_stats["processed"],
        "failed": queue_stats["failed"],
        "uptime_seconds": round(uptime, 1),
        "device": tts_module.device
    })


if __name__ == '__main__':
    # Note: if you don't change host and port, default setting to import to config will be "http://127.0.0.1:5000/tts/"
    print(f'Server is starting up. TTS URL: "http://{host}:{port}/tts/"')
    print(f'Speaker list URL: "http://{host}:{port}/speakers/"')
    print(f'Status URL: "http://{host}:{port}/status/"')
    # Use threaded=True to handle multiple incoming HTTP requests, but TTS is still processed sequentially
    api.run(host=host, port=port, threaded=True)
