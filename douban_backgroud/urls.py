from django.contrib import admin
from django.urls import path, include
from bookInfo.views import ScoreView, SearchView, StarView, TimeView, PesgView, WrodcloudView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('score/', ScoreView.as_view()),
    path('star/', StarView.as_view()),
    path('time/', TimeView.as_view()),
    path('pesg/', PesgView.as_view()),
    path('wordcloud/', WrodcloudView.as_view()),
    path('search/', SearchView.as_view()),

    # path('score/', include('bookInfo.urls'))
]
