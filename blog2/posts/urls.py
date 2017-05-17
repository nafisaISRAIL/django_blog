from django.conf.urls import url
from blog2.posts import views


urlpatterns = [
    url(r'^$', views.MainPage.as_view(), name='main'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^contact/$', views.contact_page, name='contact'),
    url(r'^media/$', views.media_page, name='media'),
    url(r'^allcat/$', views.get_categories, name='cats'),
    url(r'^add_author/$', views.add_author, name='add-author'),
    url(r'^addpost/$', views.add_post, name='add_post'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetail.as_view(),
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/update/$', views.post_update,
        name='post-update'),
    url(r'^delete/(?P<id>\d+)/$', views.post_delete, name='post-delete'),
    url(r'^author/(?P<id>\d+)/$', views.about_author, name='about-author'),
    url(r'^author_edit/(?P<id>\d+)/$', views.author_update,
        name='author-update'),
    url(r'^post_with_formset/$', views.add_post_set,
        name='add-post-with-formset'),
    url(r'^posts_by_category/(?P<id>\d+)/$',
        views.get_post_by_category, name='get_post_by_category'),
    url(r'^user/(?P<id>\d+)/$', views.personal_page, name='personal_page'),
    url(r'^sended/$', views.sended, name='sended'),
    url(r'^addpost2/$', views.PostAddClassForm.as_view(), name='add_post2'),
    url(r'^class_posts/$', views.AuthorList.as_view()),

]
