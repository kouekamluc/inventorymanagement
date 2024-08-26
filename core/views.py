from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.db.models import Sum, Avg
from inventory.models import InventoryItem
from datetime import timedelta
from django.utils import timezone


class HomeView(TemplateView):
    template_name = 'core/home.html'




class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Inventory summary
        context['total_items'] = InventoryItem.objects.count()
        context['low_stock_items'] = InventoryItem.objects.filter(quantity__lt=10).count()
        context['out_of_stock_items'] = InventoryItem.objects.filter(quantity=0).count()
        
        # Sales summary (placeholder data - replace with actual logic when you have a sales model)
        context['total_sales'] = 10000.00  # Replace with actual total sales
        context['today_sales'] = 500.00  # Replace with actual today's sales
        context['pending_orders'] = 5  # Replace with actual pending orders count
        
        # Recent orders (placeholder data - replace with actual logic when you have an order model)
        context['recent_orders'] = [
            {'id': 1, 'date': timezone.now(), 'total': 100.00},
            {'id': 2, 'date': timezone.now() - timedelta(days=1), 'total': 150.00},
            {'id': 3, 'date': timezone.now() - timedelta(days=2), 'total': 200.00},
        ]
        
        return context