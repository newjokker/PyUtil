# UtilUtil 说明


### 用到的包
* scikit_image
* scikit-learn
* cv2 ==> conda install -c menpo opencv3
* numpy
* PIL
* gdal
* matplotlib
* scipy
* 

### 自定义的符号
* a ==> b, b 为 a 的输出
* a --> b, b 为 a 的解释说明
* DS: data structure, 数据结构说明 
* need repair 后面跟的是需要完善的代码（最好设置为私有变量）

### 待做
* MappingPicture 增加主动添加图层的功能
* ShpToXml 增加过滤内容，当数据明显是错的，那就直接忽略掉，而不是报错
* ImgMatTiff 中增加图片中设置透明图层
* FTPUtil 增加判断 ftp 中是否存在此路径的方法
* MappingPicture 添加图层而不仅仅是修复图层

### v1.0.0
* 增加 LoadUtil 用于下载数据的模块
* 新增压缩模块 ZipUtil
* 将注释尽可能换成英文(去掉所有不需要的注释)，这样看起来协调一些，而且不会显得杂乱，还能避免以后的报错
* 重新开始版本，全部改为 Python3 版本的, 将所有的 函数内输出改为 logging 形式的

### v1.0.5
* 增加 AssistUtil 用于存放有待整理的函数
* 对整体代码进行了些微调整
* 使用 DbfUtil 替换 arcpy.da.SearchCursor
* 初步完善 DbfUtil 函数
* 初步完成分区分级统计
* 使用gdal完善分区统计
* 继续完善分区统计和分级统计
* 增加键盘控制相关类（KeyboardUtil）
* 增加自动创建图片（画图的类）等待完善
* 自动生成 legend 带着不同的色块，给分类 tiff 插入不同的颜色，完成自动的 mxd 生成（×）
* 完善单元测试示例
* 增加机器学习部分
* 增加爬虫项目，等待整理
* 将单独的类型检查模块迁移到 UtilUtil 中
* 以后每个模块都有一个自己的 readme.md，细节就不要往这个大的 readme.md 里面写了
* 完成 WordUtil 
* 增加内存管理相关内容
* 准备开始单元测试模块的完善
* 准备开始完善 WordUtil
* 出不了图，对图层进行金字塔的统计，【没有金字塔就没有统计，就不会有问题】 arcpy.BuildPyramidsandStatistics_management(rgb_path)
* 增加类型检查函数，用于检查输出的文件之类 TypeChecking
* 学习 numpy 中常用的函数
* mapping，新建文件保存文件夹，这样保存结果就能支持保存在特定的结构目录中去了，目录可以根据属性生成
* ImgMatTiff，中矩阵转换部分用更加合理的方法进行替换
* 开始使用 logging 全面替代 print
* 增加日志模块 LogUtil
* 增加装饰器模块，decorator,
* 完成 XmlUtil, 读 xml 的通用功能 get_info_from_node

### v1.0.4
* 使用 hasattr 优化 Maping 中 use_this_page 函数
* 使用过滤函数过滤需要出图的驱动页
* 拉伸到指定范围是有问题的们不能对修复的图层进行拉伸，还是需要获取传入的范围

### v1.0.3
* mapping 出图模块，找不到替换的数据就不进行替换 <--（貌似有问题就删除了这个功能）
* 出图模块增加缩放至指定图层的功能， zoom_to_assign_lyr 
* 完善 JsonUtil 和 PickleUtil
* 完善 JoList
* 新增 ReadData (1) PropertiesUtil (2) CsvUtil
* 新增 JoUtil 用于根据自己的想法重写 Python 自带的数据结构（有一些方法官方认为没必要也会有些问题所以没写，
我就是增加了这些功能，因为我将这些类的用户看做是能理解并懂得这些有缺陷方法带来问题的有经验的程序员）

### v1.0.2
* ftp_download 优化数据的下载，不能下载的资源及时释放
* ftp_download 下载数据时，判断保存文件夹是否存在，不存在新建

### v1.0.1
* MappingPicture 局部放大图可以是指定长宽，而不仅仅是指定边长
* ImgMatTiff 中增加 tiff_to_img_rgb， mat_to_img_rgb 两个函数，方便 rgb 真彩图的合成
* MappingPicture 使用 assign_extent 参数指定出图范围
* MappingPicture，修改参数 text_element_info 不赋值会报错的 bug
* 修复 FTPUtil 中 login 函数，增加 ip 登录功能


