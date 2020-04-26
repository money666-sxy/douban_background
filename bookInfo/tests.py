from django.test import TestCase
from bookInfo.models import Bookcomment, Bookinfo
# Create your tests here.
book = Bookinfo.objects.get(sid=1007305)
print(book.score)
