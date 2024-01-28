# coding: utf-8

"""
    Lens Control API

    API For controlling the lens on Blackmagic Design products  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class LensIrisBody(object):
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
        'aperture_stop': 'ApertureStop',
        'normalised': 'Normalised',
        'aperture_number': 'ApertureNumber'
    }

    attribute_map = {
        'aperture_stop': 'apertureStop',
        'normalised': 'normalised',
        'aperture_number': 'apertureNumber'
    }

    def __init__(self, aperture_stop=None, normalised=None, aperture_number=None):  # noqa: E501
        """LensIrisBody - a model defined in Swagger"""  # noqa: E501
        self._aperture_stop = None
        self._normalised = None
        self._aperture_number = None
        self.discriminator = None
        if aperture_stop is not None:
            self.aperture_stop = aperture_stop
        if normalised is not None:
            self.normalised = normalised
        if aperture_number is not None:
            self.aperture_number = aperture_number

    @property
    def aperture_stop(self):
        """Gets the aperture_stop of this LensIrisBody.  # noqa: E501


        :return: The aperture_stop of this LensIrisBody.  # noqa: E501
        :rtype: ApertureStop
        """
        return self._aperture_stop

    @aperture_stop.setter
    def aperture_stop(self, aperture_stop):
        """Sets the aperture_stop of this LensIrisBody.


        :param aperture_stop: The aperture_stop of this LensIrisBody.  # noqa: E501
        :type: ApertureStop
        """

        self._aperture_stop = aperture_stop

    @property
    def normalised(self):
        """Gets the normalised of this LensIrisBody.  # noqa: E501


        :return: The normalised of this LensIrisBody.  # noqa: E501
        :rtype: Normalised
        """
        return self._normalised

    @normalised.setter
    def normalised(self, normalised):
        """Sets the normalised of this LensIrisBody.


        :param normalised: The normalised of this LensIrisBody.  # noqa: E501
        :type: Normalised
        """

        self._normalised = normalised

    @property
    def aperture_number(self):
        """Gets the aperture_number of this LensIrisBody.  # noqa: E501


        :return: The aperture_number of this LensIrisBody.  # noqa: E501
        :rtype: ApertureNumber
        """
        return self._aperture_number

    @aperture_number.setter
    def aperture_number(self, aperture_number):
        """Sets the aperture_number of this LensIrisBody.


        :param aperture_number: The aperture_number of this LensIrisBody.  # noqa: E501
        :type: ApertureNumber
        """

        self._aperture_number = aperture_number

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
        if issubclass(LensIrisBody, dict):
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
        if not isinstance(other, LensIrisBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other