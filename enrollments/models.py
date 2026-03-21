from django.db import models

class Enrollment(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    church = models.CharField(max_length=100)
    celphone = models.CharField(max_length=11)
    emergency_contact = models.CharField(max_length=11)
    email = models.EmailField()
    local_proof = models.CharField()
    payment_status = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    consent_given = models.BooleanField(default=False)
    ip_address = models.CharField()
