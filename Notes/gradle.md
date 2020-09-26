[toc]

## 安装
```bash
sudo mv ./android-studio /usr/local/
cd ./android-studio/bin
./studio.sh
```
或者直接在软件管理器中安装.

## sdk下载失败
在总的 build.gradle 中加入阿里云镜像，注意要放在 jcenter() 的上边
```java
// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    repositories {
        google()
        maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }//阿里云镜像服务
        jcenter()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:4.0.1"
    }
}

allprojects {
    repositories {
        google()
        maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }//阿里云镜像服务
        jcenter()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
```