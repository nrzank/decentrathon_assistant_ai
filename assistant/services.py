from assistant.external_services import get_similar_queries
from assistant.models import SearchHistory, Recommendation


def generate_recommendations(user):
    search_history = SearchHistory.objects.filter(user=user).order_by('-timestamp')[:5]

    recommendations = []
    for entry in search_history:
        query = entry.query
        similar_queries = get_similar_queries(query)
        recommendations.extend(similar_queries)

    Recommendation.objects.update_or_create(user=user, defaults={'recommended_queries': recommendations})

    return recommendations
