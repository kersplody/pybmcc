# coding: utf-8

"""
    Media Control API

    API for controlling media devices in Blackmagic Design products.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ActiveMedia(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'workingset_index': 'int',
        'device_name': 'str'
    }

    attribute_map = {
        'workingset_index': 'workingsetIndex',
        'device_name': 'deviceName'
    }

    def __init__(self, workingset_index=None, device_name=None):  # noqa: E501
        """ActiveMedia - a model defined in Swagger"""  # noqa: E501
        self._workingset_index = None
        self._device_name = None
        self.discriminator = None
        if workingset_index is not None:
            self.workingset_index = workingset_index
        if device_name is not None:
            self.device_name = device_name

    @property
    def workingset_index(self):
        """Gets the workingset_index of this ActiveMedia.  # noqa: E501

        Working set index of the active media device  # noqa: E501

        :return: The workingset_index of this ActiveMedia.  # noqa: E501
        :rtype: int
        """
        return self._workingset_index

    @workingset_index.setter
    def workingset_index(self, workingset_index):
        """Sets the workingset_index of this ActiveMedia.

        Working set index of the active media device  # noqa: E501

        :param workingset_index: The workingset_index of this ActiveMedia.  # noqa: E501
        :type: int
        """

        self._workingset_index = workingset_index

    @property
    def device_name(self):
        """Gets the device_name of this ActiveMedia.  # noqa: E501

        Internal device name of this media device  # noqa: E501

        :return: The device_name of this ActiveMedia.  # noqa: E501
        :rtype: str
        """
        return self._device_name

    @device_name.setter
    def device_name(self, device_name):
        """Sets the device_name of this ActiveMedia.

        Internal device name of this media device  # noqa: E501

        :param device_name: The device_name of this ActiveMedia.  # noqa: E501
        :type: str
        """

        self._device_name = device_name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ActiveMedia, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ActiveMedia):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other