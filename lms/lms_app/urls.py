from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),                     
    path('index/', views.index, name='index'),        
    path('signup/', views.signup_view, name='signup'),      # Signup page
    path('login/', views.login_view, name='login'),         # Login page
    path('logout/', views.logout_view, name='logout'),      # Logout page
    path('books/', views.books, name='books'),              # Books page
    path('update/<int:id>/', views.update, name='update'),  # Update book
    path('delete/<int:id>/', views.delete, name='delete'),  # Delete book
    
]
