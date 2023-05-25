import {systemState} from "@/system";


// eslint-disable-next-line no-unused-vars
class VirtualFileDatabase{
    files = [
        {
            path: "/example1/pa.txt",  //挂载路径（以绝对路径中最上层的分享文件夹为根目录）
            realPath: "D:/hat/example1/pa.txt",  //实际路径
            updateTime: 10254698,
            size: 1024,
            visible: ["admin", "guest", "*"],  //哪些权限组能看到该文件，*代表默认对全员开放
            userVisible: ["user1", "user2"],  //哪些用户能看到该文件，覆盖权限组设置
            userInvisible: ["user3", "user4"],  //哪些用户不能看到该文件，覆盖权限组设置和可见设置
            rules: [
                {
                    type: 0, //0 for Permission Group, 1 for User override
                    target: "guest",  //目标权限组/用户id
                    permission: "adxms" //权限字符串，权限参考文档
                },
                {
                    type: 1,  //User会覆盖Permission Group的设置
                    target: "user1",
                    permission: "*d-*-"  //*代表继承上一级设定的权限，-代表无权限
                }
            ]
        }
    ]
}