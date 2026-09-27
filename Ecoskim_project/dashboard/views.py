from django.shortcuts import render
from django.db.models import Avg

from urllib.request import urlopen
from urllib.error import URLError

import json

from .models import WasteDetection


# =========================================================
# ESP32 IP ADDRESS
# =========================================================

ESP32_IP = "192.168.29.65"


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    try:

        response = urlopen(
            f"http://{ESP32_IP}/status",
            timeout=2
        )

        data = json.loads(
            response.read().decode()
        )

        esp32_status = data.get(
            "status",
            "offline"
        )

    except (
        URLError,
        json.JSONDecodeError
    ):

        esp32_status = "offline"


    return render(
        request,
        "dashboard.html",
        {
            "esp32_status": esp32_status
        }
    )


# =========================================================
# SEND ESP32 MOVEMENT COMMAND
# =========================================================

def send_command(request):

    command = request.GET.get(
        "move",
        "S"
    )


    try:

        response = urlopen(
            f"http://{ESP32_IP}/command?move={command}",
            timeout=2
        )

        result = response.read().decode()


    except URLError:

        result = "ESP32 OFFLINE"


    return render(
        request,
        "dashboard.html",
        {
            "esp32_status": "online",
            "command_result": result,
            "current_command": result
        }
    )


# =========================================================
# LIVE MONITORING
# =========================================================

def live_monitoring(request):

    return render(
        request,
        "live_monitoring.html"
    )


# =========================================================
# DETECTION HISTORY
# =========================================================

def detection_history(request):

    detections = WasteDetection.objects.all().order_by(
        "-detected_at"
    )


    return render(
        request,
        "detection_history.html",
        {
            "detections": detections
        }
    )


# =========================================================
# ADD DEMO DATA
# =========================================================

def add_demo_data(request):

    WasteDetection.objects.all().delete()


    WasteDetection.objects.create(
        waste_name="Plastic Bottle",
        waste_type="Plastic",
        confidence=94,
        classification="Harmful"
    )


    WasteDetection.objects.create(
        waste_name="Paper",
        waste_type="Paper",
        confidence=91,
        classification="Biodegradable"
    )


    WasteDetection.objects.create(
        waste_name="Metal Can",
        waste_type="Metal",
        confidence=88,
        classification="Harmful"
    )


    WasteDetection.objects.create(
        waste_name="Organic Waste",
        waste_type="Organic",
        confidence=96,
        classification="Biodegradable"
    )


    WasteDetection.objects.create(
        waste_name="Plastic Bag",
        waste_type="Plastic",
        confidence=92,
        classification="Harmful"
    )


    return render(
        request,
        "dashboard.html"
    )


# =========================================================
# ANALYTICS
# =========================================================

def analytics(request):

    # -----------------------------------------------------
    # GET ALL DETECTION RECORDS
    # -----------------------------------------------------

    detections = WasteDetection.objects.all()


    # -----------------------------------------------------
    # TOTAL WASTE
    # -----------------------------------------------------

    total_waste = detections.count()


    # -----------------------------------------------------
    # CLASSIFICATION COUNTS
    # -----------------------------------------------------

    harmful_waste = detections.filter(
        classification="Harmful"
    ).count()


    biodegradable_waste = detections.filter(
        classification="Biodegradable"
    ).count()


    # -----------------------------------------------------
    # WASTE TYPE COUNTS
    # -----------------------------------------------------

    plastic_waste = detections.filter(
        waste_type="Plastic"
    ).count()


    metal_waste = detections.filter(
        waste_type="Metal"
    ).count()


    paper_waste = detections.filter(
        waste_type="Paper"
    ).count()


    organic_waste = detections.filter(
        waste_type="Organic"
    ).count()


    # -----------------------------------------------------
    # AVERAGE DETECTION CONFIDENCE
    # -----------------------------------------------------

    average_confidence = detections.aggregate(
        Avg("confidence")
    )["confidence__avg"]


    if average_confidence is None:

        average_confidence = 0


    # -----------------------------------------------------
    # WASTE COMPOSITION PERCENTAGES
    # -----------------------------------------------------

    if total_waste:

        plastic_percentage = (
            plastic_waste / total_waste
        ) * 100


        paper_percentage = (
            paper_waste / total_waste
        ) * 100


        metal_percentage = (
            metal_waste / total_waste
        ) * 100


        organic_percentage = (
            organic_waste / total_waste
        ) * 100

    else:

        plastic_percentage = 0

        paper_percentage = 0

        metal_percentage = 0

        organic_percentage = 0


    # -----------------------------------------------------
    # DONUT CHART CUMULATIVE VALUES
    # -----------------------------------------------------

    plastic_end = plastic_percentage


    paper_end = (
        plastic_percentage
        + paper_percentage
    )


    metal_end = (
        plastic_percentage
        + paper_percentage
        + metal_percentage
    )


    # -----------------------------------------------------
    # SEND DATA TO ANALYTICS PAGE
    # -----------------------------------------------------

    return render(
        request,
        "analytics.html",
        {

            # Summary cards

            "total_waste": total_waste,

            "harmful_waste": harmful_waste,

            "biodegradable_waste": biodegradable_waste,

            "average_confidence": round(
                average_confidence,
                1
            ),


            # Waste type counts

            "plastic_waste": plastic_waste,

            "metal_waste": metal_waste,

            "paper_waste": paper_waste,

            "organic_waste": organic_waste,


            # Waste type percentages

            "plastic_percentage": round(
                plastic_percentage,
                1
            ),

            "paper_percentage": round(
                paper_percentage,
                1
            ),

            "metal_percentage": round(
                metal_percentage,
                1
            ),

            "organic_percentage": round(
                organic_percentage,
                1
            ),


            # Donut chart values

            "plastic_end": round(
                plastic_end,
                1
            ),

            "paper_end": round(
                paper_end,
                1
            ),

            "metal_end": round(
                metal_end,
                1
            ),

        }
    )