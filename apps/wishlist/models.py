from __future__ import unicode_literals
from ..login_and_reg.models import User
from django.db import models

# Create your models here.

class ItemManager(models.Manager):
    def create_item(self, form_data, user):
        errors = []
        if not form_data['name'] or form_data['name'] == '':
            errors.append("Please enter an item name")
        if len(form_data['name']) < 4:
            errors.append("Item name must be more than 3 characters")

        if errors:
            return (False, errors)

        item = Item.objects.create(name = form_data['name'], creator = user)
        item.user_added.add(user)
        return (True, item)

    def delete(self, id, user_id):
        item = Item.objects.get(id=id)
        item.delete()

    def join(self, id, user_id):
        item = Item.objects.get(id=id)
        item.user_added.add(user_id)

    def unjoin(self, id, user_id):
        item = Item.objects.get(id=id)
        item.user_added.remove(user_id)

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_added = models.ManyToManyField(User, related_name="added_to_wishlist")
    creator = models.ForeignKey(User, related_name="item_creator")
    objects = ItemManager()
