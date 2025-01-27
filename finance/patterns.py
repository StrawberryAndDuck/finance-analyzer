from finance.logger import logger


class SingletonInstance:
    __instance = None
    __tmp_method = None

    @classmethod
    def __getInstance(cls, *args, **kwagrs):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        """
        싱글톤 인스턴스는 특정 변수에 할당하지 않는 것이 좋다.
        ex)
        o1 = Obj.instance()
        o2 = Obj.clearInstance() 혹은 Obj.removeInstance()

        이후에도 o1 변수가 삭제를 시도한 인스턴스를 참조하고 있어 메모리에 남아있는 모습이 보인다.
        import sys
        sys.getrefcount(o1)  # 0이 아님 (0이 되어야 gc에 의에 메모리에서 해제된다.)
        """
        cls.__instance = cls(*args, **kwargs)
        cls.__tmp_method = cls.instance  # instance 메소드 포인터를 __tem_method 에 백업
        cls.instance = (
            cls.__getInstance
        )  # instance 메소드 포인터에 __getInstance 메소드 포인터로 대체 (instance 호출시 __getInstance 호출)
        logger.info(f"Singleton instance created: {cls.__instance}")
        return cls.__instance

    @classmethod
    def removeInstance(cls):
        """
        기존에 존재하던 인스턴스를 제거. instance()로 새로 호출해야함.
        :return:
        """
        if cls.__instance:
            cls.__instance = None  # 클래스 필드에 할당 되어 있는 인스턴스 제거
            cls.instance = cls.__tmp_method  # 백업해둔 메소드 포인터를 로드

    @classmethod
    def clearInstance(cls, *args, **kwargs):
        """
        기존에 존재하던 인스턴스를 제거하고 새로운 인스턴스를 반환한다.
        :param args:
        :param kwargs:
        :return:
        """
        if cls.__instance:
            obj = cls.__new__(cls)
            obj.__init__(*args, **kwargs)
            cls.__instance = obj
            cls.instance = cls.__getInstance
            return cls.__instance
