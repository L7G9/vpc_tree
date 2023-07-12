# tags.py


def get_tag(tags, key):
    return next(filter(lambda d: d.get("Key") == key, tags), None)


def get_tag_value(tags, key):
    tag = get_tag(tags, key)
    if tag is not None:
        return tag["Value"]
    return None
