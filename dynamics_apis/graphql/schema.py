"""
Djangophysics GraphQL schemas
"""

from ariadne import QueryType, gql, make_executable_schema

# GraphQL Schema first
from ..projects.models import Project
from dynamics_apis.users.models.users import User
from dynamics_apis.users.models.groups import Group
from ..users.serializers.users import ProjectMemberSerializer
from ..users.serializers.groups import GroupSerializer
from ..projects.serializers import ProjectSerializer

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
        id: Int!,
        name: String!,
        description: String
    }
    
    type Project    {
        id: Int!,
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
        project_type: String
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
        "Searchable list of projects"
        projects(client_id: String!, search: String): [Project],
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
    if request.token:
        filters = {'email': request.user.email}
        user_list = User.list(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            filters=filters
        )
        serializer = ProjectMemberSerializer(user_list[0])
        return serializer.data

# Users resolver
@query.field("users")
def resolve_users(_, info, client_id, project_id, archived=0, full_name='', email=''):
    """
    Users resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    """
    request = info.context.get('request', None)
    print(request.token)
    if request.token:
        filters = {}
        if archived:
            filters['archived'] = archived
        if full_name:
            filters['full_name'] = full_name
        if email:
            filters['email'] = email
        user_list = User.list(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            filters=filters
        )
        serializer = ProjectMemberSerializer(user_list, many=True)
        return serializer.data


# Groups resolver
@query.field("groups")
def resolve_groups(_, info, client_id, project_id, name=''):
    """
    User resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    """
    request = info.context.get('request', None)
    filters = {}
    if name:
        filter['name'] = name
    if request.token:
        group_list = Group.list(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            filters=filters
        )
        serializer = GroupSerializer(group_list, many=True)
        return serializer.data

# Projects resolver
@query.field("projects")
def resolve_projects(_, info, client_id, oroject_id, search=''):
    """
    Projects resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    """
    request = info.context.get('request', None)
    if request.token:
        project_list = Project.list(
            client_id=client_id,
            token=request.token
        )
        serializer = ProjectSerializer(project_list, many=True)
        return serializer.data

schema = make_executable_schema(type_defs, query)