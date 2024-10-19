from django.contrib.auth import get_user_model
from django.db import models


# Эта таблица будет хранить данные о различных предметах
# (например, математика, биология, физика).

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Каждый предмет имеет несколько тем.
# Эта таблица будет хранить информацию о конкретных темах по каждому предмету.

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Эта таблица будет хранить вопросы,
# заданные пользователями, вместе с результатами их классификации (связанными предметами и темами).

class Question(models.Model):
    text = models.TextField()
    classified_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    classified_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


# Эта таблица будет хранить ответы на вопросы,
# сгенерированные системой или полученные из внешних источников.

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to: {self.question.text[:50]}"


# Эта таблица будет хранить информацию о внешних источниках данных,
# которые могут быть использованы для получения ответов (например, API Wolfram Alpha или Google Scholar).

class ExternalSource(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.URLField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Эта таблица будет хранить логи работы агентов — для отслеживания,
# какие вопросы обрабатываются, какими агентами и как они классифицируются

class AgentLog(models.Model):
    agent_name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Log for: {self.agent_name} on {self.question.text[:50]}'


class SearchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"


class Recommendation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recommended_queries = models.TextField()

    def __str__(self):
        return f"Recommendations for {self.user.username}"


