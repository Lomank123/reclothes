import re
from orders.consts import UUID4_REGEX


def get_product_media_path(instance, filename):
    """Return path where product images will be uploaded."""
    # file will be uploaded to MEDIA_ROOT/<product_id>/<filename>
    return 'product_{0}/{1}'.format(instance.product.pk, filename)


def get_product_file_path(instance, filename):
    """Return path where product file will be uploaded."""
    # file will be uploaded to MEDIA_ROOT/<product_id>/content/<filename>
    return 'product_{0}/content/{1}'.format(instance.product.pk, filename)


def valid_uuid(uuid):
    regex = re.compile(UUID4_REGEX, re.I)
    match = regex.match(uuid)
    return bool(match)
