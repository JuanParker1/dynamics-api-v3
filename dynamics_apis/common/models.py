
import uuid
from django.db import models
from django.conf import settings


class KairnialServiceError(Exception):
    message = "Service failed"


class KairnialObject:

    def list(self, **filters):
        """
        Get a list of objects
        :param filters: Dictonnary of filters
        :return:
        """
        pass

class KairnialServer:

    @staticmethod
    def header(request):
        return {
            'appType': 'API',
            'machineid': str(uuid.uuid4()),
            'RVersion': settings.KAIRNIAL_RVERSION,
            'SystemVersion': 1,
            'UserHash': request.user.user_hash,
            'UserLanguage': request.user.lang,
        }

