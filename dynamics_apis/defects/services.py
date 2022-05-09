"""
Services that get and push information to Kairnial WS servers for reserves.php
"""

from django.conf import settings

from dynamics_apis.common.services import KairnialWSService


class KairnialDefectService(KairnialWSService):
    """
    Service that fetches and pushes defects
    """
    service_domain = 'reserves'



    def list(self, filters: dict = None, offset: int = 0,
             limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List defects
        :param filters: Serialized DefectQuerySerializer
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :return:
        """
        parameters = {
            'LIMITSKIP': offset,
            'LIMITTAKE': limit,
            'limited': {
                'lastId': offset,
                'nbItems': limit
            },
            'flag': 3, # Because...
            'giveMeC': 'true', # Pagination
            'mainPrimaryArea': True, # show areas on plan
            'backDays': -1, # filter on date, includes all
            'comment': False # get comments
        }
        if filters:
            parameters.update({key: value for key, value in filters.items() if value})
        return self.call(action='getFlexAllReserves', parameters=[parameters],
                         use_cache=True)

    def get(self, pin_id: int):
        """
        Get a defect detail
        :param pin_id: numeric pin ID
        """
        limit = 100
        offset = 0
        parameters = {
            'LIMITSKIP': offset,
            'LIMITTAKE': limit,
            'limited': {
                'lastId': offset,
                'nbItems': limit
            },
            'flag': 3,  # Because...
            'giveMeC': 'true',  # Pagination
            'mainPrimaryArea': True,  # show areas on plan
            'backDays': -1,  # filter on date, includes all
            'comment': False,  # get comments
            'uuidFilter': [pin_id, ]
        }
        return self.call(action='getFlexAllReserves', parameters=[parameters])

    def attachments(self, template_id: str):
        """
        Get file attachments on template by ID
        :param template_id: Numerric ID of the template
        """
        # TODO: test function arguments and returned values
        parameters = {'templateId': template_id}
        return self.call(action='getAttachedFilesByTemplateId', service='formControls', parameters=parameters)

    def create(self, defect_create_serializer: dict):
        """
        Defect creation service
        :param defect_create_serializer: serialized data from DefectCreateSerializer
        """
        return None
        # TODO: Check data before pushing to the backend because there is no verification whatsoever
        # return self.call(
        #    action='addReserve',
        #    parameters=[defect_create_serializer],
        # )

    def areas(self):
        """
        Get a list of areas
        """
        return self.call(
            action='getAreas',
            parameters=[]
        )

    def bim_categories(self):
        """
        List BIM categories on defects
        """
        return self.call(
            action='getBimCategories',
            parameters=[]
        )

    def bim_levels(self):
        """
        List BIM levels on defects
        """
        return self.call(
            action='getBimLevels',
            parameters=[]
        )

