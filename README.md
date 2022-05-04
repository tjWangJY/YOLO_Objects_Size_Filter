_**YOLO格式数据集目标尺寸过滤器**_

_**YOLO_Objects_Size_Filter**_

###### Author:wjy      
###### Latest Update:20220504

**功能：**

将YOLO数据集中，含小（或大）目标的数据提取出来，作为新的数据集

**使用方法：**

运行前设置参数（均位于main.py开头处），

包括：小（大）目标的定义、图片格式、需要的目标类型、数据源地址、保存路径。

小（大）目标定义：`small = 32   large = 96`
这两个参数，默认为长宽均小于32像素为小目标，均大于96像素为大目标

图片格式：`image_type = 'jpg'`

需要的目标类型：`want_which_objects = 'small'`单次输出的目标类型，small即为带有小目标的数据。
medium指不包含任何小、大目标的数据

数据源地址与保存路径于下方代码defalut参数处修改：

`   parser.add_argument('--images', type=str,
                        default='F:/Dataset/Helmet/Hardhat/Train/JPEGImage',
                        help='images path, must be applied to labels')
    parser.add_argument('--labels', type=str,
                        default='F:/Dataset/Helmet/Hardhat/Train/labels' ,
                        help='labels path, must be applied to images')
    parser.add_argument('--spath', type=str,
                        default='F:/wjy/small_ob',
                        help='save path of the filtered dataset')
`