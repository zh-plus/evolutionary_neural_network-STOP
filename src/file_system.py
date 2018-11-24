import architecture_pb2
import os
import pickle


class Folder:
    def __init__(self, path):
        self.path = path
        self.history = []
        self.max_id = 0

        dirs = os.listdir(self.dead_path())
        for file in dirs:
            if file[0:1] == 'nn':
                self.history.append(file)

        dirs = os.listdir(path)
        for file in dirs:
            if file[0:2] == 'nn':
                self.history.append(file)
                if self.file_id(file) > self.max_id:
                    self.max_id = self.file_id(file)

    def dead_path(self):
        return os.path.join(self.path, 'dead')

    def file_path(self, file):
        return os.path.join(self.path, file)

    def create_file(self, arch_proto):
        file_name = 'nn-'+str(arch_proto.id)+'-alive'
        self.history.append(file_name)
        file_path = os.path.join(self.path, file_name)
        write_file(arch_proto, file_path)
        if arch_proto.id > self.max_id:
            self.max_id = arch_proto.id
        print("create file ", file_name, " ...")

    def dead(self, arch):
        # change file name -alive to -dead
        src = 'nn-'+str(arch.id)+'-alive'
        dst = 'nn-'+str(arch.id)+'-dead'
        src_path = os.path.join(self.path, src)
        dst_path = os.path.join(self.dead_path(), dst)
        os.remove(src_path)
        write_file(arch.to_proto(), dst_path)
        print(self.file_name(arch), "is dead")

    def add(self, arch):
        src = 'nn-'+str(arch.id)+'-alive'
        self.history.append(src)
        if arch.id > self.max_id:
            self.max_id = arch.id
        file_path = os.path.join(self.path, src)
        write_file(arch.to_proto(), file_path)
        print("add", src, 'successfully')

    @staticmethod
    def file_name(arch):
        return 'nn-'+str(arch.id)+'-alive'

    @staticmethod
    def alive(file):
        name = file.split('-')
        if name[2] == 'alive':
            return True
        return False

    @staticmethod
    def file_id(file):
        name = file.split('-')
        return int(name[1])


def load_path():
    f = open('path.pickle', 'rb')  # open last visited path
    path = pickle.load(f)
    f.close()
    return path


def save_path(path):
    f = open('path.pickle', 'wb')  # b:一定要以二进制的方式打开
    pickle.dump(path, f)
    f.close()


def write_file(arch_proto, path):
    # write protocol buffer form to a file
    f = open(path, "wb")
    f.write(arch_proto.SerializeToString())
    f.close()


def read_file(path):
    # read architecture from a file
    f = open(path, "rb")
    read = architecture_pb2.ArchProto()
    read.ParseFromString(f.read())
    f.close()
    return read


def test_dir(path):
    while not os.path.isdir(path):
        print("The path is unavailable!")
        path = input("Please choose a new path: ")
    save_path(path)

    dead_path = os.path.join(path, 'dead')
    if not os.path.isdir(dead_path):
        os.mkdir(dead_path)

    return path




