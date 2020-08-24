"""For generating id in opengl"""


class GenId:
    vertex_attr_point = 0
    vertex_attr_point_dict = dict()

    some_counter = 0
    some_dict = dict()

    @classmethod
    def get_id_to_obj(cls, obj, dictionary: dict, name_of_counter: str):
        value = dictionary.get(obj)
        if value is None:
            value = getattr(cls, name_of_counter)
            dictionary[obj] = value
            setattr(cls, name_of_counter, value + 1)
        return value

    @classmethod
    def get_vert_attr_p_id(cls, obj):
        """Vertex attribute pointer id"""
        return cls.get_id_to_obj(obj, cls.vertex_attr_point_dict, "vertex_attr_point")

    @classmethod
    def get_some_value(cls, obj):
        """Just test"""
        return cls.get_id_to_obj(obj, cls.some_dict, "some_counter")
