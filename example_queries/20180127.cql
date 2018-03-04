create (Tara:Crew {name:'Tara'}), 
(Sophie:Crew {name:'Sophie'}), (Tara)-[k:KNOWS]->(Sophie),(Tara)-[:k]->(Neo)



create (Tahini_Sauce: Component {name: 'Tahini Sauce'}), (Tahini: Ingredient {name: 'Tahini'}), 
(Lemon_Juice: Ingredient {name: 'Lemon Juice'})
(Tahini_Sauce)-[i:includes]->(Tahini), (Tahini_Sauce)-[:i]->(Lemon_Juice)


create (Tara:Crew {name:'Tara'}), 
(Sophie:Crew {name:'Sophie'}), (Tara)-[:IS_BESTIES_WITH {boolean_test:TRUE}]->(Sophie)


//return all things who are friends with a crew node, showing the node, realtionships and the things
match (n:Crew)-[r:IS_BESTIES_WITH]-(m) where r.boolean_test return n,r,m

//return all things who are friends with a crew node 
match (n:Crew)-[r:IS_BESTIES_WITH]-(m) where r.boolean_test return n

match (n:Crew)-[r:IS_BESTIES_WITH]->(m) where r.boolean_test return n as n,r,m