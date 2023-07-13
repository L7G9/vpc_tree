# tags.py

"""Helper functions to access information in AWS resource tags in the data
    structures returned by Boto3."""


def get_tag(tags, key):
    """Get tag with a given key from a list of tags.

    Args:
        tags: A list of dictionaries containing AWS resource tags as defined
            in boto3.
        key: A string containing the name value of the tag's ket to find.

    return:
        A dictionary representing the AWS resource tag.
    """
    return next(filter(lambda d: d.get("Key") == key, tags), None)


def get_tag_value(tags, key):
    """Get value of a tag from s list of tags.

    Args:
        tags: A list of dictionaries containing AWS resource tags as defined
            in boto3.
        key: A string containing the name value of the tag's ket to find.

    return:
        A string containing the value of the AWS resource tag. None if no tag
            with that key is found.
    """
    tag = get_tag(tags, key)
    if tag is not None:
        return tag["Value"]
    return None
