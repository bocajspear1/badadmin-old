import depends

# sand
# Lumberyard
# Factory
# Wood
# Stone
# Windows
# House
# 

depends.add_module({"name": "melter"}, [{"name": "coal"},{"name": "match"}])
depends.add_module({"name": "quarry"}, [{"name": "wood"}])
depends.add_module({"name": "house"},[{"name": "wood"}, {"name": "stone"}, {"name": "windows"}])
depends.add_module({"name": "match"},[{"name": "wood"}, {"name": "sulfer"}])
depends.add_module({"name": "wood"},[{"name": "lumberyard"}])
depends.add_module({"name": "stone"},[{"name": "quarry"}])
depends.add_module({"name": "windows"}, [{"name": "factory"}])
depends.add_module({"name": "factory"}, [{"name": "sand"}, {"name": "melter"}])


#depends.add_module({"name": "wood"}, [{"name": "stone"}])

print ()

print("Result: ", depends.start_resolve())