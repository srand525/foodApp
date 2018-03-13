"MATCH (c1:component {name: 'sauteed kale'}), 
(c2:component {name: 'sauteed onion and garlic'}),(i:ingredient {name:'kale'})


CREATE (c1)-[:includes]->(c2) CREATE (c1)-[:includes]->(i)"


match (c:component {name:'sofrito'}), (i:ingredient {name:'onion'})
create (c)=[:includes]->[i]


MATCH (n1:Node {id:$id1})
MATCH (n2:Node) WHERE n2.ids IN $ids
CREATE (n1)-[:REL]->(n2)

match (c:component {name:'sofrito'})


create (c:component {name: 'sofrito'}) - [r:includes] -> (i:ingredient {name:'garlic'})


match (c:component {name:'sofrito'})
match (i:ingredient) where i.name in ['garlic']
create (c)-[:includes]->(i2:ingredient {name:'red_pepper'})

match (c:component {name:'sofrito'})
match (i:ingredient) where i.name in ['garlic']
match p = (c)-[:includes]->(i2:ingredient {name:'red_pepper'})
delete p


match p = (c:component {name:'sofrito'})-[:includes]->(i2:ingredient {name:'red_pepper'})
delete p

match (i:ingredient {name:'red_pepper'})
match p = (c:component {name:'sofrito'}) -[i:includes]->(i2:ingredient {name:'red_pepper'})
delete i

below creates a relationship betwen sofrito and shallot 
merge (i:ingredient {name:'shallot'})
match (c:component {name:'sofrito'})
match (i:ingredient {name:'shallot'})
create p = (c) -[r:includes]->(i)

