"""Optional CrewAI adapter.

The core app uses deterministic specialist functions so it runs without an LLM key.
When ready, install `crewai` and implement Crew/Agent/Task orchestration here.
See https://docs.crewai.com/ for current APIs. Do not claim this fallback is CrewAI.
"""
def specialist_advisory(inputs: dict, prediction: dict, sources: list[dict]) -> dict:
    soil_notes = []
    if inputs["ph"] < 5.5:
        soil_notes.append("The entered pH is acidic; confirm with a soil test before considering amendments.")
    elif inputs["ph"] > 7.5:
        soil_notes.append("The entered pH is alkaline; verify local nutrient availability guidance.")
    else:
        soil_notes.append("The entered pH is within a broad mid-range; crop-specific suitability still varies.")
    weather_notes = [
        "Temperature and humidity are interpreted as entered values, not a forecast.",
        "Rainfall total alone cannot establish irrigation needs; timing and soil drainage matter."
    ]
    crop_notes = [
        f"The ML model's leading class is {prediction['crop']}.",
        "Check local season, seed availability, market demand, disease pressure and district-level guidance."
    ]
    report = {
        "soil_agent": soil_notes,
        "weather_agent": weather_notes,
        "crop_agent": crop_notes,
        "report_agent": "Combine the model result with the retrieved sources and field observations before making a planting decision."
    }
    return {"location": inputs.get("location", "Not specified"), "prediction": prediction, "specialists": report,
            "sources": [{"title": d["title"], "source": d["source"]} for d in sources],
            "notice": "Prototype advisory, not a validated agronomic prescription."}
