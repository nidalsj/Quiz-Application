from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class Quiz(models.Model):
    candidate_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.candidate_name}'s Quiz - {self.category} - {self.difficulty}"
    
