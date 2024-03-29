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

class WorkingsetWorkingset(object):
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
        'index': 'int',
        'active_disk': 'bool',
        'volume': 'str',
        'device_name': 'str',
        'remaining_record_time': 'int',
        'total_space': 'int',
        'remaining_space': 'int',
        'clip_count': 'int'
    }

    attribute_map = {
        'index': 'index',
        'active_disk': 'activeDisk',
        'volume': 'volume',
        'device_name': 'deviceName',
        'remaining_record_time': 'remainingRecordTime',
        'total_space': 'totalSpace',
        'remaining_space': 'remainingSpace',
        'clip_count': 'clipCount'
    }

    def __init__(self, index=None, active_disk=None, volume=None, device_name=None, remaining_record_time=None, total_space=None, remaining_space=None, clip_count=None):  # noqa: E501
        """WorkingsetWorkingset - a model defined in Swagger"""  # noqa: E501
        self._index = None
        self._active_disk = None
        self._volume = None
        self._device_name = None
        self._remaining_record_time = None
        self._total_space = None
        self._remaining_space = None
        self._clip_count = None
        self.discriminator = None
        if index is not None:
            self.index = index
        if active_disk is not None:
            self.active_disk = active_disk
        if volume is not None:
            self.volume = volume
        if device_name is not None:
            self.device_name = device_name
        if remaining_record_time is not None:
            self.remaining_record_time = remaining_record_time
        if total_space is not None:
            self.total_space = total_space
        if remaining_space is not None:
            self.remaining_space = remaining_space
        if clip_count is not None:
            self.clip_count = clip_count

    @property
    def index(self):
        """Gets the index of this WorkingsetWorkingset.  # noqa: E501

        Index of this media in the working set  # noqa: E501

        :return: The index of this WorkingsetWorkingset.  # noqa: E501
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this WorkingsetWorkingset.

        Index of this media in the working set  # noqa: E501

        :param index: The index of this WorkingsetWorkingset.  # noqa: E501
        :type: int
        """

        self._index = index

    @property
    def active_disk(self):
        """Gets the active_disk of this WorkingsetWorkingset.  # noqa: E501

        Is this current item the active disk  # noqa: E501

        :return: The active_disk of this WorkingsetWorkingset.  # noqa: E501
        :rtype: bool
        """
        return self._active_disk

    @active_disk.setter
    def active_disk(self, active_disk):
        """Sets the active_disk of this WorkingsetWorkingset.

        Is this current item the active disk  # noqa: E501

        :param active_disk: The active_disk of this WorkingsetWorkingset.  # noqa: E501
        :type: bool
        """

        self._active_disk = active_disk

    @property
    def volume(self):
        """Gets the volume of this WorkingsetWorkingset.  # noqa: E501

        Volume name  # noqa: E501

        :return: The volume of this WorkingsetWorkingset.  # noqa: E501
        :rtype: str
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this WorkingsetWorkingset.

        Volume name  # noqa: E501

        :param volume: The volume of this WorkingsetWorkingset.  # noqa: E501
        :type: str
        """

        self._volume = volume

    @property
    def device_name(self):
        """Gets the device_name of this WorkingsetWorkingset.  # noqa: E501

        Internal device name of this media device  # noqa: E501

        :return: The device_name of this WorkingsetWorkingset.  # noqa: E501
        :rtype: str
        """
        return self._device_name

    @device_name.setter
    def device_name(self, device_name):
        """Sets the device_name of this WorkingsetWorkingset.

        Internal device name of this media device  # noqa: E501

        :param device_name: The device_name of this WorkingsetWorkingset.  # noqa: E501
        :type: str
        """

        self._device_name = device_name

    @property
    def remaining_record_time(self):
        """Gets the remaining_record_time of this WorkingsetWorkingset.  # noqa: E501

        Remaining record time on media device in seconds  # noqa: E501

        :return: The remaining_record_time of this WorkingsetWorkingset.  # noqa: E501
        :rtype: int
        """
        return self._remaining_record_time

    @remaining_record_time.setter
    def remaining_record_time(self, remaining_record_time):
        """Sets the remaining_record_time of this WorkingsetWorkingset.

        Remaining record time on media device in seconds  # noqa: E501

        :param remaining_record_time: The remaining_record_time of this WorkingsetWorkingset.  # noqa: E501
        :type: int
        """

        self._remaining_record_time = remaining_record_time

    @property
    def total_space(self):
        """Gets the total_space of this WorkingsetWorkingset.  # noqa: E501

        Total space on media device in bytes  # noqa: E501

        :return: The total_space of this WorkingsetWorkingset.  # noqa: E501
        :rtype: int
        """
        return self._total_space

    @total_space.setter
    def total_space(self, total_space):
        """Sets the total_space of this WorkingsetWorkingset.

        Total space on media device in bytes  # noqa: E501

        :param total_space: The total_space of this WorkingsetWorkingset.  # noqa: E501
        :type: int
        """

        self._total_space = total_space

    @property
    def remaining_space(self):
        """Gets the remaining_space of this WorkingsetWorkingset.  # noqa: E501

        Remaining space on media device in bytes  # noqa: E501

        :return: The remaining_space of this WorkingsetWorkingset.  # noqa: E501
        :rtype: int
        """
        return self._remaining_space

    @remaining_space.setter
    def remaining_space(self, remaining_space):
        """Sets the remaining_space of this WorkingsetWorkingset.

        Remaining space on media device in bytes  # noqa: E501

        :param remaining_space: The remaining_space of this WorkingsetWorkingset.  # noqa: E501
        :type: int
        """

        self._remaining_space = remaining_space

    @property
    def clip_count(self):
        """Gets the clip_count of this WorkingsetWorkingset.  # noqa: E501

        Number of clips currently on the device  # noqa: E501

        :return: The clip_count of this WorkingsetWorkingset.  # noqa: E501
        :rtype: int
        """
        return self._clip_count

    @clip_count.setter
    def clip_count(self, clip_count):
        """Sets the clip_count of this WorkingsetWorkingset.

        Number of clips currently on the device  # noqa: E501

        :param clip_count: The clip_count of this WorkingsetWorkingset.  # noqa: E501
        :type: int
        """

        self._clip_count = clip_count

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
        if issubclass(WorkingsetWorkingset, dict):
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
        if not isinstance(other, WorkingsetWorkingset):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
