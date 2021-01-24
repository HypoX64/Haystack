### Android 10+使用blueadapter搜索不到蓝牙设备的原因

查看Android官方文档关于蓝牙的部分：https://developer.android.com/guide/topics/connectivity/bluetooth
官方文档中指出：
```
如要在应用中使用蓝牙功能，您必须声明两个权限。
第一个是 BLUETOOTH。您需要此权限才能执行任何蓝牙通信，例如请求连接、接受连接和传输数据等。
第二个必须声明的权限是 ACCESS_FINE_LOCATION。您的应用需要此权限，因为蓝牙扫描可用于收集用户的位置信息。此类信息可能来自用户自己的设备，以及在商店和交通设施等位置使用的蓝牙信标。
注意：如果您的应用适配 Android 9（API 级别 28）或更低版本，则您可以声明 ACCESS_COARSE_LOCATION 权限而非 ACCESS_FINE_LOCATION 权限。
```
因此，对于蓝牙的使用需要注意：
1.除了蓝牙权限需要开启之外，位置权限也需要开启（这在Android6.0之后就要求了）。<br>
2.Android10.0以上需要开启的位置权限是```ACCESS_FINE_LOCATION```，而9.0及以下开启```ACCESS_COARSE_LOCATION```就可以了，当然使用```ACCESS_FINE_LOCATION```也可以兼容。
3.手机需要开启位置服务以及蓝牙，并保证权限已授权