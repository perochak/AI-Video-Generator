from huggingface_hub import snapshot_download

# Updated: Removed deprecated parameters
snapshot_download(
    repo_id="suhaibrashid17/MMS_TTS_Urdu_3",
    local_dir="./models/urdu_tts",
    force_download=False  # Optional: set to True to re-download
)
