from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create/', views.CreateApplicationView.as_view(), name='create_application'),
    path('review/<int:app_id>/', views.CreateReviewView.as_view(), name='create_review'),
    path('myadmin/', views.AdminPanelView.as_view(), name='admin_panel'),
    path('myadmin/<int:app_id>/', views.AdminPanelView.as_view(), name='admin_update'),
    path('er/', views.ERDiagramView.as_view(), name='er_diagram'),
]