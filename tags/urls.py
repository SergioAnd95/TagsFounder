from .views import TagListCreateView, TagsSearchView


urlpatterns = [
    (TagListCreateView, '/tags'),
    (TagsSearchView, '/tags_find'),
]
