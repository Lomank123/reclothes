# Utils

def get_product_directory_path(instance, filename):
    """
    Return path where user files will be uploaded.
    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'product_{0}/{1}'.format(instance.product.id, filename)
