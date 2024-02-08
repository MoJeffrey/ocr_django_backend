import os
import time

import jpype

if __name__ == "__main__":
    path = os.getcwd()
    # 启动JVM
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", f"-Djava.class.path={path}/java/qrCodeIdentify.jar")
    ArrayList = jpype.JClass("java.util.ArrayList")
    # 导入Java类
    MyClass = jpype.JClass("QRCodeUtil")

    # 创建MyClass对象
    my_object = MyClass()

    data = """[Q100000023_1&42]{"method":"post","data":{"item2":"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.","item1":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi"""

    data_list = ArrayList()
    fileName_list = ArrayList()

    for i in range(100):
        data_list.add(data)
        fileName_list.add(f'{i}')

    time_start = time.time()
    b = my_object.generateQRCodeImage(data_list, fileName_list, f'{path}/img/', 300, 300)
    # 关闭JVM
    b = list(b)
    time_end = time.time()
    print(time_end - time_start)
    print(b)
    print(type(b))
    jpype.shutdownJVM()