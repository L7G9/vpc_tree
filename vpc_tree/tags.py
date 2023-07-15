# tags.py
"""Helper functions to access information in AWS resource Tags in the data
structures returned by Boto3."""


def get_tag(resource, key):
    """Get Tag with a given key from a AWS resource dictionary.

    Args:
        resource: A dictionary describing a AWS resource Tags as defined in
        Boto3.
        key: A string containing the name value of the Tag's key to find.

    return:
        A dictionary representing the AWS resource Tag.
        None if resource as no Tags or Tags does no contain Tag with given key.
    """
    if 'Tags' in resource:
        return next(
            filter(lambda d: d.get('Key') == key, resource['Tags']),
            None
        )
    else:
        return None


def get_tag_value(resource, key):
    """Get value of Tag with a given key from a AWS resource dictionary.

    Args:
        resource: A dictionary describing a AWS resource Tags as defined in
        Boto3.
        key: A string containing the name value of the Tag's key to find.

    return:
        A string containing the value of the AWS resource Tag.
        None if no Tag with that key is found.
    """
    tag = get_tag(resource, key)
    if tag is not None:
        return tag['Value']
    else:
        return None
