# general.run 保存配置并运行
# 传参 （例）,把children压平，参数只有一级
# #当用户对所有children param都没有填的时候，所有children param传给后端都是None，如果填了一个，则另一个每天的由None改为default值，yaml里没写default的default都为None
{
    "uuid": "2b2133b6dc4d46bf815259bd61fad38d",
    "type": "videoEditor",
    "inFile": "C:/Users/yiyun.zy/Desktop/xuelangyun/moviepyset/sample1.mp4",
    "saveFile":"out.mp4",
    "subclipStart": 10,
    "subclipEnd": 20
}
# 返回
点run的时候就会不断生成进度百分比，等着按“查看进度”按钮是给展示出来

# "general.stop" 停止运行
# 传参
{
    "uuid": "2b2133b6dc4d46bf815259bd61fad38d"
}
# 返回
null

# general.checkStatus 查看进度
# 传参
{
    "uuid": "2b2133b6dc4d46bf815259bd61fad38d"
}
# 返回
不断emit的进度条百分比
