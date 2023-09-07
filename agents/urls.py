from django.urls import path
from .views import agent_list_view,agent_create_view,agent_detail_view,agent_update_view,agent_delete_view
app_name="agents"

urlpatterns=[
    path('',agent_list_view.as_view(),name="agents-list"),
    path('<int:pk>/',agent_detail_view.as_view(),name="agent-view"),
    path('<int:pk>/update',agent_update_view.as_view(),name="agent-update"),
    path('<int:pk>/delete',agent_delete_view.as_view(),name="agent-delete"),
    path('create',agent_create_view.as_view(),name="agent-create"),


]