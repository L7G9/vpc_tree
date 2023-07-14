# tags.py
"""Helper functions to access information in AWS resource tags in the data
structures returned by Boto3."""


def get_tag(resource, key):
    """Get tag with a given key from a AWS resource dictionary.

    Args:
        resource: A dictionary decribing a AWS resource tags as defined in boto3.
        key: A string containing the name value of the tag's key to find.

    return:
        A dictionary representing the AWS resource tag.
        None if resource as no Tags or Tags does no contain Tag with given key.
    """
    if 'Tags' in resource:
        return next(filter(lambda d: d.get('Key') == key, resource['Tags']), none)
    else:
        return None

def get_tag_value(resource, key):
    """Get value of tag with a given key from a AWS resource dictionary.

    Args:
        resource: A dictionary decribing a AWS resource tags as defined in boto3.
        key: A string containing the name value of the tag's key to find.

    return:
        A string containing the value of the AWS resource tag.
        None if no tag with that key is found.
    """
    tag = get_tag(resource, key)
    if tag is not None:
        return tag['Value']
    else:
        return None
