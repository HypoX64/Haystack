- [1 基础知识](#1-基础知识)
  - [1.1 常见疑惑](#11-常见疑惑)
    - [1.1.1 Upsample、ConvTranspose2d、conv后PixelShuffle有什么区别](#111-upsampleconvtranspose2dconv后pixelshuffle有什么区别)
- [2 Pytorch](#2-pytorch)
  - [2.1 基本使用](#21-基本使用)
    - [2.1.4 Dataset and dataloader](#214-dataset-and-dataloader)
  - [2.7 坑](#27-坑)
    - [2.7.1 當DataParallel碰上RNN的那些坑](#271-當dataparallel碰上rnn的那些坑)
    - [2.1.2 SynchronizedBatchNorm2d 多卡BatchNorm2d失效](#212-synchronizedbatchnorm2d-多卡batchnorm2d失效)
- [3 TensorRT](#3-tensorrt)
- [4 模型压缩](#4-模型压缩)
  - [4.1 Depth-wise](#41-depth-wise)
  - [4.2 量化](#42-量化)
  - [4.3 蒸馏](#43-蒸馏)
  - [4.4 重参数化](#44-重参数化)
## 1 基础知识
### 1.1 常见疑惑
#### 1.1.1 Upsample、ConvTranspose2d、conv后PixelShuffle有什么区别
1.Upsample上采样
2.先用卷积将通道数扩大一倍，然后用PixelShuffle，将两个通道的特征图相互插入使得尺寸扩大一倍。
3.利用反卷积ConvTranspose2d不改变通道数尺寸扩大一倍。
## 2 Pytorch
### 2.1 基本使用
#### 2.1.4 Dataset and dataloader
```python
class YourDataset(Dataset):

    def __init__(self, ...):
        #load...
        self.len = len()

    def __getitem__(self, index):

        return image, label

    def __len__(self):
        return self.len

def GetLoader(opt, dataset):
    return DataLoader(dataset=dataset,
                      batch_size=opt.batchsize,
                      shuffle=True,
                      num_workers=opt.load_thread
                      )
```
### 2.7 坑
#### 2.7.1 當DataParallel碰上RNN的那些坑
https://meetonfriday.com/posts/d9cbeda0/
1.將model的參數放到gpu上的時候不保證放置的memory位置一定是連續的，所以可能會有fragmentation現象，這會造成效能的降低，透過flatten_parameters()可以使得model的參數在gpu memory上的位置是連續的。
2.因為將data放到不同的gpu上跑時，由於使用了pack_padded_sequence()和pad_packed_sequence()，每個batch的長度都是不固定的，在每張gpu上執行pad_packed_sequence()時，會取它當下batch的最大長度來對其他句子進行padding，這時因為每個gpu上data不同導致當下的最大長度都會不同，在gather的時候就會產生維度不匹配的問題。
所以解決方法是，在使用pad_packed_sequence()時要額外帶入一個參數告訴當下最長的長度是多少，大概像這樣寫：
#### 2.1.2 SynchronizedBatchNorm2d 多卡BatchNorm2d失效
sync bn ，Cross-GPU Synchronized Batch Normalization，是因为多卡训练中每张卡上的batch size过小，不同步会造成BN层失效。单卡直接用原始就好了。

## 3 TensorRT

## 4 模型压缩
### 4.1 Depth-wise
```python

```
经典示范：
[MobileNet，从V1到V3](./https://zhuanlan.zhihu.com/p/70703846)
### 4.2 量化
### 4.3 蒸馏
### 4.4 重参数化

