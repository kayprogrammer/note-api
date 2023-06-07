from django.db import models
from apps.common.models import BaseModel
from apps.accounts.models import User # or from django.contrib.auth import get_user_model ... User = get_user_model()

class Note(BaseModel):
    user = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    text = models.TextField()
    pinned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']
