[toc]
## 基础知识
## Pytorch
### 坑
#### 當DataParallel碰上RNN的那些坑
https://meetonfriday.com/posts/d9cbeda0/
1.將model的參數放到gpu上的時候不保證放置的memory位置一定是連續的，所以可能會有fragmentation現象，這會造成效能的降低，透過flatten_parameters()可以使得model的參數在gpu memory上的位置是連續的。
2.因為將data放到不同的gpu上跑時，由於使用了pack_padded_sequence()和pad_packed_sequence()，每個batch的長度都是不固定的，在每張gpu上執行pad_packed_sequence()時，會取它當下batch的最大長度來對其他句子進行padding，這時因為每個gpu上data不同導致當下的最大長度都會不同，在gather的時候就會產生維度不匹配的問題。
所以解決方法是，在使用pad_packed_sequence()時要額外帶入一個參數告訴當下最長的長度是多少，大概像這樣寫：

## TensorRT

