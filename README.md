![epub](./image/epub.png)

# 自动签到

试下 github action 功能，刚好有一个小说网站练习下，都能来 github 了，下载 epub 小说还是建议去 zlib

##  本脚本功能

- iamtxt 签到，并将签到结果通过 `server酱` 发到微信。脚本非常简单，没难度，入门即会。

- ~~hifini 自动签到~~ 树大招风, 已闭站

- hifiti 自动签到

- ~~hifinicn 自动签到~~ GitHub 服务器无法访问, 不能自动签到

##  使用方法

如果你也想签到，通过你以下三步，就可以每天都有 1 积分到帐。2 积分可下载一本书

1. fork 本项目
2. 添加四个变量   当前页面 ⇨ Settings ⇨ Secrets ⇨ New repository secret ⇨ Secrets
   | 变量名     | 解释                    |
   | ---------- | ----------------------- |
   | COOKIE     | iamtxt 的 cookie        |
   | SENDKEY    | Server 酱的 key         |
   | HIFITICOOKIE | hifiti 的 cookie        |
   | HIFINICNCOOKIE | hifinicn 的 cookie        |

3. 测试启用 Actions
4. 没看明白？看 [这个项目](https://github.com/anduinnn/HiFiNi-Auto-CheckIn) 

> **可能遇见的使用问题**
>
> - 可能会失效，所以需要不定期改 cookie
> - 代码不健壮，四个变量必添加, 不然无法运行
> - GitHub Actions 一次最多运行 60 天, 每 60 天需打开 Actions 页面重新确认运行

## 计划

- ~~不 fork 别人的项目，将 hifini 加入~~
