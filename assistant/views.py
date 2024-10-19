from rest_framework import generics, status
from rest_framework.response import Response

from .calendar import create_calendar_event
from .external_services import search_gemini, search_wikipedia
from .models import ExternalSource, Subject, Answer, Question, SearchHistory
from .request_gemini import get_answer_from_gemini
from .agent import Agent
from .serializers import SubjectSerializer, QuestionSerializer, AnswerSerializer
from .services import generate_recommendations

# Инициализируем агента
agent = Agent()


class ClassifyAndAnswerView(generics.GenericAPIView):
    """
    View для классификации вопроса и получения ответа.
    """

    def get(self, request, *args, **kwargs):
        question = request.GET.get('question')

        if not question:
            return Response({'error': 'Question parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        predicted_subject = agent.predict(question)

        subject = Subject.objects.filter(name=predicted_subject).first()

        if subject:
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            gemini_source = ExternalSource.objects.get(name="Gemini")
            answer = get_answer_from_gemini(question, gemini_source.api_url, gemini_source.api_key)

            if answer:
                return Response({'answer': answer['response']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)


class TrainModelView(generics.GenericAPIView):
    """
    View для обучения модели.
    """

    def post(self, request, *args, **kwargs):
        # Ожидаем данные для обучения
        questions = request.data.get('questions')
        labels = request.data.get('labels')

        if not questions or not labels:
            return Response({'error': 'Both questions and labels are required.'}, status=status.HTTP_400_BAD_REQUEST)

        agent.train(questions, labels)

        return Response({'message': 'Model trained successfully'}, status=status.HTTP_200_OK)


class SubjectListView(generics.ListCreateAPIView):
    """
    View для получения списка предметов и создания новых предметов.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View для получения, обновления или удаления конкретного предмета.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class AnswerCreateView(generics.CreateAPIView):
    """
    View для создания нового ответа на вопрос.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionListView(generics.ListCreateAPIView):
    """
    View для получения списка вопросов и создания новых вопросов.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View для получения, обновления или удаления конкретного вопроса.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class HybridSearchView(generics.GenericAPIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=400)

        gemini_result = search_gemini(query)
        wikipedia_result = search_wikipedia(query)

        combined_result = {
            'gemini': gemini_result,
            'wikipedia': wikipedia_result
        }

        SearchHistory.objects.create(
            user=request.user,
            query=query,
            response=combined_result
        )

        return Response(combined_result)


class RecommendationView(generics.GenericAPIView):
    def get(self, request):
        recommendations = generate_recommendations(request.user)
        return Response({'recommendations': recommendations})


class CalendarReminderView(generics.GenericAPIView):
    def post(self, request):
        summary = request.data.get('summary')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if not summary or not start_time or not end_time:
            return Response({'error': 'Missing required fields'}, status=400)

        event = create_calendar_event(summary, start_time, end_time)
        return Response({'event_id': event.get('id')})
