
# astropy库fits模块读取FITS文件
# 参考翻译自：https://docs.astropy.org/en/stable/io/fits/index.html
# 用 # 标注的主要是我对代码的注释
# 用 ''' ''' 包围的主要是官方的说明和代码对应的输出结果
# 这两种标记都是用来说明的
#-------------导入库---------------

# 将astropy.io这个库导入并用‘fits’指代，‘fits’换成其他名字也是莫得问题的
from astropy.io import fits  


#-------------打开文件---------------

# 这个方法可以直接在线调用官方的示例图片,这里用不上，注释掉
# fits_image_filename = fits.util.get_testdata_filepath('test0.fits')  

# 我的本地FITS文件的文件名字符串赋给一个变量，方便后面调用
fits_image_filename = 'aia.lev1.2018-05-29T185610Z.172929830.image_lev1.fits'   
# 调用astropy.io.open()打开文件，这里终端打开的文件夹就是图片所在位置，所以直接调用文件名就可以打开
# 也可以使用如下的open()参数，mode='update'，实时更新
'''代码示例
with fits.open('original.fits', mode='update') as hdul:
    # Change something in hdul.
    # 对hdul做些修改
    hdul.flush()  # 把修改保存到原文件 changes are written back to original.fits
# 关闭文件将会保存修改，并阻止后面的写入
# closing the file will also flush any changes and prevent further writing
'''
# 默认是'只读'模式读取文件
hdul = fits.open(fits_image_filename) 

# 这里提供了另一种方式来读取文件
# with层级下的代码执行完后，会自动回收，也就可以直接关闭文件了
'''代码示例
with fits.open(fits_image_filename) as hdul:
     hdul.info()
     ···
'''

print(type(hdul))
'''输出结果
<class 'astropy.io.fits.hdu.hdulist.HDUList'>
'''

#-------------读取文件--------------
''' [HDUList的说明]
hdul是一个HDUList对象，即一个看起来像列表的 HDU 对象的集合. 
an HDUList which is a list-like collection of HDU objects.

HDU (Header Data Unit，头部数据集合) 是FITS文件构造中最高层级部分,
is the highest level component of the FITS file structure, 

由头部数据和数据矩阵或者是数据表组成。
consisting of a header and (typically) a data array or table.
'''
# 调用HDUList.info()方法来查看文件概况
hdul.info()
'''输出结果
Filename: aia.lev1.2018-05-29T185610Z.172929830.image_lev1.fits
No.    Name      Ver    Type      Cards   Dimensions   Format
  0  PRIMARY       1 PrimaryHDU       6   ()
  1                1 CompImageHDU    190   (4096, 4096)   int16
'''
# 可见这个文件包含有两个HDU数据集，索引号为0的那个HDU，有六个说明用的Cards
# 维度为空，所以初步推断是文件的说明部分。
# 索引号为1的那个HDU，有190个Cards,说明含有很多参数
# 维度为(4096,4096),数据类型为int16，这应该就是我们想要的太阳的图片数据了
# 而且Type属性也说了第二个HDU是CompImageHDU，石锤。



# astropy.io.open()还可以注入其他参数实现一些其他的功能
# 比如lazy_load_hdus参数，若设为'True'，文件被close()后还可以读取，数据的头部数据
'''代码示例
hdul = fits.open(fits_image_filename,lazy_load_hdus=False) 
'''

# 导入大文件时，memmap参数，可以通过内存映射的方式而不一次性把文件载入内存
# 默认为'True'，不过有一个问题就是文件close()后，可能还有残留的读取句柄在读取文件
# 参考：https://docs.astropy.org/en/stable/io/fits/index.html#working-with-large-files
'''代码示例
hdul = fits.open(fits_image_filename,memmap=True) 
'''

# FITS采用的是Fortran的风格的类型系统，不支持无符号的整数数据
# astropy导入FITS文件会自动转换有符号的整数数据为无符号的整数数据，uint=False参数来控制
# 参考：https://docs.astropy.org/en/stable/io/fits/index.html#unsigned-integers
''' 代码示例
hdul = fits.open(fits_image_filename,uint=False) 
'''

# astropy的open()可以无障碍地打开gzip，bzip2，pkzip等压缩的FITS文件
# 不过不同格式，有一些不同的限制。对于zip，open方法只会打开压缩包里的第一个FITS文件
# 对于bzip2则不支持使用append和update模式来open。

# 调用第一个头部数据集(HDU)的头部数据中的'COMMENT'这个Card的数据
# 也可以使用索引号，hdul[0].header[4] ，不建议使用，不同文件的特定关键字位置不一样
hdul[0].header['COMMENT']
'''输出结果
FITS (Flexible Image Transport System) format is defined in 'Astronomy
and Astrophysics', volume 376, page 359; bibcode: 2001A&A...376..359H
'''
hdul[0].header[4]
'''输出结果
FITS (Flexible Image Transport System) format is defined in 'Astronomy
'''

# 修改FITS文件，内置了一个评论和历史记录系统，也有些意思
# 参考：https://docs.astropy.org/en/stable/io/fits/index.html#working-with-fits-headers
# 将header传给hdr，方便后面修改属性，添加了一条历史记录和一条评论
hdr = hdul[0].header
'''代码示例，这里注释掉，我已经添加过了，就不再添加了
hdr['history'] = 'YuanZ1949 changed this file on 2020.6.12'
hdr['comment'] = 'Thanks STEM, I am very happy to know the power of sun.'
'''
hdr  
# print(repr(hdr)) # 这个也可以
'''输出结果
SIMPLE  =                    T / file does conform to FITS standard
BITPIX  =                   16 / number of bits per data pixel
NAXIS   =                    0 / number of data axes
EXTEND  =                    T / FITS dataset may contain extensions
COMMENT   FITS (Flexible Image Transport System) format is defined in 'Astronomy
COMMENT   and Astrophysics', volume 376, page 359; bibcode: 2001A&A...376..359H
COMMENT Thanks STEM, I am very happy to know the power of sun.
HISTORY YuanZ1949 changed this file on 2020.6.12
'''

