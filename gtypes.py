import logging
import graphene
import mal_service
import array_conn

userXmlMap = {
    'user_id': 'id',
    'user_name': 'username',
    'user_watching': 'watching',
    'user_completed': 'completed',
    'user_onhold': 'onhold',
    'user_dropped': 'dropped',
    'user_plantowatch': 'planned',
    'user_days_spent_watching': 'days_spent_watching'
}

animeXmlMap = {
    'series_animedb_id': 'id',
    'series_title': 'title',
    'series_synonyms': 'synonyms',
    'series_type': 'type',
    'series_episodes': 'episodes',
    'series_status': 'status',
    'series_start': 'start_date',
    'series_end': 'end_date',
    'series_image': 'image_url'
}

# TODO: how can meta-program in python?

class AnimeXmlModel(object):
    def __init__(self, node):
        for attr in node:
            mapped = animeXmlMap.get(attr.tag)
            if mapped:
                setattr(self, mapped, attr.text)

class UserXmlModel(object):
    def __init__(self, node):
        self.series_list = map(AnimeXmlModel, node.findall('anime'))
        for attr in node.find('myinfo'):
            mapped = userXmlMap.get(attr.tag)
            # logging.info([attr.tag, mapped, attr.text])
            if mapped:
                setattr(self, mapped, attr.text)

class Anime(graphene.ObjectType):
    """Anime"""
    id = graphene.ID()
    title = graphene.String()
    synonyms = graphene.String()
    type = graphene.String()
    episodes = graphene.String()
    status = graphene.String()
    start_date = graphene.String()
    end_date = graphene.String()
    image_url = graphene.String()

class AnimeConnection(graphene.relay.Connection):
    class Meta:
        node = Anime

class User(graphene.ObjectType):
    """User"""
    id = graphene.ID()
    username = graphene.String()
    watching = graphene.Int()
    completed = graphene.Int()
    onhold = graphene.Int()
    dropped = graphene.Int()
    planned = graphene.Int()
    days_spent_watching = graphene.Float()
    series_list = graphene.relay.ConnectionField(AnimeConnection)

    def resolve_series_list(obj, args, context, info):
        return array_conn.resolve(obj.series_list, args)

class Query(graphene.ObjectType):
    viewer = graphene.Field(User, username=graphene.String())

    # TODO: pick up status and type from AST
    def resolve_viewer(obj, args, context, info):
        return UserXmlModel(mal_service.get_list(args.get('username')))
