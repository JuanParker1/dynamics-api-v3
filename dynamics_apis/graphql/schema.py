"""
Djangophysics GraphQL schemas
"""
from datetime import datetime, date

from ariadne import QueryType, gql, make_executable_schema

# GraphQL Schema first
from ..users.models import User, Group
from ..users.serializers import ProjectMemberSerializer, GroupSerializer
from ..projects.serializers import ProjectSerializer

type_defs = '''

    """
    User GraphQL services,
    """
    type User   {
        id: Int!,
        full_name: String!,
        email: String,
        archived: Bool
    }
    
    type Group   {
        id: Int!,
        name: String!,
        description: String
    }
    
    type Project    {
        id Int!,
        name String!,
        services_backend String!,
        # "Karnial has servers in multiple locations, this provides info on the location of the data
        authentication_backend String!,
        active Bool,
        maintenance Bool,
        metadata String,
        application_type String,
        creation_date String!,
        last_activity String,
        project_type String
    }
    
    """
    Root Query
    """
    type Query {
        "Current user resolver"
        user((client_id: String, project_id String): User
        "Searchable list of users"
        users(client_id: String, project_id String, archived: Bool, full_name: String, email: String): [User]
        "Searchable list of groups"
        groups(client_id: String, project_id String, name: String): [Group]
        "Searchable list of projects"
        projects(search: String): [Project] 
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
    filters = {'email': request.user.email}
    if request and request.user:
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
def resolve_users(_, info, client_id, project_id, archived, full_name, email):
    """
    Users resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    """
    request = info.context.get('request', None)
    filters = {'archived': archived, 'full_name': full_name, 'email': email}
    if request and request.user:
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
def resolve_groups(_, info, client_id, project_id, name):
    """
    User resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    """
    request = info.context.get('request', None)
    filters = {'name': name}
    if request and request.user:
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
def resolve_projects(_, info, client_id, oroject_id, search):
    """
    Projects resolver, if user is connected
    :param _: all params
    :param info: QraphQL request context
    """
    request = info.context.get('request', None)
    if request and request.user:
        project_list = Project.list(
            client_id=client_id,
            token=request.token,
            project_id=project_id
        )
        serializer = GroupSerializer(project_list, many=True)
        return serializer.data