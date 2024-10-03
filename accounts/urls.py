from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-budget/', views.create_budget, name='create_budget'),
    path('budget/<int:budget_id>/', views.budget_detail, name='budget_detail'),
    path('budget/<int:budget_id>/update/', views.budget_update, name='budget_update'),
    path('budget/<int:budget_id>/delete/', views.budget_delete, name='budget_delete'),
    path('budget/<int:budget_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('transaction/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transaction/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('budget/<int:budget_id>/analytics/', views.budget_analytics, name='budget_analytics'),
]