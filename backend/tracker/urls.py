from django.urls import path
from . import views, forms

# Contents
# ========
# > TT Object Conversion Form Views
# > Create Update Delete Template Views
# > Detail Template Views
# > List Template Views


urlpatterns = [ 
    
# TT Object Conversion Form URLs
# ==============================

# Note:
# The following views use customized forms to track produce movement
# through the various stages of production. This includes keeping
# quantities and weights current amongst batches.

     path('forms/harvest_to_storage/', views.harvest_to_storage, name='tt_harvest_to_storage_form'),

     path('forms/storage_to_product/', views.storage_to_product, name='tt_storage_to_product_form'),
    
     path('forms/product_to_lab_sample/', views.product_to_lab_sample, name='tt_product_to_lab_sample_form'),

     path('forms/product_to_inventory/', views.product_to_inventory, name='tt_product_to_inventory_form'),

     path('forms/inventory_to_stop_item/', views.inventory_to_stop_item, name='tt_inventory_to_stop_item_form'),


# Create Update Delete Template URLs
# ==================================
    
    path('strain/create/', views.StrainCreate.as_view(), name='strain_create'),
    path('strain/<int:pk>/update/', views.StrainUpdate.as_view(), name='strain_update'),
    path('strain/<int:pk>/delete/', views.StrainDelete.as_view(), name='strain_delete'),

    path('tt_inventory/create/', views.TTInventoryCreate.as_view(), name='tt_inventory_create'),
    path('tt_inventory/<int:pk>/update/', views.TTInventoryUpdate.as_view(), name='tt_inventory_update'),
    path('tt_inventory/<int:pk>/delete/', views.TTInventoryDelete.as_view(), name='tt_inventory_delete'),

    path('tt_inventory_product/create/', views.TTInventoryProductCreate.as_view(), name='tt_inventory_product_create'),
    path('tt_inventory_product/<int:pk>/update/', views.TTInventoryProductUpdate.as_view(), name='tt_inventory_product_update'),
    path('tt_inventory_product/<int:pk>/delete/', views.TTInventoryProductDelete.as_view(), name='tt_inventory_product_delete'),

    path('tt_location/create/', views.TTLocationCreate.as_view(), name='tt_location_create'),
    path('tt_location/<int:pk>/update/', views.TTLocationUpdate.as_view(), name='tt_location_update'),
    path('tt_location/<int:pk>/delete/', views.TTLocationDelete.as_view(), name='tt_location_delete'),

    path('tt_plant_batch/create/', views.TTPlantBatchCreate.as_view(), name='tt_plant_batch_create'),
    path('tt_plant_batch/<int:pk>/update/', views.TTPlantBatchUpdate.as_view(), name='tt_plant_batch_update'),
    path('tt_plant_batch/<int:pk>/delete/', views.TTPlantBatchDelete.as_view(), name='tt_plant_batch_delete'),

    path('tt_plant_batch_harvest/create/', views.TTPlantBatchHarvestCreate.as_view(), name='tt_plant_batch_harvest_create'),
    path('tt_plant_batch_harvest/<int:pk>/update/', views.TTPlantBatchHarvestUpdate.as_view(), name='tt_plant_batch_harvest_update'),
    path('tt_plant_batch_harvest/<int:pk>/delete/', views.TTPlantBatchHarvestDelete.as_view(), name='_delete'),

    path('tt_storage_batch/create/', views.TTStorageBatchCreate.as_view(), name='tt_storage_batch_create'),
    path('tt_storage_batch/<int:pk>/update/', views.TTStorageBatchUpdate.as_view(), name='tt_storage_batch_update'),
    path('tt_storage_batch/<int:pk>/delete/', views.TTStorageBatchDelete.as_view(), name='tt_storage_batch_delete'),

    path('tt_product_batch/create/', views.TTProductBatchCreate.as_view(), name='tt_product_batch_create'),
    path('tt_product_batch/<int:pk>/update/', views.TTProductBatchUpdate.as_view(), name='tt_product_batch_update'),
    path('tt_product_batch/<int:pk>/delete/', views.TTProductBatchDelete.as_view(), name='tt_product_batch_delete'),

    path('tt_sublot/create/', views.TTSublotCreate.as_view(), name='tt_sublot_create'),
    path('tt_sublot/<int:pk>/update/', views.TTSublotUpdate.as_view(), name='tt_sublot_update'),
    path('tt_sublot/<int:pk>/delete/', views.TTSublotDelete.as_view(), name='tt_sublot_delete'),

    path('tt_lab_sample/create/', views.TTLabSampleCreate.as_view(), name='tt_lab_sample_create'),
    path('tt_lab_sample/<int:pk>/update/', views.TTLabSampleUpdate.as_view(), name='tt_lab_sample_update'),
    path('tt_lab_sample/<int:pk>/delete/', views.TTLabSampleDelete.as_view(), name='tt_lab_sample_delete'),

    path('plant/create/', views.PlantCreate.as_view(), name='plant_create'),
    path('plant/<int:pk>/update/', views.PlantUpdate.as_view(), name='plant_update'),
    path('plant/<int:pk>/delete/', views.PlantDelete.as_view(), name='plant_delete'),

    path('weight/create/', views.WeightCreate.as_view(), name='weight_create'),
    path('weight/<int:pk>/update/', views.WeightUpdate.as_view(), name='weight_update'),
    path('weight/<int:pk>/delete/', views.WeightDelete.as_view(), name='weight_delete'),

    path('derivative/create/', views.DerivativeCreate.as_view(), name='derivative_create'),
    path('derivative/<int:pk>/update/', views.DerivativeUpdate.as_view(), name='derivative_update'),
    path('derivative/<int:pk>/delete/', views.DerivativeDelete.as_view(), name='derivative_delete'),

    path('plant_harvest/create/', views.PlantHarvestCreate.as_view(), name='plant_harvest_create'),
    path('plant_harvest/<int:pk>/update/', views.PlantHarvestUpdate.as_view(), name='plant_harvest_update'),
    path('plant_harvest/<int:pk>/delete/', views.PlantHarvestDelete.as_view(), name='plant_harvest_delete'),

    path('lab_result/create/', views.LabResultCreate.as_view(), name='lab_result_create'),
    path('lab_result/<int:pk>/update/', views.LabResultUpdate.as_view(), name='lab_result_update'),
    path('lab_result/<int:pk>/delete/', views.LabResultDelete.as_view(), name='lab_result_delete'),

    path('lab_sample_result/create/', views.LabSampleResultCreate.as_view(), name='lab_sample_result_create'),
    path('lab_sample_result/<int:pk>/update/', views.LabSampleResultUpdate.as_view(), name='lab_sample_result_update'),
    path('lab_sample_result/<int:pk>/delete/', views.LabSampleResultDelete.as_view(), name='lab_sample_result_delete'),

    path('lab_sample/create/', views.LabSampleCreate.as_view(), name='lab_sample_create'),
    path('lab_sample/<int:pk>/update/', views.LabSampleUpdate.as_view(), name='lab_sample_update'),
    path('lab_sample/<int:pk>/delete/', views.LabSampleDelete.as_view(), name='lab_sample_delete'),

    path('inventory/create/', views.InventoryCreate.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/update/', views.InventoryUpdate.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.InventoryDelete.as_view(), name='inventory_delete'),

    path('inventory_room/create/', views.InventoryRoomCreate.as_view(), name='inventory_room_create'),
    path('inventory_room/<int:pk>/update/', views.InventoryRoomUpdate.as_view(), name='inventory_room_update'),
    path('inventory_room/<int:pk>/delete/', views.InventoryRoomDelete.as_view(), name='inventory_room_delete'),

    path('inventory_sublot/create/', views.InventorySublotCreate.as_view(), name='inventory_sublot_create'),
    path('inventory_sublot/<int:pk>/update/', views.InventorySublotUpdate.as_view(), name='inventory_sublot_update'),
    path('inventory_sublot/<int:pk>/delete/', views.InventorySublotDelete.as_view(), name='inventory_sublot_delete'),

    path('inventory_move/create/', views.InventoryMoveCreate.as_view(), name='inventory_move_create'),
    path('inventory_move/<int:pk>/update/', views.InventoryMoveUpdate.as_view(), name='inventory_move_update'),
    path('inventory_move/<int:pk>/delete/', views.InventoryMoveDelete.as_view(), name='inventory_move_delete'),

    path('plant_cure/create/', views.PlantCureCreate.as_view(), name='plant_cure_create'),
    path('plant_cure/<int:pk>/update/', views.PlantCureUpdate.as_view(), name='plant_cure_update'),
    path('plant_cure/<int:pk>/delete/', views.PlantCureDelete.as_view(), name='plant_cure_delete'),

    path('invoice_inventory/create/', views.InvoiceInventoryCreate.as_view(), name='invoice_inventory_create'),
    path('invoice_inventory/<int:pk>/update/', views.InvoiceInventoryUpdate.as_view(), name='invoice_inventory_update'),
    path('invoice_inventory/<int:pk>/delete/', views.InvoiceInventoryDelete.as_view(), name='invoice_inventory_delete'),

    path('invoice_model/create/', views.InvoiceModelCreate.as_view(), name='invoice_model_create'),
    path('invoice_model/<int:pk>/update/', views.InvoiceModelUpdate.as_view(), name='invoice_model_update'),
    path('invoice_model/<int:pk>/delete/', views.InvoiceModelDelete.as_view(), name='invoice_model_delete'),

    path('manifest_driver/create/', views.ManifestDriverCreate.as_view(), name='manifest_driver_create'),
    path('manifest_driver/<int:pk>/update/', views.ManifestDriverUpdate.as_view(), name='manifest_driver_update'),
    path('manifest_driver/<int:pk>/delete/', views.ManifestDriverDelete.as_view(), name='manifest_driver_delete'),

    path('stop_item/create/', views.StopItemCreate.as_view(), name='stop_item_create'),
    path('stop_item/<int:pk>/update/', views.StopItemUpdate.as_view(), name='stop_item_update'),
    path('stop_item/<int:pk>/delete/', views.StopItemDelete.as_view(), name='stop_item_delete'),

    path('manifest_stop/create/', views.ManifestStopCreate.as_view(), name='manifest_stop_create'),
    path('manifest_stop/<int:pk>/update/', views.ManifestStopUpdate.as_view(), name='manifest_stop_update'),
    path('manifest_stop/<int:pk>/delete/', views.ManifestStopDelete.as_view(), name='manifest_stop_delete'),

    path('manifest_vehicle/create/', views.ManifestVehicleCreate.as_view(), name='manifest_vehicle_create'),
    path('manifest_vehicle/<int:pk>/update/', views.ManifestVehicleUpdate.as_view(), name='manifest_vehicle_update'),
    path('manifest_vehicle/<int:pk>/delete/', views.ManifestVehicleDelete.as_view(), name='manifest_vehicle_delete'),

    path('manifest_thirdpartytransporter/create/', views.ManifestThirdPartyTransporterCreate.as_view(), name='manifest_thirdpartytransporter_create'),
    path('manifest_thirdpartytransporter/<int:pk>/update/', views.ManifestThirdPartyTransporterUpdate.as_view(), name='manifest_thirdpartytransporter_update'),
    path('manifest_thirdpartytransporter/<int:pk>/delete/', views.ManifestThirdPartyTransporterDelete.as_view(), name='manifest_thirdpartytransporter_delete'),

    path('manifest/create/', views.ManifestCreate.as_view(), name='manifest_create'),
    path('manifest/<int:pk>/update/', views.ManifestUpdate.as_view(), name='manifest_update'),
    path('manifest/<int:pk>/delete/', views.ManifestDelete.as_view(), name='manifest_delete'),

    path('grow_room/create/', views.GrowRoomCreate.as_view(), name='grow_room_create'),
    path('grow_room/<int:pk>/update/', views.GrowRoomUpdate.as_view(), name='grow_room_update'),
    path('grow_room/<int:pk>/delete/', views.GrowRoomDelete.as_view(), name='grow_room_delete'),




# Detail Template URLS
# ====================    
    path('strain/<str:pk>',
         views.StrainDetailView.as_view(), name='strain_detail'),
    path('tt_inventory_product/<str:pk>',
         views.TTInventoryProductDetailView.as_view(), name='tt_inventory_product_detail'),
     path('tt_inventory/<str:pk>',
         views.TTInventoryDetailView.as_view(), name='tt_inventory_detail'),
    path('tt_location/<str:pk>',
         views.TTLocationDetailView.as_view(), name='tt_location_detail'),
    path('tt_plant_batch/<str:pk>',
        views.TTPlantBatchDetailView.as_view(), name='tt_plant_batch_detail'),
    path('tt_plant_batch_harvest/<str:pk>',
         views.TTPlantBatchHarvestDetailView.as_view(), name='tt_plant_batch_harvest_detail'),
    path('tt_product_batch/<str:pk>',
         views.TTProductBatchDetailView.as_view(), name='tt_product_batch_detail'),
    path('tt_storage_batch/<str:pk>',
         views.TTStorageBatchDetailView.as_view(), name='tt_storage_batch_detail'),
    path('tt_sublot/<str:pk>',
         views.TTSublotDetailView.as_view(), name='tt_sublot_detail'),
    path('tt_lab_sample/<str:pk>',
         views.TTLabSampleDetailView.as_view(), name='tt_lab_sample_detail'),
    path('plant/<str:pk>',
         views.PlantDetailView.as_view(), name='plant_detail'),
    path('weight/<str:pk>',
         views.WeightDetailView.as_view(), name='weight_detail'),
    path('derivative/<str:pk>',
         views.DerivativeDetailView.as_view(), name='derivative_detail'),
    path('plant_harvest/<str:pk>',
         views.PlantHarvestDetailView.as_view(), name='plant_harvest_detail'),
    path('lab_result/<str:pk>',
         views.LabResultDetailView.as_view(), name='lab_result_detail'),
    path('lab_sample_result/<str:pk>',
         views.LabSampleResultDetailView.as_view(), name='lab_sample_result_detail'),
    path('lab_sample/<str:pk>',
         views.LabSampleDetailView.as_view(), name='lab_sample_detail'),
    path('inventory/<str:pk>',
         views.InventoryDetailView.as_view(), name='inventory_detail'),
    path('inventory_room/<str:pk>',
         views.InventoryRoomDetailView.as_view(), name='inventory_room_detail'),
    path('inventory_sublot/<str:pk>',
         views.InventorySublotDetailView.as_view(), name='inventory_sublot_detail'),
    path('inventory_move/<str:pk>',
         views.InventoryMoveDetailView.as_view(), name='inventory_move_detail'),
    path('plant_cure/<str:pk>',
         views.PlantCureDetailView.as_view(), name='plant_cure_detail'),
    path('invoice_inventory/<str:pk>',
         views.InvoiceInventoryDetailView.as_view(), name='invoice_inventory_detail'),
    path('invoice_model/<str:pk>',
         views.InvoiceModelDetailView.as_view(), name='invoice_model_detail'),
    path('manifest_driver/<str:pk>',
         views.ManifestDriverDetailView.as_view(), name='manifest_driver_detail'),
    path('stop_item/<str:pk>',
         views.StopItemDetailView.as_view(), name='stop_item_detail'),
    path('manifest_stop/<str:pk>',
         views.ManifestStopDetailView.as_view(), name='manifest_stop_detail'),
    path('manifest_vehicle/<str:pk>',
         views.ManifestVehicleDetailView.as_view(), name='manifest_vehicle_detail'),
    path('manifest_thirdpartytransporter/<str:pk>',
         views.ManifestThirdPartyTransporterDetailView.as_view(), name='manifest_thirdpartytransporter_detail'),
    path('manifest/<str:pk>',
         views.ManifestDetailView.as_view(), name='manifest_detail'),
    path('grow_room/<str:pk>',
         views.GrowRoomDetailView.as_view(), name='grow_room_detail'),

    path('tt_storage_batch/create/',  
          views.TTStorageBatchCreateView.as_view(), name='tt_storage_batch_form'),

# List Template URLs
# ===================
    path('', views.BookListView.as_view(), name='book_list'),
    path('', views.PlantListView.as_view(), name='plant_list'),


]