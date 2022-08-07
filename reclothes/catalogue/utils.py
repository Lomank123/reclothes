def get_product_media_path(instance, filename):
    """Return path where product images will be uploaded."""
    # file will be uploaded to MEDIA_ROOT/<product_id>/<filename>
    return 'product_{0}/{1}'.format(instance.product.pk, filename)