'''代码示例，修改其他属性
hdr = hdul[0].header

hdr.set('observer', 'Edwin Hubble')

hdr['targname'] = ('NGC121-a', 'the observation target')
hdr.comments['targname']
'''

hdr[:2]
'''输出结果
SIMPLE  =                    T / file does conform to FITS standard     
BITPIX  =                   16 / number of bits per data pixel  
'''
list(hdr.keys())  
'''输出结果
['SIMPLE',
 'BITPIX',
 'NAXIS',
 'EXTEND',
 'COMMENT',
 'COMMENT',
 'COMMENT',
 'HISTORY']
'''

# 如果读取的FIST文件不是非常标准的FIST文件(这是常有的事)
# 那可以使用fix工具尝试修复(仅限比较无关的差异)
'''读取报错时的输出
VerifyError: Unparsable card (OSCNMEAN), fix it first with .verify('fix').
'''
# 修复代码
hdul[1].verify('fix')
'''输出结果
WARNING: VerifyWarning: Verification reported errors: [astropy.io.fits.verify]
WARNING: VerifyWarning: Card 68: [astropy.io.fits.verify]
WARNING: VerifyWarning:     Card 'OSCNMEAN' is not FITS standard (invalid value string: '-nan').  Fixed 'OSCNMEAN' card to meet the FITS standard. [astropy.io.fits.verify]
WARNING: VerifyWarning: Card 69: [astropy.io.fits.verify]
WARNING: VerifyWarning:     Card 'OSCNRMS' is not FITS standard (invalid value string: '-nan').  Fixed 'OSCNRMS' card to meet the FITS standard. [astropy.io.fits.verify]
WARNING: VerifyWarning: Note: astropy.io.fits uses zero-based indexing.
 [astropy.io.fits.verify]
'''
# 读取带有图片数据的第二个HDU(hdul[1])的数据部分(.data)
data = hdul[1].data
# 还可以使用name来索引hdu，但是我们的文件里第二个HDU没有这个属性，就不用了
'''代码示例
data = hdul['某个name值'].data
data = hdul['某个name值',2].data  # 同名name的第二个HDU
'''

# 获取数据矩阵大小
data.shape
'''输出结果
(4096, 4096)
'''
# 数据的类型
data.dtype.name
'''输出结果
'int16'
'''

# 可以看出是numpy类型，那么就可以随意分割，查看，数学运算
type(data)
'''输出结果
numpy.ndarray
'''

# 取值,取指定行列的数据的值
print(data[1, 4])
'''输出结果
0
'''

# 切片,截取数据的一部分输出出来
data[30:40, 10:20]
'''输出结果
array([[ 0,  3,  0,  0, -2,  0,  1,  0,  0, -1],
       [ 0,  0, -1, -1,  1, -1,  0,  1, -1,  1],
       [ 0, -1, -1, -1,  0,  0, -1,  1, -1, -1],
       [-1,  0,  0,  0, -2,  2,  0,  0, -2,  0],
       [ 1,  0, -2,  1,  0,  0,  0,  1, -1, -1],
       [-2, -1,  0, -1, -1, -2, -1,  0, -1, -1],
       [ 0, -1, -2,  0,  0, -1,  0,  1, -1,  1],
       [-3,  1,  0,  1,  1,  1, -1, -1, -2,  1],
       [ 0, -2, -2, -1,  0, -2,  1,  1,  1,  1],
       [ 0, -1, -1, -2,  0,  1,  1,  0,  2,  0]], dtype=int16)
'''
# The next example of array manipulation is to convert the image data from counts to flux:
'''不太懂的一个操作，可能是特殊图片的处理
photflam = hdul[1].header['photflam']
exptime = hdr['exptime']
data = data * photflam / exptime
hdul.close()
'''

# Table数据处理(那种每个数据点是个元组的FITS文件)
# 参考：https://docs.astropy.org/en/stable/io/fits/index.html#working-with-table-data
# 暂且略过

# 保存文件更改，调用HDUList.writeto() 方法保存
'''代码示例:#这里注释掉,我下载的hdul不规范,无法保存
hdul.writeto('newtable.fits')
'''

# 读完数据自然要关掉文件，调用close()即可
hdul.close()
# 上面把图像数据赋值给了`data`这个变量，并演示了矩阵的一些处理函数
# 下面就开始处理`data`

# 参考文章:https://blog.csdn.net/qq_37274615/article/details/79159468
# 导入matplotlib绘图库
from matplotlib import image
 # 调用图片保存函数直接将数组储存为图片
image.imsave('FITS-image-out.png', data)

'''imsave函数的构造
def imsave(fname, arr, vmin=None, vmax=None, cmap=None, format=None,
           origin=None, dpi=100):
    #Save an array as an image file.
'''

# 导入pyplot库,取plt做别名
from matplotlib import pyplot as plt
#plt绘制data
plt.imshow(data)
#plt显示绘制结果
plt.show()

'''imshow()函数的构造
def imshow(
        X, cmap=None, norm=None, aspect=None, interpolation=None,
        alpha=None, vmin=None, vmax=None, origin=None, extent=None,
        shape=cbook.deprecation._deprecated_parameter, filternorm=1,
        filterrad=4.0, imlim=cbook.deprecation._deprecated_parameter,
        resample=None, url=None, *, data=None, **kwargs):
'''

# 导入opencv库
import cv2
# 保存data
cv2.imwrite("FITS-cv2-out.png", data)
