"""
Script with custom Exceptions and Errors for the Mental State Improvement Project
"""


class BaseMSIProjectException(Exception):
    pass


class ImageException(BaseMSIProjectException):
    pass


class APINotAvailable(ImageException):
    pass


class NoResponseError(ImageException):
    pass


class PexelAPIKeyError(ImageException):
    pass


class JsonError(ImageException):
    pass


class QuoteException(BaseMSIProjectException):
    pass


class NoResponseFromQuoteUrl(QuoteException):
    pass


class JSONExtractError(QuoteException):
    pass


class MessageException(BaseMSIProjectException):
    pass


class WebhookUrlError(MessageException):
    pass