from django.db import models

# Create your models here.
from django.urls import reverse  # To generate URLS by reversing URL patterns
#from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid  # Required for unique tool instances
from datetime import date

from django.conf import settings  # Required to assign User as a borrower


class Category(models.Model):
    """Model representing a tool category."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a tool category e.g. 'gardening', 'decorating'."
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return reverse('category-detail', args=[str(self.id)])

class Tool(models.Model):
    """Model representing a tool (but not a specific copy of a tool)."""
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(
        Category, help_text="Select a category")
    # ManyToManyField used because a category can contain many tools and a Tool can cover many categorys.
    # category class has already been defined so we can specify the object above.

    def display_category(self):
        """Creates a string for the category. This is required to display category in Admin."""
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'

    def get_absolute_url(self):
        """Returns the url to access a particular tool record."""
        return reverse('tool-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        # the second title() is a string method to 
        # enforce caps on words in title
        return (self.name.title())



class ToolInstance(models.Model):
    """Model representing a specific copy of a tool (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular tool across whole library")
    tool = models.ForeignKey('Tool', on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """Determines if the tool is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='tool availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set tool as returned"),)

    def get_absolute_url(self):
        """Returns the url to access a particular tool instance."""
        return reverse('toolinstance-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.tool.name})'

