"""
Common models for all Kairnial objects
"""

from django.conf import settings


class PaginatedModel:
    page_size = getattr(settings, 'PAGE_SIZE', 100)

    @classmethod
    def paginated_list(
            cls,
            client_id: str,
            token: str,
            project_id: str,
            page_offset: int = 0,
            page_limit: int = 100,
            **kwargs
    ):
        """
        Generate a subset of the list
        :return: total: int, paginated_list: [], page_offset: int, page_limit: int
        """
        obj_list = cls.list(
            client_id=client_id,
            token=token,
            project_id=project_id,
            **kwargs
        )
        total = len(obj_list)
        print(len(obj_list), page_offset, page_limit + page_offset)
        paginated_list = obj_list[page_offset: page_offset + page_limit]
        return total, paginated_list, page_offset, page_limit