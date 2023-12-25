import requests

url = "https://api.spotify.com/v1/me/player/currently-playing"

payload = {}
headers = {
  'Authorization': 'Bearer BQD2ETUeFb99zT37R3aS_le-ThgR_ztLlNX86c50Aixx2Dew9bEJ-S8h-klEGzJb47lPlZ-AeYTTXiQtoNQ40OwCnIh3xquorS9nTRP31AORZvlcb1-CEWb0KC3-LVgt0YCB9a90YXcCedvqpaInhdA_8DIjgzL9gLsEjql5jJ0-DWn4NySa1ZBXRF83jTBjHolRPcPSVoU'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
