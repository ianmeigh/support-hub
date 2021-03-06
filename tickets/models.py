"""Models for tickets application"""


import datetime as dt
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.core.validators import MinLengthValidator
from cloudinary.models import CloudinaryField
from model_utils import Choices

from .validators import textfield_not_empty, validate_image


class Team(models.Model):
    """Team model.

    Tickets objects can be set with one team to convey information about
    who is working on the request. Used when filtering tickets.
    """

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class TicketCategory(models.Model):
    """Ticket Category model.

    Tickets objects can be set with one category to convey information about
    the request. Used when filtering tickets.
    """

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Ticket model - Represent Support Tickets that can be raised by users"""

    STATUS = Choices(
        ("open", ("Open")),
        ("inprogress", ("In Progress")),
        ("onhold", ("On Hold")),
        ("closed", ("Closed")),
    )

    TYPE = Choices(
        ("request", ("Request")),
        ("incident", ("Incident")),
    )

    PRIORITY = Choices(
        ("low", ("Low")),
        ("medium", ("Medium")),
        ("high", ("High")),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_author",
    )
    title = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(int(10))],
        unique=False,
        blank=False,
    )
    description = models.TextField(
        validators=[textfield_not_empty(min_length=int(20))]
    )
    ticket_image = CloudinaryField(
        "image",
        validators=[validate_image],
        blank=True,
        help_text=(
            "Only 'jpg' or 'png' files permitted. Maximum file size is 3MB."
        ),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=STATUS.open,
    )
    type = models.CharField(
        max_length=8,
        choices=TYPE,
        default=TYPE.request,
    )
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY,
        default=PRIORITY.low,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.SET_NULL,
        related_name="ticket_category",
        blank=False,
        null=True,
    )
    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="assigned_team",
        blank=True,
        null=True,
    )
    assigned_technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_technician",
        blank=True,
        null=True,
    )

    class Meta:
        # Ordering configured to show the most recently updated tickets first
        ordering = ("-updated_on",)

    def __str__(self):
        return f"Request #: {self.id} - {self.title}"

    # CREDIT: CodingEntrepreneurs - Python & Django 3.2 Tutorial Series
    # Video 44 (get absolute url) & 45 (Django URLs Reverse)
    # URL: 44 - https://www.youtube.com/watch?v=b42B-xli-vQ
    # URL: 45 - https://www.youtube.com/watch?v=rm2YTMc2s10
    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.pk})

    @property
    def get_time_now(self):
        """Gets the current time (UTC timezone aware).

        Returns:
            datetime.datetime: Current time with timezone information (UTC)
        """
        return dt.datetime.now(dt.timezone.utc)

    def set_ticket_updated_now(self):
        """
        Sets the ticket model 'updated_on' field to the current time (UTC).
        """
        self.updated_on = self.get_time_now
        self.save(update_fields=["updated_on"])


class Comment(models.Model):
    """Comment Model."""

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
    )
    body = models.TextField(validators=[textfield_not_empty()])
    created_on = models.DateTimeField(auto_now_add=True)

    # Remove HTML tags in for comment body. For use in the admin panel
    # CREDIT: arie - Stack Overflow
    # URL: https://stackoverflow.com/a/9294835
    @property
    def body_without_tags(self):
        """Strips all HTML tags from the comment body (used to improve
        readability in the admin site).

        Returns:
            str: Comment body striped of all HTML tags
        """
        return strip_tags(self.body)
