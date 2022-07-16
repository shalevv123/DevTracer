import DevTracer as dt


@dt.Query
def no_vis_example():

    query = '''
            MATCH (n:HLR)
            WHERE n.req_type = 'functional' AND not (:Sysreq)-[]->(n)
            RETURN n
            '''
    return query


@dt.Query(visualize=True, file_name='example_query')
def vis_example():

    query = '''
            MATCH p=(:LLR)-[:implemented]->(c:code)<-[:bugs]-()
            RETURN p
            '''
    return query


def main():
    # dt.initData("ExampleData.json")
    dt.lookupObject("MY-SDD-25021")
    # print(dt.unimplementedReq("HLR"))
    # print(dt.untestedReq("LLR"))
    # print(dt.unlinkedTests())
    # print(dt.completeSysReq())
    # print(no_vis_example())
    vis_example()
    pass


if __name__ == "__main__":
    main()
