from . import spoti
from flask import request, jsonify
from .utils import search_songs_by_name


@spoti.route('/search', methods=['GET'])
def search_songs():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing search query"}), 400
    try:
        search_results = search_songs_by_name(query)
        tracks = [
            {
                "name": item['name'],
                "artist": [artist['name'] for artist in item['artists']],
                "album": item['album']['name'],
                "release_date": item['album']['release_date'],
                "duration_ms": item['duration_ms'],
                "preview_url": item.get('preview_url')
            }
            for item in search_results['tracks']['items']
        ]
        return jsonify(tracks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500