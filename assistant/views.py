from rest_framework import generics, status
from rest_framework.response import Response
from .models import ExternalSource, Subject, Answer, Question
from .request_gemini import get_answer_from_gemini
from .agent import Agent
from .serializers import SubjectSerializer, QuestionSerializer, AnswerSerializer

# Инициализируем агента
agent = Agent()

class ClassifyAndAnswerView(generics.GenericAPIView):
    """
    View для классификации вопроса и получения ответа.
    """
    def get(self, request, *args, **kwargs):
        question = request.GET.get('question')

        # Проверка, что вопрос передан
        if not question:
            return Response({'error': 'Question parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Предполагаем, что модель уже обучена на примерах
        predicted_subject = agent.predict(question)

        # Проверяем, есть ли ответ в нашей базе
        subject = Subject.objects.filter(name=predicted_subject).first()

        if subject:
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Иначе ищем ответ через Gemini API
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

        # Обучаем модель на предоставленных данных
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


