"""
Djangophysics GraphQL schemas
"""

from ariadne import QueryType, gql, make_executable_schema

from dynamics_apis.projects.models import Project
from dynamics_apis.users.models.contacts import Contact
from dynamics_apis.users.models.groups import Group
from dynamics_apis.users.models.users import User
from dynamics_apis.users.serializers.contacts import ContactSerializer, ContactQuerySerializer
from dynamics_apis.users.serializers.groups import GroupSerializer, GroupQuerySerializer
from dynamics_apis.users.serializers.users import ProjectMemberSerializer, UserQuerySerializer
from .serializers.projects import ProjectGraphQLSerializer

# GraphQL Schema first
type_defs = '''

    """
    User GraphQL services,
    """
    type User   {
        id: Int!,
        full_name: String!,
        email: String,
        archived: Boolean
    }
    
    type Group   {
        id: String!,
        name: String!,
        description: String
    }
    
    type Contact   {
        id: Int!,
        uuid: String!,
        name: String,
        alternative_name: String,
        company_name: String,
        company_category: String,
        short_name: String,
        link_to_defects: Boolean,
        address: String,
        zipcode: String,
        city: String,
        county: String,
        country: String,
        direct_phone: String,
        fax: String,
        mobile: String,
        url: String,
        email: String,
        description: String,
        external_reference: String,
        created_at: String,
        updated_at: String,
        created_by: User
    }
    
    type Project    {
        id: String!,
        name: String!,
        services_backend: String!,
        # "Karnial has servers in multiple locations, this provides info on the location of the data
        authentication_backend: String!,
        active: Boolean,
        maintenance: Boolean,
        metadata: String,
        application_type: String,
        creation_date: String!,
        last_activity: String,
        project_type: String,
        users(archived: Boolean, full_name: String, email: String): [User],
        groups(name: String): [Group],
        contacts(type: String, search: String, ids: [Int], created_start: String, created_end: String, update_start: String, update_end: String): [Contact]
    }
    
    """
    Root Query
    """
    type Query {
        "Current user resolver"
        user(client_id: String!, project_id: String!): User,
        "Searchable list of users"
        users(client_id: String!, project_id: String!, archived: Boolean, full_name: String, email: String): [User],
        "Searchable list of groups"
        groups(client_id: String!, project_id: String!, name: String): [Group],
        "Searchable list of contacts"
        contacts(client_id: String!, project_id: String!, type: String, search: String, ids: [Int], created_start: String, created_end: String, update_start: String, update_end: String): [Contact],
        "Searchable list of projects"
        projects(client_id: String!, page_offset: Int = 0, page_limit: Int = 100, search: String): [Project]
    }
'''

gql(type_defs)

# Root resolver
query = QueryType()


# User resolver
@query.field("user")
def resolve_user(_, info, client_id, project_id):
    """
    User resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    :param client_id: ID of the client
    :param project_id: ID of the project
    """
    request = info.context.get('request', None)
    if hasattr(request, 'token'):
        filters = {'email': request.user.email}
        user_list = User.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            filters=filters
        )
        serializer = ProjectMemberSerializer(user_list[0])
        return serializer.data


# Users resolver
@query.field("users")
def resolve_users(_, info, client_id, project_id, **filters):
    """
    Users resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    :param client_id: ID of the client
    :param project_id: ID of the project
    """
    request = info.context.get('request', None)
    if hasattr(request, 'token'):
        usq = UserQuerySerializer(data=filters)
        usq.is_valid()
        user_list = User.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            filters=usq.validated_data
        )
        serializer = ProjectMemberSerializer(user_list, many=True)
        return serializer.data


# Groups resolver
@query.field("groups")
def resolve_groups(_, info, client_id, project_id, **filters):
    """
    User resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    :param client_id: ID of the client
    :param project_id: project RGOC
    """
    request = info.context.get('request', None)
    gqs = GroupQuerySerializer(data=filters)
    gqs.is_valid()
    if hasattr(request, 'token'):
        group_list = Group.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            filters=gqs.validated_data
        )
        serializer = GroupSerializer(group_list, many=True)
        return serializer.data


# Groups resolver
@query.field("contacts")
def resolve_contacts(_, info, client_id, project_id, **filters):
    """
    User resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    :param client_id: ID of the client
    :param project_id: ID of the project
    """
    request = info.context.get('request', None)
    cqs = ContactQuerySerializer(data=filters)
    cqs.is_valid()
    if hasattr(request, 'token'):
        contacts_list = Contact.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            filters=cqs.validated_data
        )
        serializer = ContactSerializer(contacts_list, many=True)
        return serializer.data


def enhance_project_list(obj_list, client_id, token, selections, user_id = None):
    """
    Inject client_id and token into lists to use in serializer relations
    """
    node_serializers = {
        'users': UserQuerySerializer,
        'groups': GroupQuerySerializer,
        'contacts': ContactQuerySerializer
    }
    filters = {}
    for sel in [s for s in selections if s in node_serializers]:
        nss = node_serializers[sel](data=selections.get(sel))
        nss.is_valid()
        filters[sel] = nss.validated_data
    for i in range(len(obj_list)):
        obj_list[i]['client_id'] = client_id
        obj_list[i]['token'] = token
        obj_list[i]['user_id'] = user_id
        for sel in ['contacts', 'groups', 'users']:
            selected = sel in selections
            obj_list[i][sel] = {
                'client_id': client_id, 'token': token,
                'project_id': obj_list[i]['g_nom'],
                'selected': selected,
                'filters': filters.get(sel, {})
            }


# Projects resolver
@query.field("projects")
def resolve_projects(_, info, client_id: str, page_offset: int = 0, page_limit: int = 100,
                     search=''):
    """
    Projects resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    :param client_id: ID of the client
    :param page_offset: # of first record
    :param page_limit: max nb of records per request
    :param search: full string search
    """
    request = info.context.get('request', None)
    if hasattr(request, 'token'):
        total, project_list, page_offset, page_limit = Project.paginated_list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            page_offset=page_offset,
            page_limit=page_limit,
            search=search
        )
        selections = {s.name.value: {a.name.value: a.value.value for a in s.arguments} for s in
                      info.field_nodes[0].selection_set.selections}
        enhance_project_list(
            obj_list=project_list,
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            selections=selections)
        serializer = ProjectGraphQLSerializer(project_list, many=True)
        return serializer.data


schema = make_executable_schema(type_defs, query)
