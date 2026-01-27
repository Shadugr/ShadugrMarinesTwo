/datum/tts_provider/coqui
	name = "Coqui"
	is_enabled = TRUE
	supports_server_effects = TRUE  // Coqui server applies effects

/datum/tts_provider/coqui/request(text, datum/tts_seed/coqui/seed, datum/callback/proc_callback, effect = 0)
	if(throttle_check())
		return FALSE

	// Coqui TTS doesn't support SSML, so we send plain text
	// Include effect parameter for server-side audio processing
	var/list/req_body = list(
		"text" = text,
		"sample_rate" = 24000,
		"speaker" = seed.value,
		"effect" = effect
	)

	SShttp.create_async_request(
		RUSTG_HTTP_METHOD_POST,
		CONFIG_GET(string/tts_api_url_silero),
		json_encode(req_body),
		list("Content-Type" = "application/json"),
		proc_callback
	)
	return TRUE

/datum/tts_provider/coqui/process_response(datum/http_response/response)
	var/data = json_decode(response.body)

	// Check for error response
	if(data["error"])
		log_game("Coqui TTS error: [data["error"]]")
		return null

	return data["results"][1]["audio"]

// Coqui TTS doesn't support SSML prosody tags, so these return text unchanged
/datum/tts_provider/coqui/pitch_whisper(text)
	return text

/datum/tts_provider/coqui/rate_faster(text)
	return text

/datum/tts_provider/coqui/rate_medium(text)
	return text
