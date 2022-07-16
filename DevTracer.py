import functools
import neo4j.exceptions
from neo4j import GraphDatabase as gd
import webbrowser
import json
from time import sleep

# DEVELOPER NOTE: if more edges are added they should be added to this dict in the form of:
# (base node : connection name)
_TYPE_DICT = {'SysReq': 'implemented', 'HLR': 'implemented', 'LLR': 'implemented', 'code': 'implemented',
              'SystemTest': 'tests', 'HLT': 'tests', 'LLT': 'tests',
              'bug': 'bugs', 'verification': 'verifies'}

# DEVELOPER NOTE: change the login based on the server uri and the username password pair.
# Any neo4j server can be used but one can be setup using "neo4j desktop".
_LOGIN_INFO = {'uri': "bolt://localhost:7687", 'auth': ("neo4j", "12345")}

# DEVELOPER NOTE: change the version of the neovis.js library if required
# These changed might require changes in the html formatting
_NEOVIS_JS_VERSION = 'https://cdn.neo4jlabs.com/neovis.js/v1.5.0/neovis.js'


def _dictToStr(dict: dict):
    """

    :param dict: Json dictionary.
    :return: A string that represents the dictionary ready for a cypher query.
    """
    string = '{'
    for key, value in dict.items():
        string += (key + ': ')
        if type(value) == str:
            string += ("'" + str(value) + "', ")
        else:
            string += (str(value) + ", ")
    string = string[0:-2] + '}'
    return string


def _visualization(query, file_name='visualization'):
    """

    :param query: Cypher query.
    :param file_name: name for the output html file.
    :output: html file containing the visualization + opening of the file in the browser.
    """
    f = open(file_name + '.html', 'w')
    html_template = '''
    <html>
    <head>
        <title>DataViz</title>
        <style type="text/css">
            #viz {
                width: 1200px;
                height: 900px;
            }
        </style>
        <script src="''' + _NEOVIS_JS_VERSION + '''"></script>
    </head>   
    <script>
        function draw() {
            var config = {
                container_id: "viz",
                server_url: "''' + _LOGIN_INFO['uri'] + '''",
                server_user: "''' + _LOGIN_INFO['auth'][0] + '''",
                server_password: "''' + _LOGIN_INFO['auth'][1] + '''",
                labels: {
                    "SystemReq": {
                        caption: "type"
                    },
                    "HLR": {
                        caption: "type"
                    },
                    "LLR": {
                        caption: "type"
                    },
                    "Code": {
                        caption: "type"
                    },
                    "LLT": {
                        caption: "type"
                    },
                    "HLT": {
                        caption: "type"
                    },
                    "SystemTest": {
                        caption: "type"
                    },
                    "Bug": {
                        caption: "type"
                    },
                    "Verification": {
                        caption: "type"
                    }
                },
                relationships: {
                    "implements": {
                        caption: true,
                    },
                    "bugged": {
                        caption: true,
                    },
                    "verifies": {
                        caption: true,
                    },
                    "tests": {
                        caption: true,
                    }
                },
                arrows: true,
                initial_cypher: "''' + query + '''"
            }
            var viz = new NeoVis.default(config);
            viz.render();
            console.log(viz);
        }
    </script>
    <body onload="draw()">
        <div id="viz"></div>
    </body>
    </html>
    '''
    f.write(html_template)
    f.close()
    webbrowser.open(file_name + '.html')


def _reformat_results(result):
    """

    :param result: A cypher query transaction object.
    :return: Some form of representation of the returned data.
    """
    # TODO: switch results to the desired return format
    return result.data()


def Query(decorated=None, /, *, visualize=False, file_name='visualization'):
    """

    :param decorated: Used to indicate if the decorator was called with or without parameters .
    :param visualize: The value indicated if we will or will not call the visualization function on the query output.
    :param file_name: name for the output html file.
    :return: This is a decorator, Its main purpose is to get a function that returns a cypher query and execute it on the database.
    """

    def real_query(func):
        """

        :param func: the function we want to execute on its results.
        :return: A function that when executed will run it's result query on the database.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    with gd.driver(**_LOGIN_INFO) as data_base_connection:
                        with data_base_connection.session() as session:
                            cypher_query = ' '.join(func(*args, **kwargs).split())
                            result = _reformat_results(session.run(cypher_query))
                    break
                except neo4j.exceptions.ServiceUnavailable:
                    sleep(30)
            if visualize:
                _visualization(cypher_query, file_name)

            return result

        return wrapper

    if callable(decorated):
        return real_query(decorated)
    else:
        return real_query


@Query
def restsDatabase():
    """

    :return: Resets the database.
    """
    query = "Match (n) DETACH DELETE n"
    return query


@Query
def _createNode(node):
    """

    :param node: node to create.
    :return: Creates the node.
    """
    new_node = node.copy()
    if 'outgoing_links' in new_node:
        del new_node['outgoing_links']
    query = 'CREATE (node: ' + node['type'] + ' ' + _dictToStr(new_node) + ')'
    return query


@Query
def _createEdge(src, dst, relationship_type):
    """

    :param src: Src node.
    :param dst: Dst node.
    :param relationship_type: relashionship type 
    :return: Creates the relashionship.
    """
    query = "MATCH  (src), (dst) " \
            "WHERE src.id = '" + src + "' AND dst.id = '" + dst + "' " \
                                                                  "CREATE (src)-[e:" + _TYPE_DICT[
                relationship_type] + "]->(dst) " \
                                     "RETURN type(e)"
    return query


def _createEdges(node):
    """

    :param node: the entity to be linked.
    """
    if 'outgoing_links' in node:
        for link in node['outgoing_links']:
            _createEdge(node['id'], link, node['type'])


def initData(file_path):
    """

    :param file_path: a file path to the json input file.
    """
    with open(file_path) as f:
        data = json.load(f)
        restsDatabase()
        for node in data:
            _createNode(node)
        for node in data:
            _createEdges(node)


@Query(visualize=True, file_name='lookup_query')
def lookupObject(id):
    query = '''
            MATCH p=(n)-[*]-()
            WHERE n.id=''' "'" + str(id) + "'" + '''
            RETURN p
            '''
    return query


@Query
def unimplementedReq(node_type):
    query = '''
            MATCH (n:''' + node_type + ''')
            WHERE not (n)-[:implemented]->()
            RETURN n
            '''
    return query


@Query
def untestedReq(node_type):
    query = '''
            MATCH (n:''' + node_type + ''')
            WHERE not (n)<-[:tests]-()
            RETURN n
            '''
    return query


@Query
def unlinkedTests():
    query = '''
            MATCH (n)
            WHERE n.type in ['LLT','HLT','SystemTest']
            RETURN n
            '''
    return query


@Query
def completeSysReq():
    query = '''
            MATCH ()-[:tests]->(n:SysReq)<-[:verifies]-()
            WHERE (n)-[:implemented]->()
            RETURN n
            '''
    return query
