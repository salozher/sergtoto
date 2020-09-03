import hashlib
import os
import random
import string



def random_string_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    new_slug = "{randstr}".format(randstr=random_string_generator(size=32))
    return new_slug

