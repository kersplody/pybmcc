# coding: utf-8

"""
    System Control API

    API for controlling the System Modes on Blackmagic Design products.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SupportedFormat(object):
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
        'codecs': 'list[str]',
        'frame_rates': 'list[FrameRate]',
        'max_off_speed_frame_rate': 'float',
        'min_off_speed_frame_rate': 'float',
        'record_resolution': 'Resolution',
        'sensor_resolution': 'Resolution'
    }

    attribute_map = {
        'codecs': 'codecs',
        'frame_rates': 'frameRates',
        'max_off_speed_frame_rate': 'maxOffSpeedFrameRate',
        'min_off_speed_frame_rate': 'minOffSpeedFrameRate',
        'record_resolution': 'recordResolution',
        'sensor_resolution': 'sensorResolution'
    }

    def __init__(self, codecs=None, frame_rates=None, max_off_speed_frame_rate=None, min_off_speed_frame_rate=None, record_resolution=None, sensor_resolution=None):  # noqa: E501
        """SupportedFormat - a model defined in Swagger"""  # noqa: E501
        self._codecs = None
        self._frame_rates = None
        self._max_off_speed_frame_rate = None
        self._min_off_speed_frame_rate = None
        self._record_resolution = None
        self._sensor_resolution = None
        self.discriminator = None
        if codecs is not None:
            self.codecs = codecs
        if frame_rates is not None:
            self.frame_rates = frame_rates
        if max_off_speed_frame_rate is not None:
            self.max_off_speed_frame_rate = max_off_speed_frame_rate
        if min_off_speed_frame_rate is not None:
            self.min_off_speed_frame_rate = min_off_speed_frame_rate
        if record_resolution is not None:
            self.record_resolution = record_resolution
        if sensor_resolution is not None:
            self.sensor_resolution = sensor_resolution

    @property
    def codecs(self):
        """Gets the codecs of this SupportedFormat.  # noqa: E501


        :return: The codecs of this SupportedFormat.  # noqa: E501
        :rtype: list[str]
        """
        return self._codecs

    @codecs.setter
    def codecs(self, codecs):
        """Sets the codecs of this SupportedFormat.


        :param codecs: The codecs of this SupportedFormat.  # noqa: E501
        :type: list[str]
        """

        self._codecs = codecs

    @property
    def frame_rates(self):
        """Gets the frame_rates of this SupportedFormat.  # noqa: E501


        :return: The frame_rates of this SupportedFormat.  # noqa: E501
        :rtype: list[FrameRate]
        """
        return self._frame_rates

    @frame_rates.setter
    def frame_rates(self, frame_rates):
        """Sets the frame_rates of this SupportedFormat.


        :param frame_rates: The frame_rates of this SupportedFormat.  # noqa: E501
        :type: list[FrameRate]
        """

        self._frame_rates = frame_rates

    @property
    def max_off_speed_frame_rate(self):
        """Gets the max_off_speed_frame_rate of this SupportedFormat.  # noqa: E501


        :return: The max_off_speed_frame_rate of this SupportedFormat.  # noqa: E501
        :rtype: float
        """
        return self._max_off_speed_frame_rate

    @max_off_speed_frame_rate.setter
    def max_off_speed_frame_rate(self, max_off_speed_frame_rate):
        """Sets the max_off_speed_frame_rate of this SupportedFormat.


        :param max_off_speed_frame_rate: The max_off_speed_frame_rate of this SupportedFormat.  # noqa: E501
        :type: float
        """

        self._max_off_speed_frame_rate = max_off_speed_frame_rate

    @property
    def min_off_speed_frame_rate(self):
        """Gets the min_off_speed_frame_rate of this SupportedFormat.  # noqa: E501


        :return: The min_off_speed_frame_rate of this SupportedFormat.  # noqa: E501
        :rtype: float
        """
        return self._min_off_speed_frame_rate

    @min_off_speed_frame_rate.setter
    def min_off_speed_frame_rate(self, min_off_speed_frame_rate):
        """Sets the min_off_speed_frame_rate of this SupportedFormat.


        :param min_off_speed_frame_rate: The min_off_speed_frame_rate of this SupportedFormat.  # noqa: E501
        :type: float
        """

        self._min_off_speed_frame_rate = min_off_speed_frame_rate

    @property
    def record_resolution(self):
        """Gets the record_resolution of this SupportedFormat.  # noqa: E501


        :return: The record_resolution of this SupportedFormat.  # noqa: E501
        :rtype: Resolution
        """
        return self._record_resolution

    @record_resolution.setter
    def record_resolution(self, record_resolution):
        """Sets the record_resolution of this SupportedFormat.


        :param record_resolution: The record_resolution of this SupportedFormat.  # noqa: E501
        :type: Resolution
        """

        self._record_resolution = record_resolution

    @property
    def sensor_resolution(self):
        """Gets the sensor_resolution of this SupportedFormat.  # noqa: E501


        :return: The sensor_resolution of this SupportedFormat.  # noqa: E501
        :rtype: Resolution
        """
        return self._sensor_resolution

    @sensor_resolution.setter
    def sensor_resolution(self, sensor_resolution):
        """Sets the sensor_resolution of this SupportedFormat.


        :param sensor_resolution: The sensor_resolution of this SupportedFormat.  # noqa: E501
        :type: Resolution
        """

        self._sensor_resolution = sensor_resolution

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
        if issubclass(SupportedFormat, dict):
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
        if not isinstance(other, SupportedFormat):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other