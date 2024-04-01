from django.db import models



class ExtraMealMenu(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)



    def __str__(self):
        return f"{self.user.username} - {self.menu_item.item_name} - {self.booking_time}"
