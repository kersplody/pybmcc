# coding: utf-8

"""
    Video Control API

    API For controlling the video on Blackmagic Design products  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InlineResponse2006(object):
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
        'continuous_shutter_auto_exposure': 'bool',
        'shutter_speed': 'ShutterSpeed',
        'shutter_angle': 'ShutterAngle'
    }

    attribute_map = {
        'continuous_shutter_auto_exposure': 'continuousShutterAutoExposure',
        'shutter_speed': 'shutterSpeed',
        'shutter_angle': 'shutterAngle'
    }

    def __init__(self, continuous_shutter_auto_exposure=None, shutter_speed=None, shutter_angle=None):  # noqa: E501
        """InlineResponse2006 - a model defined in Swagger"""  # noqa: E501
        self._continuous_shutter_auto_exposure = None
        self._shutter_speed = None
        self._shutter_angle = None
        self.discriminator = None
        if continuous_shutter_auto_exposure is not None:
            self.continuous_shutter_auto_exposure = continuous_shutter_auto_exposure
        if shutter_speed is not None:
            self.shutter_speed = shutter_speed
        if shutter_angle is not None:
            self.shutter_angle = shutter_angle

    @property
    def continuous_shutter_auto_exposure(self):
        """Gets the continuous_shutter_auto_exposure of this InlineResponse2006.  # noqa: E501

        Is shutter controlled by auto exposure  # noqa: E501

        :return: The continuous_shutter_auto_exposure of this InlineResponse2006.  # noqa: E501
        :rtype: bool
        """
        return self._continuous_shutter_auto_exposure

    @continuous_shutter_auto_exposure.setter
    def continuous_shutter_auto_exposure(self, continuous_shutter_auto_exposure):
        """Sets the continuous_shutter_auto_exposure of this InlineResponse2006.

        Is shutter controlled by auto exposure  # noqa: E501

        :param continuous_shutter_auto_exposure: The continuous_shutter_auto_exposure of this InlineResponse2006.  # noqa: E501
        :type: bool
        """

        self._continuous_shutter_auto_exposure = continuous_shutter_auto_exposure

    @property
    def shutter_speed(self):
        """Gets the shutter_speed of this InlineResponse2006.  # noqa: E501


        :return: The shutter_speed of this InlineResponse2006.  # noqa: E501
        :rtype: ShutterSpeed
        """
        return self._shutter_speed

    @shutter_speed.setter
    def shutter_speed(self, shutter_speed):
        """Sets the shutter_speed of this InlineResponse2006.


        :param shutter_speed: The shutter_speed of this InlineResponse2006.  # noqa: E501
        :type: ShutterSpeed
        """

        self._shutter_speed = shutter_speed

    @property
    def shutter_angle(self):
        """Gets the shutter_angle of this InlineResponse2006.  # noqa: E501


        :return: The shutter_angle of this InlineResponse2006.  # noqa: E501
        :rtype: ShutterAngle
        """
        return self._shutter_angle

    @shutter_angle.setter
    def shutter_angle(self, shutter_angle):
        """Sets the shutter_angle of this InlineResponse2006.


        :param shutter_angle: The shutter_angle of this InlineResponse2006.  # noqa: E501
        :type: ShutterAngle
        """

        self._shutter_angle = shutter_angle

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
        if issubclass(InlineResponse2006, dict):
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
        if not isinstance(other, InlineResponse2006):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
