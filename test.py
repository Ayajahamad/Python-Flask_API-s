items_db = [
               {
                   id:1,
                   'name':'abc'
                },
                {
                   id:2,
                   'name':'def'
                },
                {
                   id:3,
                   'name':'abc'
                }
           ]
up = {id:1,'name':'zxc'}
item_id = 1
bd_ite = next((i for i in items_db if i[id] == item_id),None)

print(bd_ite)
items_db.remove(bd_ite)
print(items_db)
