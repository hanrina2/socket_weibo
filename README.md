# socket_weibo
- 基于socket HTTP服务器的weibo项目
- Web框架采取MVC架构
- Controller层使用高阶函数进行路由分发，自定义请求封装和响应封装
- Model使用自制基于Mysql的ORM， 实现增删改查接口的封装，自动生成对应SQL请求
- View使用Jinja2模板动态渲染页面

# 功能
- 注册/登录
- 微博发布、删除和修改
- 评论发表、删除和修改
- 用户权限

# 演示
![image](https://github.com/hanrina2/socket_weibo/blob/master/weibo_demo.gif)
