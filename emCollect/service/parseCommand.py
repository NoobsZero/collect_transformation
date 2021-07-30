import sys
import getopt
import logging

MODULE_TYPE_TF = "TF"

MODULE_TYPE_NAME = [MODULE_TYPE_TF]


class TransForm(object):
    __instance = None

    def __init__(self):
        if not self.__instance:
            self.data_type = ""
            self.data_path = ""
            self.img_path = ""
            self.local_path = "./result"
            self.coco_img_path = ""
            self.logLevel = logging.INFO

    @classmethod
    def get_TransForm(cls):
        """
            单例模式（懒汉模式）
            调用get_instance类方法的时候才会生成UnCompress实例
        :return: TransForm
        """
        if not cls.__instance:
            cls.__instance = TransForm()
        return cls.__instance


def UseAge():
    """
        使用帮助信息
    Returns:
        pass
    """
    print("")
    print("USEAGE:")
    print("\t-h help\t\t\t: 帮助信息 \n"
          "\t-m module [TF]\t\t\t TF:old标注工具json或xml文件转为CVAT格式下的COCO数据格式 \n"
          "\t-y type\t\t\t: 数据类型[json,xml] \n"
          "\t--data_path\t\t\t: 数据存储目录 \n"
          "\t--img_path\t\t\t: 图片存储目录 \n"
          "\t--local_path\t\t\t: 结果目录 \n"
          "\t--coco_img_path\t\t\t: coco目錄 \n"
          "     \tpython3 emCollect [-h] [-m] [-t] [--data_path] [--img_path] [--local_path] [--coco_img_path]\n"
          " ")
    print("\t")
    print("")


class ReadCommandParameter:
    def __init__(self):
        """
            读取命令参数
            logLevel 日志级别（默认INFO）
            sourceStr
        """
        self.moduleType = ""
        self.module = None
        self.logLevel = logging.INFO

    def parseCommandArgs(self, argv):
        """
            解析命令参数（功能定义）
        Args:
            argv: 命令参数
                -h 帮助信息

        Returns: self

        """
        try:
            opts, args = getopt.getopt(argv, "hm:t:", ["help", "module=", "type=", "isDebug",
                                                       "data_path=", "img_path=", "local_path=", "coco_img_path="])
        except getopt.GetoptError:
            UseAge()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                UseAge()
                sys.exit()
            elif opt in ('-m', '--module'):
                self.moduleType = arg
                if self.moduleType not in MODULE_TYPE_NAME:
                    UseAge()
                    print("moduleType[{}] is not in {}".format(opt, MODULE_TYPE_NAME))
                    sys.exit(1)
            elif opt == "--isDebug":
                self.logLevel = logging.DEBUG
            elif self.moduleType == MODULE_TYPE_TF:
                self.module = TransForm.get_TransForm()
                if opt in ('-t', '--type'):
                    if arg in ['json', 'xml']:
                        self.module.data_type = arg
                    else:
                        UseAge()
                        print("TransForm.data_type[{}] is not in {}".format(opt, ['json', 'xml']))
                        sys.exit(1)
                elif opt == "--data_path":
                    self.module.data_path = arg
                elif opt == "--img_path":
                    self.module.img_path = arg
                elif opt == "--local_path":
                    self.module.local_path = arg
                elif opt == "--coco_img_path":
                    self.module.coco_img_path = arg
        self.printInputMessage()
        self.module.logLevel = self.logLevel
        return self.module

    def printInputMessage(self):
        print(self.__dict__)
