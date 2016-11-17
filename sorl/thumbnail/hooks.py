import importlib

from django.core.exceptions import ImproperlyConfigured

from sorl.thumbnail.images import ImageFile


def load_path_attr(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


class ThumbnailDefaultHookset(object):

    IMAGE_FILE_CLASS = ImageFile


class HookProxy(object):

    def __getattr__(self, attr):
        from sorl.thumbnail.conf import settings
        return getattr(load_path_attr(settings.THUMBNAIL_HOOKSET)(), attr)


hookset = HookProxy()
