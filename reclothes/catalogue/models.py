from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from catalogue.utils import get_product_directory_path


class CustomBaseModel(models.Model):
    """
    Abstract model with creation and last update date fields.
    """

    creation_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Creation date"),
        help_text=_("Not required")
    )
    last_update = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Last update"),
        help_text=_("Not required")
    )

    def save(self, *args, **kwargs):
        date = timezone.now()
        if self.creation_date is None:
            self.creation_date = date
        self.last_update = date
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(CustomBaseModel):
    name = models.CharField(
        max_length=255,
        help_text=_("Required and unique"),
        verbose_name=_("Name"),
        unique=True
    )
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalogue:category_list", kwargs={"pk": self.pk})


class Tag(CustomBaseModel):
    """
    Tags to different products.
    """
    name = models.CharField(max_length=64, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class ProductType(models.Model):
    """
    Type of product (e.g. boots, T-shirt, jacket).
    """

    name = models.CharField(max_length=255, verbose_name=_("Type"), help_text=_("Required"), unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
    Product attribute model which allows to add properties to certain product types (e.g. shoe size).
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, verbose_name=_("Attribute name"), help_text=_("Required"))

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")

    def __str__(self):
        return self.name


class Product(CustomBaseModel):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    title = models.CharField(verbose_name=_("Title"), help_text=_("Required"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), help_text=_("Not required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular_price"),
        help_text=_("Maximum 9999.99"),
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )

    class Meta:
        ordering = ["-creation_date"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalogue:product_detail", kwargs={"pk": self.pk})


class ProductAttributeValue(models.Model):
    """
    Value of product attribute. Connected with product as well.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product attribute value. Maximum of 255 words."),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Attribute Value")
        verbose_name_plural = _("Product Attribute Values")

    def __str__(self):
        return self.value


class ProductReview(CustomBaseModel):
    """
    Sort of a comment to product with its own rating.
    """
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    text = models.TextField(verbose_name=_("Review text"), help_text=_("Review"), blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rating"),
        help_text=_("Choose from 1 to 5"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")


class ProductImage(CustomBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to=get_product_directory_path,
    )
    alt_text = models.CharField(
        max_length=255,
        verbose_name=_("Alturnative text"),
        help_text=_("Add alternative text"),
    )
    is_feature = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
