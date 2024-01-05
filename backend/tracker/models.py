from django.urls import reverse
from django.db import models
import uuid

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


# Note about conversion of Biotrack models:
# Because Django reserves "id" when I encounter "id" in Biotrack
# I add a "biotrack_" prefix.   id   >>>   biotrack_id

class Strain(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, null=True, blank=True)
    shortname = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    coa_link = models.CharField(max_length=250, null=True, blank=True)
    thc_amt = models.FloatField(null=True, blank=True)
    cbd_amt = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Plant(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    converted = models.BooleanField()
    deleted = models.BooleanField()
    destroy_reason = models.CharField(max_length=250, null=True, blank=True)
    destroy_reason_id = models.IntegerField(null=True, blank=True)
    destroy_scheduled = models.BooleanField()
    destroy_scheduled_time = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_scheduled = models.BooleanField()
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #BiotrackAPI key = 'id'
    location = models.CharField(max_length=250, null=True, blank=True)
    mother = models.BooleanField()
    org_id = models.IntegerField(null=True, blank=True)
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular plant instance."""
        return reverse('plant_detail', args=[str(self.biotrack_id)])
    
    def __str__(self):
        return self.biotrack_id


class Weight(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(null=True, blank=True)
    uom = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.strain

class Derivative(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accounted_for = models.IntegerField(null=True, blank=True)
    additional_collections = models.BooleanField()
    cure_collections = models.BooleanField()
    deleted = models.IntegerField(null=True, blank=True)
    harvest_collections = models.BooleanField()
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
    deleted = models.BooleanField()
    derivative = models.ForeignKey(Derivative, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    harvest_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.harvest_id


class Lab_Result(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    failure = models.BooleanField()
    name = models.CharField(max_length=250, null=True, blank=True)
    sample_id = models.IntegerField(null=True, blank=True)
    test = models.IntegerField(null=True, blank=True)
    uom = models.CharField(max_length=250, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.sample_id)


class Lab_Sample_Result(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    lab_provided = models.BooleanField()
    sample_id = models.IntegerField(null=True, blank=True)
    test_id = models.IntegerField(null=True, blank=True)
    test_panel = models.CharField(max_length=250, null=True, blank=True)
    test_pass = models.BooleanField()
    test_value = models.FloatField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.sample_id)


class Lab_Sample(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField()
    amount = models.FloatField(null=True, blank=True)
    amount_used = models.FloatField(null=True, blank=True)
    deleted = models.BooleanField()
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    inventory_type = models.IntegerField(null=True, blank=True)
    lab_license = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    medical_grade = models.BooleanField()
    parent_id = models.CharField(max_length=250, null=True, blank=True)
    result = models.CharField(max_length=250, null=True, blank=True)
    results = models.ForeignKey(Lab_Result, on_delete=models.CASCADE)
    rn_d = models.BooleanField()
    sample_use = models.CharField(max_length=250, null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    test_results = models.ForeignKey(Lab_Sample_Result, on_delete=models.CASCADE)
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.biotrack_id)

class Inventory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory_name = models.CharField(max_length=250, null=True, blank=True)
    current_room = models.IntegerField(null=True, blank=True)
    deleted = models.BooleanField()
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #BiotrackAPI key = 'id'
    id_serial = models.IntegerField(null=True, blank=True)
    inventory_type = models.IntegerField(null=True, blank=True)
    lab_sample = models.ForeignKey(Lab_Sample, on_delete=models.CASCADE)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    med_usable_weight = models.FloatField(null=True, blank=True)
    medicated = models.BooleanField()
    product_name = models.CharField(max_length=250, null=True, blank=True)
    qa_status = models.CharField(max_length=250, null=True, blank=True)
    rec_usable_weight = models.FloatField(null=True, blank=True)
    remaining_amount = models.FloatField(null=True, blank=True)
    seized = models.BooleanField()
    session_time = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    strain = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    unit_based = models.BooleanField()
    usable_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.inventory_name


class Inventory_Room(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted = models.BooleanField()
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    location_license = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    quarantine = models.BooleanField()
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Inventory_Sublot(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    inventory_ids = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    new_room_id = models.IntegerField(null=True, blank=True)


class Plant_Cure(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cure_id = models.CharField(max_length=250, null=True, blank=True)
    deleted = models.BooleanField()
    derivative = models.ForeignKey(Derivative, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.cure_id


class Invoice_Inventory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(null=True, blank=True)
    deleted = models.BooleanField()
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    invoice_id = models.CharField(max_length=250, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True) 
    uom = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.inventory_id

class Invoice_Model(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accepted = models.BooleanField()
    buyer_location_license = models.CharField(max_length=250, null=True, blank=True)
    deleted = models.BooleanField()
    inventory = models.ForeignKey(Invoice_Inventory, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=250, null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    refund_invoice_id = models.CharField(max_length=250, null=True, blank=True)
    refunded = models.BooleanField()
    session_time = models.IntegerField(null=True, blank=True) 
    transaction_id = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.invoice_id


class Manifest_Driver(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dateof_birth = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Stop_Item(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted = models.BooleanField()
    description = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    inventory_id = models.CharField(max_length=250, null=True, blank=True)
    manifest_id = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    quantity_received = models.FloatField(null=True, blank=True)
    session_time = models.IntegerField(null=True, blank=True)
    stop_number = models.IntegerField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.manifest_id


class Manifest_Stop(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approximate_arrival = models.CharField(max_length=250, null=True, blank=True)
    approximate_departure = models.CharField(max_length=250, null=True, blank=True)
    approximate_route = models.CharField(max_length=250, null=True, blank=True)
    driver_arrived = models.BooleanField()
    driver_arrived_time = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    invoice = models.ForeignKey(Invoice_Model, on_delete=models.CASCADE)
    biotrack_invoice_id = models.CharField(max_length=250, null=True, blank=True) #Original BiotrackAPI key = 'invoice_id'
    items = models.ForeignKey(Stop_Item, on_delete=models.CASCADE)
    items_count = models.IntegerField(null=True, blank=True)
    location_license = models.CharField(max_length=250, null=True, blank=True)
    manifest_id = models.CharField(max_length=250, null=True, blank=True)
    stop_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.manifest_id


class Manifest_Vehicle(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.CharField(max_length=250, null=True, blank=True) #Original BiotrackAPI key = 'id'
    vehicle_name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.vehicle_name


class Manifest_ThirdPartyTransporter(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_number = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Manifest(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=250, null=True, blank=True)
    completed = models.BooleanField()
    completion_date = models.CharField(max_length=250, null=True, blank=True)
    created_on = models.CharField(max_length=250, null=True, blank=True)
    deleted = models.BooleanField()
    driver_arrived = models.BooleanField()
    drivers = models.ForeignKey(Manifest_Driver, on_delete=models.CASCADE)
    in_transit = models.BooleanField()
    is_accepted = models.BooleanField()
    is_parked = models.BooleanField()
    license_number = models.CharField(max_length=250, null=True, blank=True)
    manifest_id = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    received = models.BooleanField()
    session_time = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    stop_count = models.IntegerField(null=True, blank=True)
    stops = models.ForeignKey(Manifest_Stop, on_delete=models.CASCADE)
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

class Grow_Room(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted = models.BooleanField()
    external_id = models.CharField(max_length=250, null=True, blank=True)
    biotrack_id = models.IntegerField(null=True, blank=True) #BiotrackAPI key = 'id'
    location_license = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    updated_on = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
    



