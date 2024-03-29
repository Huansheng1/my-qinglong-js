# 幻生青龙脚本备份

## 特别声明
本仓库发布的脚本及其中涉及的任何解锁和解密分析脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害。

间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 本人对于由此引起的任何隐私泄漏或其他后果概不负责。

请勿将本仓库的任何内容用于商业或非法目的，否则后果自负。

如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

任何以任何方式查看此项目的人或直接或间接使用该项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或Script项目的规则，则视为您已接受此免责声明。

您必须在下载后的24小时内从计算机或手机中完全删除以上内容

您使用或者复制了本仓库且本人制作的任何脚本，则视为 已接受 此声明，请仔细阅读


## 公告
> 自写 + 自用 的他人脚本

不定期更新，有问题提issue描述清楚，避免浪费大家时间；或者 进群 -  [通知群](https://t.me/huan_sheng) 

### 青龙拉取
> 先安装nodejs依赖：
* `crypto`

#### 运行说明
旧版本：
```bash
ql repo https://github.com/Huansheng1/my-qinglong-js.git "" "sendNotify.js|utils.js|SendNotify" "sendNotify.js|utils.js|SendNotify" "main"
```
新版：  
新建订阅 - 在名称处粘贴上面命令，定时更新时间自己设置 - 
![](https://pic.imgdb.cn/item/64777068f024cca1734809e1.jpg)、![](https://pic.imgdb.cn/item/64777091f024cca1734833ad.jpg)

> 国内拉取不下来的，可将地址替换为：`https://gitclone.com/github.com/Huansheng1/my-qinglong-js.git`、`https://hub.nuaa.cf/Huansheng1/my-qinglong-js.git`；自己哪个快用哪个，有别的好用的欢迎补充。
### 脚本说明

见各个脚本 头部描述

### 投稿说明

请前往 [discussions](https://github.com/Huansheng1/my-qinglong-js/discussions/2) 查看要求，按说明投递

### 报错提示
1. `/ql/data/config/config.sh: line xxx`：`这种基本都是配置文件里的数据配错了，导致qinglong读取环境变量直接崩了，请检查是否多了空格或者格式不合法`
2. 两个依赖，一个 `https-proxy-agent`，一个 `http-proxy-agent`；两个都要装！别再问了🤡
3. 还有`./utils.js`是文件！不是依赖，单拉文件不是拉整个仓库的去仓库里找到 `utils.js` 文件，放到要运行的脚本同一目录下，别给我装依赖了🥶

