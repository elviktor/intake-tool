from django.urls import path
from .views import BookListView, PlantListView, StrainDetailView, TTInventoryDetailView, TTLocationDetailView, TTPlantBatchDetailView, TTPlantBatchHarvestDetailView, TTProductBatchDetailView, TTSublotDetailView 

urlpatterns = [ 
    path('', BookListView.as_view(), name='book_list'),
    path('', PlantListView.as_view(), name='plant_list'),
    path('strain/<int:pk>',
         StrainDetailView.as_view(), name='strain_detail'),
    path('tt_inventory/<int:pk>',
         TTInventoryDetailView.as_view(), name='tt_inventory_detail'),
    path('tt_location/<int:pk>',
         TTLocationDetailView.as_view(), name='tt_location_detail'),
    path('tt_plant_batch/<int:pk>',
         TTPlantBatchDetailView.as_view(), name='tt_plant_batch_detail'),
    path('tt_plant_batch_harvest/<int:pk>',
         TTPlantBatchHarvestDetailView.as_view(), name='tt_plant_batch_harvest_detail'),
    path('tt_product_batch/<int:pk>',
         TTProductBatchDetailView.as_view(), name='tt_product_batch_detail'),
    path('tt_sublot/<int:pk>',
         TTSublotDetailView.as_view(), name='tt_sublot_detail'),

]