import requests
import os

GOOGLE_API = os.getenv("GOOGLE_MAPS_API_KEY")


# ---------------------------
# FIND NEARBY HOSPITALS
# ---------------------------
def find_nearby_hospitals(lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": 15000,
        "type": "hospital",
        "key": GOOGLE_API
    }

    res = requests.get(url, params=params).json()

    hospitals = []

    for r in res.get("results", [])[:5]:
        hospitals.append({
            "name": r["name"],
            "address": r.get("vicinity"),
            "place_id": r["place_id"],
            "lat": r["geometry"]["location"]["lat"],
            "lng": r["geometry"]["location"]["lng"]
        })

    return hospitals


# ---------------------------
# GET PHONE NUMBER
# ---------------------------
def get_phone(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number",
        "key": GOOGLE_API
    }

    res = requests.get(url, params=params).json()

    return res.get("result", {}).get("formatted_phone_number", "Not available")


# ---------------------------
# BUILD EMERGENCY RESPONSE
# ---------------------------
def build_emergency_response(lat, lng):
    hospitals = find_nearby_hospitals(lat, lng)

    messages = [
        {
            "role": "assistant",
            "content": "⚠️ Emergency detected — showing nearest hospitals"
        }
    ]

    for h in hospitals:
        phone = get_phone(h["place_id"])

        maps_link = f"https://www.google.com/maps/dir/?api=1&destination={h['lat']},{h['lng']}"

        text = f"""
        🏥 {h['name']}
        📍 {h['address']}
        📞 {phone}
        🧭 Directions:
        {maps_link}
        """

        messages.append({"role": "assistant", "content": text})
    
    if not hospitals:
        messages.append({
            "role":"assistant",
            "content":"Unable to fetch hospitals. Please open Google Maps and search nearby hospitals."
        })

    return messages