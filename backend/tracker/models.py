from django.urls import reverse
from django.db import models
import uuid
from accounts.models import CustomUser
from django.utils.crypto import get_random_string

class Book(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('book_detail', args=[str(self.id)])

    def __str__(self):
        return self.title


# Contents
# ========
# > Notes
# > Bio Track (Original) API Models
# > TT Models (Converted)
# > Delete Models
    
# Notes
# ======

# Required 'base' model fields - essential functions
# ------------------------------
# All Base models need to contain the following fields
# in the following order:
# uid, user, deleted
    
# Required 'base' model fields - location tracking
# ------------------------------
# All Base models tracking location need to contain the following fields
# in the following order:      (ex. TT_Plant_Batch)
# location, sublot, from_row, to_row
    
# Required 'base' model fields - amount tracking
# ------------------------------
# All Base models tracking amount need to contain the following fields
# in the following order:      (ex. TT_Product_Batch)
# total_quantity, total_weight, remaining_quantity, remaining_weight


# ======================
# Bio Track API (original) Models
# ======================
# The following are models based off of the Bio Track API
# Note about conversion of Biotrack models:
# Because Django reserves "id" when I encounter "id" in Biotrack
# I add a "biotrack_" prefix.   id   >>>   biotrack_id

class Strain(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=250, null=True, blank=True)
    shortname = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    coa_link = models.CharField(max_length=250, null=True, blank=True)
    thc_amt = models.FloatField(null=True, blank=True)
    cbd_amt = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('strain_detail', args=[str(self.uid)])

    def __str__(self):
        return self.name


class Plant(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    converted = models.BooleanField(default=False)
    destroy_reason = models.CharField(max_length=250, null=True, blank=True)
    destroy_reason_id = models.IntegerField(null=True, blank=True)
    destroy_scheduled = models.BooleanField(default=False)
    destroy_scheduled_time = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_scheduled = models.BooleanField(default=False)
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #BiotrackAPI key = 'id'
    location = models.CharField(max_length=250, null=True, blank=True)
    mother = models.BooleanField(default=False)
    org_id = models.IntegerField(null=True, blank=True)
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular plant instance."""
        return reverse('plant_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.biotrack_id


class Weight(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    amount = models.FloatField(null=True, blank=True)
    uom = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.strain

class Derivative(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    accounted_for = models.IntegerField(null=True, blank=True)
    additional_collections = models.BooleanField(default=False)
    cure_collections = models.BooleanField(default=False)
    harvest_collections = models.BooleanField(default=False)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    plant_id = models.CharField(max_length=250, null=True, blank=True)
    room = models.IntegerField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    whole_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.biotrack_id)


class Plant_Harvest(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    derivative = models.ForeignKey(Derivative, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.harvest_id


class Lab_Result(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=250, null=True, blank=True)
    sample_id = models.IntegerField(null=True, blank=True)
    failure = models.BooleanField(default=False)
    test = models.IntegerField(null=True, blank=True)
    uom = models.CharField(max_length=250, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.sample_id)


class Lab_Sample_Result(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    sample_name = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    lab_provided = models.BooleanField(default=False)
    sample_id = models.IntegerField(null=True, blank=True)
    test_id = models.IntegerField(null=True, blank=True)
    test_panel = models.CharField(max_length=250, null=True, blank=True)
    test_pass = models.BooleanField(default=False)
    test_value = models.FloatField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.sample_name)


class Lab_Sample(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    amount = models.FloatField(null=True, blank=True)
    amount_used = models.FloatField(null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    inventory_type = models.IntegerField(null=True, blank=True)
    lab_license = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    medical_grade = models.BooleanField(default=False)
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    result = models.CharField(max_length=250, null=True, blank=True)
    results = models.ForeignKey(Lab_Result, on_delete=models.CASCADE)
    rn_d = models.BooleanField(default=False)
    sample_use = models.CharField(max_length=250, null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    test_results = models.ForeignKey(Lab_Sample_Result, on_delete=models.CASCADE)
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.biotrack_id)

class Inventory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    inventory_name = models.CharField(max_length=250, null=True, blank=True)
    current_room = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #BiotrackAPI key = 'id'
    id_serial = models.IntegerField(null=True, blank=True)
    inventory_type = models.IntegerField(null=True, blank=True)
    lab_sample = models.ForeignKey(Lab_Sample, on_delete=models.CASCADE)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    med_usable_weight = models.FloatField(null=True, blank=True)
    medicated = models.BooleanField(default=False)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    qa_status = models.CharField(max_length=250, null=True, blank=True)
    rec_usable_weight = models.FloatField(null=True, blank=True)
    remaining_amount = models.FloatField(null=True, blank=True)
    seized = models.BooleanField(default=False)
    session_time = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    unit_based = models.BooleanField(default=False)
    usable_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.inventory_name


class Inventory_Room(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    location_license = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    quarantine = models.BooleanField(default=False)
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Inventory_Sublot(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    sublot_name = models.CharField(max_length=250, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    uom = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.sublot_name


class Inventory_Move(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    inventory_ids = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    new_room_id = models.IntegerField(null=True, blank=True)


class Plant_Cure(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    cure_id = models.CharField(max_length=250, null=True, blank=True)
    derivative = models.ForeignKey(Derivative, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.cure_id

# Inventory moved down to TT section

class Grow_Room(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    location_license = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    updated_on = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
    

# Trichomes Tracker App Models::
# The following section of models (with TT_ prefix) are based on the initial DB
# designed for the Trichomes Tracker App.

class TT_Location(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=250, null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    location_license = models.CharField(max_length=250, null=True, blank=True)
    quarantine = models.BooleanField(default=False)
    transaction_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_location_detail', args=[str(self.uid)])

    def __str__(self):
        return self.name


class TT_Sublot(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    sublot_name = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    uom = models.CharField(max_length=250, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_sublot_detail', args=[str(self.uid)])

    def __str__(self):
        return self.sublot_name


class TT_Plant_Batch(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    strain = models.ForeignKey(Strain, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True) #Use qty to bulk_create() Biotrack plant models
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    sublot = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    from_row = models.IntegerField(null=True, blank=True)
    to_row = models.IntegerField(null=True, blank=True)
    mother = models.BooleanField(default=False)
    org_id = models.IntegerField(null=True, blank=True)
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)
    converted = models.BooleanField(default=False)
    destroy_reason = models.CharField(max_length=250, null=True, blank=True)
    destroy_reason_id = models.IntegerField(null=True, blank=True)
    destroy_scheduled = models.BooleanField(default=False)
    destroy_scheduled_time = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_scheduled = models.BooleanField(default=False)
    session_time = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular plant instance."""
        return reverse('tt_plant_batch_detail', args=[str(self.uid)])
    
    def __str__(self):
        return f'{self.strain} {self.uid}'


class TT_Plant_Batch_Harvest(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    plant_batch = models.ForeignKey(TT_Plant_Batch, on_delete=models.CASCADE)
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    sublot = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    from_row = models.IntegerField(null=True, blank=True)
    to_row = models.IntegerField(null=True, blank=True)
    harvest_stage = models.CharField(max_length=250, null=True, blank=True)
    harvest_completed = models.BooleanField(default=False)
    harvest_start_date = models.DateField(null=True, blank=True)
    harvest_finish_date = models.DateField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    transaction_id = models.IntegerField(null=True, blank=True)
    total_wet_weight = models.FloatField(null=True, blank=True)
    total_dry_weight = models.FloatField(null=True, blank=True)
    # The following "remaining weights" are key for tracking product amounts
    # It is what can be submitted to OCM. They interact with the following models:
    # TT_Product_Batch, 
    remaining_wet_weight = models.FloatField(null=True, blank=True) 
    remaining_dry_weight = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_plant_batch_harvest_detail', args=[str(self.uid)])

    def __str__(self):
        return f'{self.plant_batch.strain} {self.uid}'


class TT_Storage_Batch(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    harvest_batch = models.ForeignKey(TT_Plant_Batch_Harvest, on_delete=models.CASCADE)
    package_number = models.IntegerField(null=True, blank=True)
    location_date = models.DateField(null=True, blank=True)
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    sublot = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    from_row = models.IntegerField(null=True, blank=True)
    to_row = models.IntegerField(null=True, blank=True)
    # Select if product uses WET (fresh frozen) or DRY (flower) cannabis
    wet_dry = models.CharField(max_length=3, null=True, blank=True)
    produce_category = models.CharField(max_length=250, null=True, blank=True)
    # Update cannabis amounts still on hand. 
    # If TT_Storage_Batch.wet_dry = "wet":
    #     TT_Plant_Batch_Harvest.remaining_wet_weight = TT_Plant_Batch_Harvest.remaining_wet_weight - TT_Storage_Batch.weight
    # If TT_Storage_Batch.wet_dry = "dry":
    #     TT_Plant_Batch_Harvest.remaining_dry_weight = TT_Plant_Batch_Harvest.remaining_dry_weight - TT_Storage_Batch.weight
    weight = models.FloatField(null=True, blank=True)
    # Status examples: in storage, sent to processor, converted to product batch, destroyed
    status = models.CharField(max_length=250, null=True, blank=True)
    converted = models.BooleanField(default=False)
    destroy_reason = models.CharField(max_length=250, null=True, blank=True)
    destroy_reason_id = models.IntegerField(null=True, blank=True)
    destroy_scheduled = models.BooleanField(default=False)
    destroy_scheduled_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_storage_batch_detail', args=[str(self.uid)])

    def __str__(self):
        return f'{self.harvest_batch} {self.wet_dry} {str(self.package_number)}'


class TT_Product_Batch(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    product_category = models.CharField(max_length=250, null=True, blank=True)
    harvest_batch = models.ForeignKey(TT_Plant_Batch_Harvest, on_delete=models.CASCADE)
    storage_batches = models.ForeignKey(TT_Storage_Batch, on_delete=models.CASCADE)
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    sublot = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    from_row = models.IntegerField(null=True, blank=True)
    to_row = models.IntegerField(null=True, blank=True)
    # uom (Unit of Measurement) & total_quantity & total_weight will help link important info to model that can (1) inform inventory of the total_quantity & total_weight of incoming product units; (2) Lab_sample weights can subtract from this when created to keep amounts current.
    uom = models.CharField(max_length=250, null=True, blank=True)
    total_quantity = models.IntegerField(null=True, blank=True)
    # Add weights of selected storage_batches to get this
    total_weight = models.FloatField(null=True, blank=True)
    remaining_quantity = models.IntegerField(null=True, blank=True)
    remaining_weight = models.FloatField(null=True, blank=True)
    available = models.BooleanField(default=False)
    # Select if product uses WET (fresh frozen) or DRY (flower) cannabis
    wet_dry = models.CharField(max_length=3, null=True, blank=True)
    packaging = models.CharField(max_length=250, null=True, blank=True)
    wholesale_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    msrp = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    moq = models.IntegerField(null=True, blank=True)
    thc_percent = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    terp_percent = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2) 
    thc_mg = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=3)
    thc_mg_per_serving = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    grow_type = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sell_points = models.TextField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    use_by_date = models.DateField(null=True, blank=True)
    sku = models.CharField(max_length=250, null=True, blank=True)
    coa = models.URLField(null=True, blank=True)
    tested = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
           

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_product_batch_detail', args=[str(self.uid)])

    def __str__(self):
        return f'{self.product_name} {self.uid}'

class TT_Inventory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    inventory_name = models.CharField(max_length=250, null=True, blank=True)
    inventory_type = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    sublot = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    from_row = models.IntegerField(null=True, blank=True)
    to_row = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #BiotrackAPI key = 'id'
    id_serial = models.IntegerField(null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_inventory_detail', args=[str(self.uid)])

    def __str__(self):
        return f'{self.inventory_name}'

class TT_Inventory_Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    inventory = models.ForeignKey(TT_Inventory, on_delete=models.CASCADE)
    product_batch = models.ForeignKey(TT_Product_Batch, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    qa_status = models.CharField(max_length=250, null=True, blank=True)
    total_quantity = models.IntegerField(null=True, blank=True)
    remaining_quantity = models.IntegerField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    remaining_amount = models.FloatField(null=True, blank=True)
    unit_based = models.BooleanField(default=False)
    usable_weight = models.FloatField(null=True, blank=True)
    rec_usable_weight = models.FloatField(null=True, blank=True)
    med_usable_weight = models.FloatField(null=True, blank=True)
    medicated = models.BooleanField(default=False)
    seized = models.BooleanField(default=False)
    session_time = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_inventory_product_detail', args=[str(self.uid)])

    def __str__(self):
        return f'{self.product_name} in {self.inventory.inventory_name}'


# I can use the same approach as for adding
# Product batches to TT_Inventory::
# TT_Inventory.amount = TT_Inventory.amount - Invoice_Inventory.amount
class Invoice_Model(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    invoice_name = models.CharField(max_length=250, null=True, blank=True)
    inventory = models.ForeignKey(TT_Inventory, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    buyer_location_license = models.CharField(max_length=250, null=True, blank=True)
    invoice_id = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    refund_invoice_id = models.CharField(max_length=250, null=True, blank=True)
    refunded = models.BooleanField(default=False)
    session_time = models.IntegerField(null=True, blank=True) 
    transaction_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True) 

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('invoice_model_detail', args=[str(self.uid)])

    def __str__(self):
        return self.invoice_name

# This name comes from Bio Track API
# I would call this model Invoice_Item
class Invoice_Inventory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    invoice_model = models.ForeignKey(Invoice_Model, on_delete=models.CASCADE)
    inventory_product = models.ForeignKey(TT_Inventory_Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True) # Quantity
    price = models.FloatField(null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    invoice_id = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True) 
    uom = models.CharField(max_length=250, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
      
    def __str__(self):
        return self.inventory_product


class TT_Lab_Sample(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    sample_name = models.CharField(max_length=250, null=True, blank=True)
    product_batch = models.ForeignKey(TT_Product_Batch, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    location = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    sublot = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    from_row = models.IntegerField(null=True, blank=True)
    to_row = models.IntegerField(null=True, blank=True)
    # To update cannabis amounts/weight::
    # TT_Product_Batch.total_weight = TT_Product_Batch.total_weight - TT_Lab_Sample.amount
    amount = models.FloatField(null=True, blank=True) # 'amount' = 'weight'
    amount_used = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    inventory_type = models.IntegerField(null=True, blank=True)
    lab_license = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    medical_grade = models.BooleanField(default=False)
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    result = models.CharField(max_length=250, null=True, blank=True)
    results = models.ForeignKey(Lab_Result, on_delete=models.CASCADE)
    rn_d = models.BooleanField(default=False)
    sample_use = models.CharField(max_length=250, null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    test_results = models.ForeignKey(Lab_Sample_Result, on_delete=models.CASCADE)
    transaction_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_lab_sample_detail', args=[str(self.uid)])

    def __str__(self):
        return f'{self.sample_name} {self.uid}'


class Manifest_Driver(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    dateof_birth = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Stop_Item(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    inventory_product = models.ForeignKey(TT_Inventory_Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    manifest_id = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    quantity_received = models.FloatField(null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    stop_number = models.IntegerField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    # TT_Product_Batch.total_weight = TT_Product_Batch.total_weight - Stop_Item.weight
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.manifest_id


class Manifest_Stop(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    approximate_arrival = models.CharField(max_length=250, null=True, blank=True)
    approximate_departure = models.CharField(max_length=250, null=True, blank=True)
    approximate_route = models.CharField(max_length=250, null=True, blank=True)
    driver_arrived = models.BooleanField(default=False)
    driver_arrived_time = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    invoice = models.ForeignKey(Invoice_Model, on_delete=models.CASCADE)
    biotrack_invoice_id = models.CharField(max_length=250, null=True, blank=True) #Original BiotrackAPI key = 'invoice_id'
    items = models.ManyToManyField(Stop_Item)
    items_count = models.IntegerField(null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    manifest_id = models.CharField(max_length=250, null=True, blank=True)
    stop_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.manifest_id


class Manifest_Vehicle(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #Original BiotrackAPI key = 'id'
    vehicle_name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.vehicle_name


class Manifest_ThirdPartyTransporter(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    license_number = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Manifest(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    city = models.CharField(max_length=250, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completion_date = models.CharField(max_length=250, null=True, blank=True)
    created_on = models.CharField(max_length=250, null=True, blank=True)
    driver_arrived = models.BooleanField(default=False)
    drivers = models.ForeignKey(Manifest_Driver, on_delete=models.CASCADE)
    in_transit = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_parked = models.BooleanField(default=False)
    license_number = models.CharField(max_length=250, null=True, blank=True)
    manifest_id = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    received = models.BooleanField(default=False)
    session_time = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    stop_count = models.IntegerField(null=True, blank=True)
    stops = models.ManyToManyField(Manifest_Stop)
    street = models.CharField(max_length=250, null=True, blank=True)
    third_party_transporter = models.ForeignKey(Manifest_ThirdPartyTransporter, on_delete=models.CASCADE)
    total_item_count = models.IntegerField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    updated_on = models.CharField(max_length=250, null=True, blank=True)
    vehicle = models.ForeignKey(Manifest_Vehicle, on_delete=models.CASCADE)
    zip = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.manifest_id
    

    # Delete Tracking Models
    # ======================

class TT_Location_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Location, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_location_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'


class TT_Sublot_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Sublot, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_sublot_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'


class Strain_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(Strain, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('strain_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class TT_Plant_Batch_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Plant_Batch, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_plant_batch_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class TT_Plant_Batch_Harvest_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Plant_Batch_Harvest, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_plant_batch_harvest_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}' 
    

class TT_Storage_Batch_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Storage_Batch, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_storage_batch_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'


class TT_Product_Batch_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Product_Batch, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_product_batch_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class Lab_Result_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(Lab_Result, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('lab_result_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class Lab_Sample_Result_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(Lab_Sample_Result, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('lab_sample_result_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class TT_Lab_Sample_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Lab_Sample, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_lab_sample_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'


class TT_Inventory_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Inventory, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_sublot_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class TT_Inventory_Product_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(TT_Inventory_Product, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('tt_inventory_product_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class Invoice_Model_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(Invoice_Model, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('invoice_model_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'
    

class Invoice_Inventory_Delete(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delete_time = models.DateTimeField(auto_now_add=True)
    deleted_item = models.ForeignKey(Invoice_Inventory, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('invoice_inventory_delete_detail', args=[str(self.uid)])

    def __str__(self):
        return f'Delete Record - {self.deleted_item} {self.uid}'