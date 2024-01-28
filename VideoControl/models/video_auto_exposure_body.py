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

class VideoAutoExposureBody(object):
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
        'mode': 'AutoExposureMode'
    }

    attribute_map = {
        'mode': 'mode'
    }

    def __init__(self, mode=None):  # noqa: E501
        """VideoAutoExposureBody - a model defined in Swagger"""  # noqa: E501
        self._mode = None
        self.discriminator = None
        if mode is not None:
            self.mode = mode

    @property
    def mode(self):
        """Gets the mode of this VideoAutoExposureBody.  # noqa: E501


        :return: The mode of this VideoAutoExposureBody.  # noqa: E501
        :rtype: AutoExposureMode
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this VideoAutoExposureBody.


        :param mode: The mode of this VideoAutoExposureBody.  # noqa: E501
        :type: AutoExposureMode
        """

        self._mode = mode

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
        if issubclass(VideoAutoExposureBody, dict):
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
        if not isinstance(other, VideoAutoExposureBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
