= Building Neo4j Applications with Python

> Learn how to interact with Neo4j from Python using the Neo4j Python Driver

This repository accompanies the link:https://graphacademy.neo4j.com/courses/app-python/[Building Neo4j Applications with Python course^] on link:https://graphacademy.neo4j.com/[Neo4j GraphAcademy^].

For a complete walkthrough of this repository,  link:https://graphacademy.neo4j.com/courses/app-python/[enrol now^].

== A Note on comments

You may spot a number of comments in this repository that look a little like this:

[source,python]
----
# tag::something[]
someCode()
# end::something[]
----


We use link:https://asciidoc-py.github.io/index.html[Asciidoc^] to author our courses.
Using these tags means that we can use a macro to include portions of code directly into the course itself.

From the point of view of the course, you can go ahead and ignore them.


== Setting up your environment

[source,sh]
----
python -m venv neoflix

source neoflix/bin/activate
----



== Running the Application

[source,sh]
export FLASK_APP=api
export FLASK_ENV=development
flask run

