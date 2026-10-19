# Small reviewed starter corpus. Expand with locally relevant, authoritative sources.
# The retrieval implementation is TF-IDF to keep setup simple and deterministic.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = [
 {"id":"soil-ph", "title":"Soil pH and nutrient availability", "source":"https://www.fao.org/soils-portal/",
  "text":"Soil pH affects nutrient availability and microbial activity. Test soil using a calibrated method and interpret results with local extension guidance. Amendments should be based on soil test results rather than guesswork."},
 {"id":"soil-test", "title":"Soil testing and nutrient management", "source":"https://www.fao.org/soils-portal/soil-management/",
  "text":"Soil testing helps determine nutrient status and guide fertilizer decisions. Nitrogen, phosphorus and potassium needs vary by crop, soil type, season, and expected yield. Avoid applying fertilizer solely from a generic recommendation."},
 {"id":"water", "title":"Water management", "source":"https://www.fao.org/land-water/",
  "text":"Crop water requirements depend on crop stage, climate, soil texture, and rainfall distribution. Monitor field conditions and avoid both water stress and waterlogging. Seasonal rainfall totals do not show whether rain arrives at the right time."},
 {"id":"integrated", "title":"Integrated crop management", "source":"https://www.fao.org/plant-production-protection/",
  "text":"Crop choice should consider local climate, soil, seed availability, pest pressure, market access, and planting calendar. Seek region-specific extension advice and use integrated pest management practices."},
 {"id":"bangladesh", "title":"Bangladesh agricultural information", "source":"https://dae.gov.bd/",
  "text":"For Bangladesh-specific crop calendars, pest management and cultivation guidance, consult the Department of Agricultural Extension and local agricultural officers. Recommendations should reflect district, season, irrigation availability and soil test results."}
]
_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
_matrix = _vectorizer.fit_transform([d["title"] + " " + d["text"] for d in DOCS])

def retrieve(question: str, k: int = 3):
    q = _vectorizer.transform([question])
    scores = cosine_similarity(q, _matrix).ravel()
    indexes = scores.argsort()[::-1][:k]
    results = []
    for i in indexes:
        if scores[i] > 0:
            d = DOCS[int(i)]
            results.append({**d, "relevance": round(float(scores[i]), 3)})
    return results

def grounded_answer(question: str, docs: list, api_key: str | None = None, model_name: str = "gemini-2.5-flash"):
    if not docs:
        return "I could not find a sufficiently relevant passage in the current knowledge collection. Please consult a local agricultural extension officer or provide a more specific question."
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            context = "\n\n".join(f"[{d['title']}] {d['text']} Source: {d['source']}" for d in docs)
            prompt = (
                "You are an agricultural information assistant. Answer only from the supplied context. "
                "If context is insufficient, say so. Do not invent pesticide doses or fertilizer rates. "
                "Use cautious language and recommend local extension advice for field-specific decisions. "
                f"Question: {question}\n\nContext:\n{context}"
            )
            response = client.models.generate_content(model=model_name, contents=prompt)
            answer = response.text or "The model did not return a text answer."
            return answer
        except Exception:
            # Keep the app usable if the optional provider is unavailable.
            pass
    return "Based on the retrieved notes: " + " ".join(d["text"] for d in docs) + " This is general information; verify field-specific decisions with local agricultural extension guidance."
