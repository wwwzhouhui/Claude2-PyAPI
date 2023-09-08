import pickle

class IDStorage:
    def __init__(self):
        self.id = None

    def get_id(self):
        if self.id is None:
            try:
                with open('../id.pickle', 'rb') as f:
                    self.id = pickle.load(f)
            except FileNotFoundError:
                print("No ID found. Creating new ID")
        return self.id

    def set_id(self,id):
        self.id = id
        with open('../id.pickle', 'wb') as f:
            pickle.dump(self.id, f)

# 测试代码
storage = IDStorage()

# 第一次调用get_id，会生成新的ID并保存到文件
id_value = storage.get_id()
storage.set_id("sssss")
#id_value = storage.get_id()
if id_value is not None:
    print("dddddD")
else:
    print(id_value)
#
# # 第二次调用get_id，会从文件中读取已有的ID
# id_value = storage.get_id()
# print(id_value)
#
# # 修改ID并保存到文件
# import uuid
# conversation_id = str(uuid.uuid4())
# storage.set_id(conversation_id)
# id_value = storage.get_id()
# print(id_value)

