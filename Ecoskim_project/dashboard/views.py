from django.shortcuts import render
from urllib.request import urlopen
from urllib.error import URLError
import json


ESP32_IP = "10.129.29.174"


def dashboard(request):

    try:
        response = urlopen(
            f"http://{ESP32_IP}/status",
            timeout=2
        )

        data = json.loads(response.read().decode())

        esp32_status = data.get("status", "offline")

    except (URLError, json.JSONDecodeError):
        esp32_status = "offline"

    return render(request, 'dashboard.html', {
        'esp32_status': esp32_status
    })


def send_command(request):

    command = request.GET.get("move", "S")

    try:
        response = urlopen(
            f"http://{ESP32_IP}/command?move={command}",
            timeout=2
        )

        result = response.read().decode()

    except URLError:
        result = "ESP32 OFFLINE"

    return render(request, 'dashboard.html', {
        'esp32_status': 'online',
        'command_result': result,
        'current_command': result
    })

def live_monitoring(request):
    return render(request, 'live_monitoring.html')