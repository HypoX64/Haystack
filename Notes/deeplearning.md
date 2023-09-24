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
### 2.2 高级使用
#### 2.2.1 打印梯度
```python
for k, v in net.module.depth_optimizer.named_parameters():
    print(k,v.grad)
```
#### 2.2.2 梯度阶段
```python
optimizer.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm(net.module.parameters(),max_norm=1e-2, norm_type=2)
optimizer.step()
```
#### 2.2.3 判断nan与inf，去掉他们
```python

def drop_nan_inf(tensor):
    tensor = torch.where(torch.isnan(tensor), torch.full_like(tensor, 0), tensor)
    tensor = torch.where(torch.isinf(tensor), torch.full_like(tensor, 1), tensor)
    return tensor
    
if torch.isnan(imgs).any():
    print('nan in imgs')
    exit()
if torch.isinf(imgs).any():
    print('inf in imgs')
    exit()
```

#### 2.2.4 记录模型运行
```
with torch.profiler.record_function("net"):
    net(img)
```

#### 2.2.5 一种自适应归一化方法
```python
# 解决输入尺度不一致，且需要归一化到0-1直接的问题
def normalize_depth(depth,expand=1.0):
    bs,c,h,w = depth.shape
    _depth = depth.view(bs,c*h*w)
    mean = torch.mean(_depth,dim=1).view(bs,1,1,1)
    mean = torch.clamp(mean,min=1e-3,max=1e6)
    depth = torch.clamp((depth+mean*(expand-1)) /(mean*expand*2),0,1)
    return depth,mean

def anti_normalize_depth(depth,mean,expand=1.0):
    depth = depth*mean*expand*2 - mean*(expand-1)
    return depth
```


### 2.7 坑
#### 2.7.1 當DataParallel碰上RNN的那些坑
https://meetonfriday.com/posts/d9cbeda0/
1.將model的參數放到gpu上的時候不保證放置的memory位置一定是連續的，所以可能會有fragmentation現象，這會造成效能的降低，透過flatten_parameters()可以使得model的參數在gpu memory上的位置是連續的。
2.因為將data放到不同的gpu上跑時，由於使用了pack_padded_sequence()和pad_packed_sequence()，每個batch的長度都是不固定的，在每張gpu上執行pad_packed_sequence()時，會取它當下batch的最大長度來對其他句子進行padding，這時因為每個gpu上data不同導致當下的最大長度都會不同，在gather的時候就會產生維度不匹配的問題。
所以解決方法是，在使用pad_packed_sequence()時要額外帶入一個參數告訴當下最長的長度是多少，大概像這樣寫：
#### 2.7.2 SynchronizedBatchNorm2d 多卡BatchNorm2d失效
sync bn ，Cross-GPU Synchronized Batch Normalization，是因为多卡训练中每张卡上的batch size过小，不同步会造成BN层失效。此时要将所有的BatchNorm2d转换为SynchronizedBatchNorm2d
```python
net = torch.nn.SyncBatchNorm.convert_sync_batchnorm(net)
```
### 2.8 第三方库安装起来的疑难杂症
#### 2.8.1 pytorch3d
pytorch3d 0.7已经支持直接通过conda安装，请使用0.71以上版本，性能有较大提升
```bash
# 首先更新conda并创建环境
conda create -n pytorch3d python=3.9.12
conda activate pytorch3d
# pytorch
# conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.6 -c pytorch -c conda-forge
# pytorch3d
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
conda install -c bottler nvidiacub
conda install pytorch3d -c pytorch3d
# torch_scatter
conda install pytorch-scatter -c pyg
# 其他依赖
pip install -r requirements.txt
```
#### 2.8.2 nerfstudio
https://github.com/nerfstudio-project/nerfstudio/tree/v0.2.2
```bash
# 创建环境
conda create --name nerfstudio -y python=3.8
conda activate nerfstudio
python -m pip install --upgrade pip
# 安装pytorch
pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 -f https://download.pytorch.org/whl/torch_stable.html
# 安装tiny-cuda-nn
pip install ninja
git clone --recursive https://github.com/nvlabs/tiny-cuda-nn
cd tiny-cuda-nn
git checkout tags/v1.6
cd .\bindings\torch
python setup.py install
# 安装nerfstudio
git clone https://github.com/nerfstudio-project/nerfstudio
cd nerfstudio
git checkout tags/v0.2.2
pip install -e .
# 测试完成安装
ns-download-data nerfstudio --capture-name=poster
ns-train nerfacto --data data/nerfstudio/poster
```

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

