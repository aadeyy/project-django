from django.db import models

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.category})"