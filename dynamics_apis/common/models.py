"""
Common models for all Kairnial objects
"""
import inspect
from django.conf import settings


class PaginatedModel:
    page_size = getattr(settings, 'PAGE_SIZE', 100)

    @classmethod
    def paginated_list(
            cls,
            client_id: str,
            token: str,
            project_id: str = None,
            page_offset: int = 0,
            page_limit: int = 100,
            **kwargs
    ):
        """
        Generate a subset of the list
        :return: total: int, paginated_list: [], page_offset: int, page_limit: int
        """
        if set(inspect.getfullargspec(cls.list).args) & {'page_offset', 'page_limit'} == {'page_offset', 'page_limit'}:
            # Kairnial function call supports pagination
            response = cls.list(
                client_id=client_id,
                token=token,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit,
                **kwargs
            )
            total = response.get('total', 0)
            paginated_list = response.get('items', [])
            page_offset = response.get('LIMITSKIP', page_offset)
            page_limit = response.get('LIMITTAKE', page_limit)
            return total, paginated_list, page_offset, page_limit
        else:
            # Manual pagination when not supported by Kairnial WS
            obj_list = cls.list(
                client_id=client_id,
                token=token,
                project_id=project_id,
                **kwargs
            )
            total = len(obj_list)
            paginated_list = obj_list[page_offset: page_offset + page_limit]
            return total, paginated_list, page_offset, page_limit