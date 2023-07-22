# test_tags.py

import pytest
from vpc_tree.tags import get_tag, get_tag_value


@pytest.fixture(scope="function")
def resource():
    return {
        'ResourceId': 'Res-01',
        'Tags': [
            {'Key': 'TagKey-01', 'Value': 'Res-01-TagValue-01'},
            {'Key': 'TagKey-02', 'Value': 'Res-01-TagValue-02'},
        ],
    }


@pytest.fixture(scope="function")
def resource_no_tags():
    return {
        'ResourceId': 'Res-02',
    }


class TestGetTag:
    def test_get_tag(self, resource):
        tag = get_tag(resource, "TagKey-01")
        assert tag == {'Key': 'TagKey-01', 'Value': 'Res-01-TagValue-01'}

    def test_get_tag_unknown_tag(self, resource):
        tag = get_tag(resource, "TagKey-99")
        assert tag is None

    def test_get_tag_no_tags(self, resource_no_tags):
        tag = get_tag(resource_no_tags, "TagKey-01")
        assert tag is None


class TestGetTagValue:
    def test_get_tag_value(self, resource):
        value = get_tag_value(resource, "TagKey-01")
        assert value == "Res-01-TagValue-01"
