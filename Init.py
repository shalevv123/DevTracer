import numpy as np
import pandas as pd
from neo4j import GraphDatabase as gd

project_id = [i for i in range(1,10001)]
team_id = [i for i in range(1,501)]
bug_id = [i for i in range(1,11)]

execution_commands = []

for bid in bug_id:
    neo4j_create_statemenet = "CREATE (b:Bug {bug_id:" + str(bid) + "})"
    execution_commands.append(neo4j_create_statemenet)

for tid in team_id:
    neo4j_create_statemenet = "CREATE (t:Team {team_id:" + str(tid) + "})"
    execution_commands.append(neo4j_create_statemenet)

for pid in project_id:
    neo4j_create_statemenet = "CREATE (p:Project {project_id:" + str(pid) + "})"
    execution_commands.append(neo4j_create_statemenet)

    tid = np.random.randint(low=1,high=len(team_id)+1)
    neo4j_create_statemenet = "MATCH  (p:Project), (t:Team) " \
                              "WHERE p.project_id = "+str(pid)+" AND t.team_id = "+str(tid)+" " \
                              "CREATE (p)-[m:Managed]->(t) " \
                              "RETURN type(m)"
    execution_commands.append(neo4j_create_statemenet)

    rand = np.random.randint(30)
    if not rand:
        bid = np.random.randint(low=1,high=len(bug_id)+1)
        neo4j_create_statemenet = "MATCH  (p:Project), (b:Bug) " \
                                  "WHERE p.project_id = " + str(pid) + " AND b.bug_id = " + str(bid) + " " \
                                  "CREATE (p)-[bu:Bugged]->(b) " \
                                  "RETURN type(bu)"

        execution_commands.append(neo4j_create_statemenet)





def execute_transactions(execution_commands):
    data_base_connection = gd.driver(uri="bolt://localhost:7687", auth=("neo4j", "nobugshere"))
    session = data_base_connection.session()
    for i in execution_commands:
        session.run(i)

def hardReset():
    data_base_connection = gd.driver(uri="bolt://localhost:7687", auth=("neo4j", "nobugshere"))
    session = data_base_connection.session()
    session.run("Match (n) DETACH DELETE n")


hardReset()
execute_transactions(execution_commands)



