
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import InventoryItem
from django.db.models import Q 
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404


class InventoryListView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        category = self.request.GET.get('category')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('-last_updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['categories'] = InventoryItem.objects.values_list('category', flat=True).distinct()
        return context




class InventoryDetailView(LoginRequiredMixin, DetailView):
    model = InventoryItem
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'item'

class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    fields = ['name', 'description', 'quantity', 'unit_price', 'category']
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        form.instance.managed_by = self.request.user
        messages.success(self.request, 'Inventory item created successfully.')
        return super().form_valid(form)
    
    
class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    fields = ['name', 'description', 'quantity', 'unit_price', 'category']
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        messages.success(self.request, 'Inventory item updated successfully.')
        return super().form_valid(form)

class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Inventory item deleted successfully.')
        return super().delete(request, *args, **kwargs)



class InventoryAdjustmentView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    template_name = 'inventory/inventory_adjustment.html'
    fields = ['quantity']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')
        amount = int(request.POST.get('amount', 0))
        
        if action == 'add':
            self.object.quantity += amount
            messages.success(request, f'Added {amount} to {self.object.name}.')
        elif action == 'remove':
            if self.object.quantity >= amount:
                self.object.quantity -= amount
                messages.success(request, f'Removed {amount} from {self.object.name}.')
            else:
                messages.error(request, f'Not enough {self.object.name} in inventory.')
        
        self.object.save()
        return redirect('inventory_list')