"""
Entities defined in this module

One entity object represents a row of one of the tables of the database, in the program:
    i.e: All data that would be stored in the database is encapsulated in entities when it has to exist in RAM

Entities are responsible for data validation, which means that data encapsulated in an entity is considered to be
valid. This means that data that is to be validated should be passed to the entity through a setter which validates it

Entities must have __slots__ which hold the column names of the table it belongs. Elements of __slots__ must have the
exact same name as the column of the table. This is because the repos use slots to perform queries.

"""
pass
