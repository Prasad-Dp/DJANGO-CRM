from django.urls import path
from . import views
app_name="leads"
urlpatterns=[
    path('',views.leads_list_view.as_view(),name="lead-list"),
    path('<int:pk>/',views.leads_detail_view.as_view(),name="lead-view"),
    path('<int:pk>/update/',views.lead_update_view.as_view(),name="lead-update"),
    path('<int:pk>/delete/',views.lead_delete_view.as_view(),name="lead-delete"),
    path('create/',views.leads_create_view.as_view(),name="lead-create"),
    path('category/',views.CategoryListView.as_view(),name="category-list"),
    path('category/<int:pk>/',views.categoryDetailView.as_view(),name='category-detail'),
    
]