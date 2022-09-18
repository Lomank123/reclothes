from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from catalogue.utils import get_product_media_path, get_product_file_path


class CustomBaseModel(models.Model):
    """
    Abstract model with creation and update datetime fields.

    save() method has been overriden to allow modifying dates during tests.
    """

    created_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Updated at"))

    def save(self, *args, **kwargs):
        date = timezone.now()
        if self.created_at is None:
            self.created_at = date
        self.updated_at = date
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(MPTTModel):
    """
    Category model implemented with MPTT
    so each category may have subcategories.
    """
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="children",
    )
    name = models.CharField(
        max_length=255,
        help_text=_("Required and unique"),
        verbose_name=_("Name"),
        unique=True,
    )
    slug = models.SlugField(
        max_length=255, unique=True, help_text=_("Category safe URL"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "catalogue:category_list", kwargs={"category_slug": self.slug})


class Tag(CustomBaseModel):
    """Tags to different products."""
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Type"),
        help_text=_("Required and unique"),
        unique=True,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")
        ordering = ['-is_active']

    def __str__(self):
        return f'{self.name} ({self.pk})'


class ProductAttribute(models.Model):
    """Allows to add properties to certain product types (e.g. shoe size)."""

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
        related_name="product_attrs",
        verbose_name=_("Product Type"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Attribute name"),
        help_text=_("Required and unique"),
        unique=True,
    )

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Product(CustomBaseModel):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
        related_name="products",
        verbose_name=_("Product Type"),
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="products",
        verbose_name=_("Category"),
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="tags", verbose_name=_("Tags"))
    title = models.CharField(
        verbose_name=_("Title"), help_text=_("Required"), max_length=255)
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Not required"), blank=True)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("Quantity"),
        help_text=_("How many products have left."),
    )
    regular_price = models.DecimalField(
        validators=[MinValueValidator(0.01)],
        verbose_name=_("Regular price"),
        help_text=_("Maximum 9999.99"),
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        help_text=_("Change product visibility"),
        default=True,
    )
    is_limited = models.BooleanField(
        default=True,
        verbose_name=_("Limited"),
        help_text=_("Depends on quantity."),
    )
    company = models.ForeignKey(
        to='accounts.Company',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='products',
        verbose_name=_('Company'),
    )
    keys_limit = models.IntegerField(
        default=1,
        verbose_name=_('Keys limit'),
        help_text=_('How many keys should user get per purchase.'),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f'{self.title} ({self.pk})'

    @property
    def in_stock(self):
        return self.quantity > 0

    @property
    def ordered_images(self):
        """Images ordered by is_feature."""
        return self.images.order_by('-is_feature')

    @property
    def attrs_with_values(self):
        """Attrs with related values."""
        return self.attr_values.select_related('attribute')

    @property
    def reviews_with_users(self):
        """Reviews with users ordered by creation date."""
        return self.reviews.select_related('user').order_by('-created_at')


class ProductAttributeValue(models.Model):
    """
    Value of product attribute.

    Connected with product as well.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="attr_values",
        verbose_name=_("Product"),
    )
    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.RESTRICT,
        verbose_name=_("Product attribute"),
        help_text=_("Product attribute name"),
    )
    value = models.CharField(
        max_length=255,
        verbose_name=_("Value"),
        help_text=_("Product attribute value"),
    )

    class Meta:
        verbose_name = _("Product Attribute Value")
        verbose_name_plural = _("Product Attribute Values")
        # Product can't have duplicate attributes
        constraints = [
            models.UniqueConstraint(
                fields=['product_id', 'attribute_id'],
                name='unique_value_constraint',
            ),
        ]

    def __str__(self):
        return self.value


class ProductReview(CustomBaseModel):
    """Comment to product with its own rating."""
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Product"),
    )
    text = models.TextField(
        verbose_name=_("Review text"), blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rating"),
        help_text=_("Choose from 1 to 5"),
        blank=True, null=True,
    )

    class Meta:
        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")
        # User cannot leave more than 1 comment to each product
        constraints = [
            models.UniqueConstraint(
                fields=['product_id', 'user_id'],
                name='unique_review_constraint',
            ),
        ]

    def __str__(self):
        return f'Review ({self.pk})'


class ProductImage(CustomBaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Product"),
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to=get_product_media_path,
    )
    alt_text = models.CharField(
        max_length=255,
        default="Alt text",
        verbose_name=_("Alternative text"),
        help_text=_("This displays when image fails to load."),
    )
    is_feature = models.BooleanField(
        default=False, verbose_name=_("Feature image"))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f'{self.alt_text} {self.pk}'


class ProductFile(CustomBaseModel):
    product = models.ForeignKey(
        Product,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("Product"),
    )
    file = models.FileField(
        upload_to=get_product_file_path,
        verbose_name=_("File"),
        help_text=_('User will be able to download this file after purchase.'),
    )
    link = models.URLField(
        max_length=255,
        blank=True, null=True,
        verbose_name=_('Download link'),
    )
    is_main = models.BooleanField(
        default=False, verbose_name=_("Main file"))

    class Meta:
        ordering = ['-id']
        verbose_name = _("Product File")
        verbose_name_plural = _("Product Files")

    def __str__(self):
        return f'File {self.pk} to product {self.product.pk}'


class ActivationKey(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name='activation_keys',
        verbose_name=_('Product'),
    )
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='activation_keys',
        verbose_name=_('Order'),
    )
    key = models.CharField(
        max_length=512,
        unique=True,
        verbose_name=_('Activation key'),
        help_text=_('Must be unique'),
    )
    expired_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Expiry date'))

    class Meta:
        ordering = ["-expired_at"]
        verbose_name = _("Activation key")
        verbose_name_plural = _("Activation keys")

    def __str__(self):
        return f'Activation key ({self.pk}) to product ({self.product.pk})'

    @property
    def expired(self):
        return self.expired_at < timezone.now()
