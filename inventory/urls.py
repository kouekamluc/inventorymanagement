from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='inventory_list'),
    path('<int:pk>/', views.InventoryDetailView.as_view(), name='inventory_detail'),
    path('new/', views.InventoryCreateView.as_view(), name='inventory_create'),
    path('<int:pk>/edit/', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='inventory_delete'),
    path('<int:pk>/adjust/', views.InventoryAdjustmentView.as_view(), name='inventory_adjustment'),

]