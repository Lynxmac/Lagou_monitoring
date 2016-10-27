# Lagou_monitoring

#### 选择lagou_sendmail脚本，填写修改必要信息，直接扔到VPS，定个crontab定时任务即可

#### 脚本 lagou_ifttt.py 是与 IFTTT挂钩的，在lagou_ifttt.py只需要填写两个变量API_KEY和事件名，发送Trigger Request其它事情由IFTTT完成，但需要在IFTTT上创建Recipe，触发事件搜索MAKER,触发后的action由自己选择，我选择了GMAIL发送邮件，需登录GMAIL

### 大概流程：

- 获取API_KEY
#### API_KEY可在 https://ifttt.com/maker 上获取

- 在 https://ifttt.com/myrecipes/personal/new 创建新的recipe

- 触发事件选择Maker，填写的EVENT NAME, 需要记下，组装trigger request时需要用到

- 执行事件选择Gmail

- 填写修改邮件内容与收件人

- 创建后，可以在 https://ifttt.com/maker 点击 How to Trigger Events ，进入页面进行测试

#### 填写API_KEY和EVENT后，一样直接扔到VPS，再用crontab定个每天执行定时任务
