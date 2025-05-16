from django.db import models
import os
from django.conf import settings

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/', null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):    # 원래 사진에서 다른 사진으로 바뀌면 원래 사진은 삭제 되어야됨.
        if self.pk:
            try:
                old = Blog.objects.get(pk=self.pk)  # 일단 원래꺼 가져옴
                if old.image and old.image != self.image:   # 원래 사진이 선택한 사진과 다르면 원래 사진 삭제
                    if os.path.isfile(old.image.path):
                        os.remove(old.image.path)
            except Blog.DoesNotExist:
                pass
        super().save(*args, **kwargs)    # 저장
    
    def delete(self, *args, **kwargs):  # 실제 글을 삭제하는 부분임.
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)  # 사진도 실제로 같이 삭제가 되어야됨.
        super().delete(*args, **kwargs)