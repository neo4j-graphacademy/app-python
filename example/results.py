# Import the Driver
from neo4j import GraphDatabase

# Create a Driver instance
driver = GraphDatabase.driver("neo4j://localhost:7687",
    auth=("neo4j", "neo"))

# Verify Connectivity
# driver.verify_connectivity()

# tag::get_actors[]
# tag::get_actors_unit_of_work[]
# Unit of work
def get_actors(tx, movie): # <1>
    result = tx.run("""
        MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: $title})
        RETURN p
    """, title=movie)

    # tag::get_actor_nodes[]
    # Access the `p` value from each record
    return [ record["p"] for record in result ]
    # end::get_actor_nodes[]
    # end::get_actors_unit_of_work[]

# Open a Session
with driver.session() as session:
    # Run the unit of work within a Read Transaction
    actors = session.execute_read(get_actors, movie="The Green Mile") # <2>

    for record in actors:
        print(record["p"])

    session.close()
# end::get_actors[]

def get_actors_iterate(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[r:ACTED_IN]->(:Movie {title: $title})
        RETURN p, r.roles AS roles
    """, title=movie)

    # tag::keys[]
    # Get all keys available in the result
    print(result.keys()) # ["p", "roles"]
    # end::keys[]

    # tag::peek[]
    # Check the first record without consuming it
    peek = result.peek()
    print(peek)
    # end::peek[]


    # Get the next record
    first = result.single()

    # tag::record_keys[]
    # Get the keys available in the record
    first.keys()
    # ['p', 'roles]
    # end::record_keys[]

    # Get a value or retun the default value
    first.get("roles", default="Unknown")

    # tag::for[]
    for record in result:
        print(record["p"]) # Person Node
    # end::for[]


"""
Consume the remainder of this result and return a ResultSummary.
"""
# tag::consume[]
def get_actors_consume(tx, name):
    result = tx.run("""
        MERGE (p:Person {name: $name})
        RETURN p
    """, name=name)

    info = result.consume()
    # end::consume[]

    # tag::times[]
    # The time it took for the server to have the result available. (milliseconds)
    print(info.result_available_after)

    # The time it took for the server to consume the result. (milliseconds)
    print(info.result_consumed_after)
    # end::times[]

    # tag::counters[]
    print("{0} nodes created".format(info.counters.nodes_created))
    print("{0} properties set".format(info.counters.properties_set))
    # end::counters[]

    return info

"""
Obtain the next and only remaining record from this result if available
else return None. Calling this method always exhausts the result.

A warning is generated if more than one record is available but the
first of these is still returned.
"""
# tag::single[]
def get_actors_single(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: $title})
        RETURN p
    """, title=movie)

    return result.single()
# end::single[]

"""
Obtain the next record from this result without consuming it. This
leaves the record in the buffer for further processing.
"""
def get_actors_peek(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: $title})
        RETURN p
    """, title=movie)

    # Check the first record without consuming it
    peek = result.peek()
    print(peek)

    return result.values()


"""
Return a Graph instance containing all the graph objects in the result.
After calling this method, the result becomes detached, buffering all
remaining records.

A graph is a local, self-contained graph object that acts as a container
for Node and Relationship instances.
"""
# tag::graph[]
def get_actors_graph(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: $title})
        RETURN p, r, m
    """, title=movie)

    return result.graph()
# end::graph[]


"""
value(key=0, default=None)
Helper function that return the remainder of the result as a list of values.
"""
# tag::value[]
def get_actors_values(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: $title})
        RETURN p.name AS name, m.title AS title, r.roles AS roles
    """, title=movie)

    return result.value("name", False)
    # Returns the `name` value, or False if unavailable

# end::value[]

"""
values(*keys)
Helper function that return the remainder of the result as a list of values lists.
"""
# tag::values[]
def get_actors_values(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: $title})
        RETURN p.name AS name, m.title AS title, r.roles AS roles
    """, title=movie)

    return result.values("name", "title", "roles")

# end::values[]

"""
Helper function that return the remainder of the result as a list of dictionaries.
"""
# tag::data[]
def get_actors_data(tx, movie):
    result = tx.run("""
        MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: $title})
        RETURN p.name AS name, m.title AS title, r.roles AS roles
    """, title=movie)

    return result.data("name", "title", "roles")
# end::data[]


def get_node_example(tx, movie):
    # tag::run[]
    result = tx.run("""
    MATCH path = (person:Person)-[actedIn:ACTED_IN]->(movie:Movie {title: $title})
    RETURN path, person, actedIn, movie
    """, title=movie)
    # end::run[]

    # tag::node[]
    for record in result:
        node = record["movie"]
        # end::node[]

        # tag::node_info[]

        print(node.id)              # <1>
        print(node.labels)          # <2>
        print(node.items())         # <3>

        # <4>
        print(node["name"])
        print(node.get("name", "N/A"))
        # end::node_info[]

        # tag::rel[]
        acted_in = record["actedIn"]

        print(acted_in.id)         # <1>
        print(acted_in.type)       # <2>
        print(acted_in.items())    # <3>

        # 4
        print(acted_in["roles"])
        print(acted_in.get("roles", "(Unknown)"))

        print(acted_in.start_node) # <5>
        print(acted_in.end_node)   # <6>
        # end::rel[]

        # tag::path[]
        path = record["path"]

        print(path.start_node)  # <1>
        print(path.end_node)    # <2>
        print(len(path))  # <1>
        print(path.relationships)  # <1>
        # end::path[]

        # tag::segments[]
        for rel in iter(path):
            print(rel.type)
            print(rel.start_node)
            print(rel.end_node)
        # end::segments[]


def temporal():
    year = 2018
    month = 4
    day = 30
    hour = 12
    minute = 34
    second = 56
    nanosecond = 789123456

    # tag::temporal[]
    # Create a DateTime instance using individual values
    datetime = neo4j.time.DateTime(year, month, day, hour, minute, second, nanosecond)

    #  Create a DateTime  a time stamp (seconds since unix epoch).
    from_timestamp = neo4j.time.DateTime(1609459200000) # 2021-01-01

    # Get the current date and time.
    now = neo4j.time.DateTime.now()

    print(now.year) # 2022


    # end::temporal[]
