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

class InlineResponse200(object):
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
        'continuous_aperture_auto_exposure': 'bool',
        'aperture_stop': 'ApertureStop',
        'normalised': 'Normalised',
        'aperture_number': 'ApertureNumber'
    }

    attribute_map = {
        'continuous_aperture_auto_exposure': 'continuousApertureAutoExposure',
        'aperture_stop': 'apertureStop',
        'normalised': 'normalised',
        'aperture_number': 'apertureNumber'
    }

    def __init__(self, continuous_aperture_auto_exposure=None, aperture_stop=None, normalised=None, aperture_number=None):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger"""  # noqa: E501
        self._continuous_aperture_auto_exposure = None
        self._aperture_stop = None
        self._normalised = None
        self._aperture_number = None
        self.discriminator = None
        if continuous_aperture_auto_exposure is not None:
            self.continuous_aperture_auto_exposure = continuous_aperture_auto_exposure
        if aperture_stop is not None:
            self.aperture_stop = aperture_stop
        if normalised is not None:
            self.normalised = normalised
        if aperture_number is not None:
            self.aperture_number = aperture_number

    @property
    def continuous_aperture_auto_exposure(self):
        """Gets the continuous_aperture_auto_exposure of this InlineResponse200.  # noqa: E501

        Is Aperture controlled by auto exposure  # noqa: E501

        :return: The continuous_aperture_auto_exposure of this InlineResponse200.  # noqa: E501
        :rtype: bool
        """
        return self._continuous_aperture_auto_exposure

    @continuous_aperture_auto_exposure.setter
    def continuous_aperture_auto_exposure(self, continuous_aperture_auto_exposure):
        """Sets the continuous_aperture_auto_exposure of this InlineResponse200.

        Is Aperture controlled by auto exposure  # noqa: E501

        :param continuous_aperture_auto_exposure: The continuous_aperture_auto_exposure of this InlineResponse200.  # noqa: E501
        :type: bool
        """

        self._continuous_aperture_auto_exposure = continuous_aperture_auto_exposure

    @property
    def aperture_stop(self):
        """Gets the aperture_stop of this InlineResponse200.  # noqa: E501


        :return: The aperture_stop of this InlineResponse200.  # noqa: E501
        :rtype: ApertureStop
        """
        return self._aperture_stop

    @aperture_stop.setter
    def aperture_stop(self, aperture_stop):
        """Sets the aperture_stop of this InlineResponse200.


        :param aperture_stop: The aperture_stop of this InlineResponse200.  # noqa: E501
        :type: ApertureStop
        """

        self._aperture_stop = aperture_stop

    @property
    def normalised(self):
        """Gets the normalised of this InlineResponse200.  # noqa: E501


        :return: The normalised of this InlineResponse200.  # noqa: E501
        :rtype: Normalised
        """
        return self._normalised

    @normalised.setter
    def normalised(self, normalised):
        """Sets the normalised of this InlineResponse200.


        :param normalised: The normalised of this InlineResponse200.  # noqa: E501
        :type: Normalised
        """

        self._normalised = normalised

    @property
    def aperture_number(self):
        """Gets the aperture_number of this InlineResponse200.  # noqa: E501


        :return: The aperture_number of this InlineResponse200.  # noqa: E501
        :rtype: ApertureNumber
        """
        return self._aperture_number

    @aperture_number.setter
    def aperture_number(self, aperture_number):
        """Sets the aperture_number of this InlineResponse200.


        :param aperture_number: The aperture_number of this InlineResponse200.  # noqa: E501
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
        if issubclass(InlineResponse200, dict):
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
        if not isinstance(other, InlineResponse200):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
