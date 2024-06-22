## 环境配置说明

## Python 环境配置指南

此文档提供了如何使用 `environment.yml` 和 `requirements.txt` 文件来设置Python环境的详细步骤。这些步骤将帮助您确保Python环境的正确配置，以支持特定的开发需求。

### 环境要求

- **Python 版本**: 3.8
- **管理工具**: Conda 和 pip

### 创建环境

#### 使用 Conda

1. **创建环境**：
   使用 `environment.yml` 文件创建一个新的 Conda 环境。确保 `environment.yml` 文件中指定的Python版本为3.8。

   使用以下命令创建环境：
   
   ```bash
   conda env create -f environment.yml
   ```
   
2. **激活环境**：
   环境创建完成后，使用以下命令激活该环境：

   ```bash
   conda activate myenv
   ```

#### 使用 pip

使用pip安装包：

1. **安装 pip 依赖**：
   如果环境中还需要安装由 pip 管理的包，在激活环境后使用 `requirements.txt` 安装这些包。

   安装 pip 依赖：
   
   ```bash
   pip install -r requirements.txt
   ```

通过遵循这些步骤，您可以确保您的Python开发环境是正确配置的。

##  SQLite环境配置说明

### 1. 确认安装包已就位

确保以下安装包已经位于项目根目录下的**``sqlite``**文件夹中：

- **``sqlite-dll-win-x64-3460000``**
- **``sqlite-tools-win-x64-3460000``**

### 2. 配置数据库文件

确认数据库文件 **``database.sqlite``** 已经位于项目根目录下。

### 3. 配置环境变量(如果需要在命令行中使用数据库)

在系统环境变量中添加 SQLite 的上面两个安装路径，以便在命令行中可以直接访问 SQLite 工具。

### 4. 连接数据库

根据后端数据库使用说明

## 后端数据库使用说明

### 概述

后端系统使用 SQLite3 数据库来存储和管理数据。SQLite3 是一种轻量级的嵌入式数据库管理系统，使用简单轻便，整个数据库文件只由一个文件组成。

### 数据库使用说明

#### 数据库文件

后端使用的数据库**已经创建完毕**，文件位于项目根目录下的 `database.sqlite` 文件。该文件包含了系统所有的数据表和相关数据。

#### 创建数据库

如果仍需创建数据库，运行init_db.py。

### 测试数据库

运行oringin.py，main函数部分已经测试了增删改查

## 表结构

### 1. Book

存储图书信息。

| 字段名                    | 数据类型  | 描述                         |
| ------------------------- | --------- | ---------------------------- |
| book_id                   | char(8)   | 图书的唯一标识符，主键       |
| book_name                 | char(100) | 图书名称                     |
| book_image                | blob      | 存储图书封面图片的二进制数据 |
| book_author               | char(100) | 作者名                       |
| book_location             | char(100) | 图书位置信息                 |
| book_score                | float     | 图书评分                     |
| book_storage              | char(50)  | 存储信息                     |
| book_reservation_time     | float     | 预约时间长度                 |
| book_reservation_location | char(100) | 预约取书位置                 |

### 2. StudentAccount

存储学生账户信息。

| 字段名   | 数据类型  | 描述                 |
| -------- | --------- | -------------------- |
| net_id   | char(8)   | 学生网络标识符，主键 |
| name     | char(100) | 学生姓名             |
| gain     | int       | 积分                 |
| password | char(100) | 账户密码             |

### 3. TeacherAccount

存储教师账户信息。

| 字段名    | 数据类型  | 描述                 |
| --------- | --------- | -------------------- |
| net_id    | char(8)   | 教师网络标识符，主键 |
| name      | char(100) | 教师用户名           |
| real_name | char(100) | 教师真实姓名         |
| gain      | int       | 积分                 |
| password  | char(100) | 账户密码             |

### 4. AdminAccount

存储管理员账户信息。

| 字段名    | 数据类型  | 描述                   |
| --------- | --------- | ---------------------- |
| net_t     | char(8)   | 管理员网络标识符，主键 |
| name      | char(100) | 管理员姓名             |
| gain      | int       | 积分                   |
| real_name | char(100) | 管理员真实姓名         |
| password  | char(100) | 账户密码               |

### 5. Comment

存储用户对图书的评论。

| 字段名      | 数据类型   | 描述                       |
| ----------- | ---------- | -------------------------- |
| net_id      | char(8)    | 用户网络标识符             |
| book_id     | char(8)    | 图书标识符                 |
| comment     | char(1000) | 评论内容                   |
| score       | int        | 评分                       |
| time        | float      | 评论时间                   |
| primary key |            | 复合主键 (net_id, book_id) |

### 6. ReservationBook

存储图书预约信息。

| 字段名      | 数据类型 | 描述                       |
| ----------- | -------- | -------------------------- |
| net_id      | char(8)  | 用户网络标识符             |
| book_id     | char(8)  | 图书标识符                 |
| time        | float    | 预约时间                   |
| primary key |          | 复合主键 (net_id, book_id) |

### 7. BorrowBook

存储图书借阅信息。

| 字段名      | 数据类型 | 描述                      |
| ----------- | -------- | ------------------------- |
| net_id      | char(8)  | 用户网络标识符            |
| book_id     | char(8)  | 图书标识符                |
| time        | float    | 借阅时间                  |
| primary key |          | 复合主键 (net_id, book_t) |

## API文档

### API 文档概览

#### 基础信息
- **基础URL**: `http://<your-domain>/`
- **协议**: REST
- **返回格式**: JSON
- **认证方式**: （如果需要）每个请求需在Header中包含有效的API Key。

#### 状态码
- **200 OK**: 请求成功。
- **201 Created**: 资源创建成功。
- **400 Bad Request**: 服务器无法理解请求格式。
- **404 Not Found**: 请求的资源未找到。
- **500 Internal Server Error**: 服务器内部错误。

---

### API端点详细信息

#### 1. 学生账户管理

##### 创建学生账户
- **方法**: POST
- **URL**: `/account/student`
- **请求体**:
  ```json
  {
    "net_id": "student123",
    "name": "John Doe",
    "gain": 100,
    "password": "password123"
  }
  ```
- **成功响应**:
  ```json
  {
    "message": "Account created successfully"
  }
  ```
- **失败响应**:
  ```json
  {
    "error": "Invalid request data"
  }
  ```

##### 获取学生账户信息
- **方法**: GET
- **URL**: `/account/student/<net_id>`
- **成功响应**:
  ```json
  {
    "net_id": "student123",
    "name": "John Doe",
    "real_name": null,
    "gain": 100,
    "password": "password123"
  }
  ```
- **失败响应**:
  ```json
  {
    "message": "Account not found"
  }
  ```

##### 更新学生账户信息
- **方法**: PUT
- **URL**: `/account/student/<net_id>`
- **请求体**:
  ```json
  {
    "name": "Updated Name",
    "gain": 150
  }
  ```
- **成功响应**:
  ```json
  {
    "message": "Account updated successfully"
  }
  ```

##### 删除学生账户
- **方法**: DELETE
- **URL**: `/account/student/<net_id>`
- **成功响应**:
  ```json
  {
    "message": "Account deleted successfully"
  }
  ```

#### 2. 教师账户管理
（同学生账户管理）

#### 3. 管理员账户管理
（同学生账户管理）

#### 4. 评论管理

##### 创建评论
- **方法**: POST
- **URL**: `/comments`
- **请求体**:
  ```json
  {
    "net_id": "user123",
    "book_id": "book456",
    "comment": "This book is great!",
    "score": 5,
    "time": 1645612345.678
  }
  ```
- **成功响应**:
  ```json
  {
    "message": "Item created successfully"
  }
  ```

##### 获取评论
- **方法**: GET
- **URL**: `/comments/<net_id>/<book_id>`
- **成功响应**:
  ```json
  {
    "net_id": "user123",
    "book_id": "book456",
    "comment": "This book is great!",
    "score": 5,
    "time": 1645612345.678
  }
  ```

##### 删除评论
- **方法**: DELETE
- **URL**: `/comments/<net_id>/<book_id>`
- **成功响应**:
  ```json
  {
    "message": "Item deleted successfully"
  }
  ```

#### 5. 书籍管理

##### 创建书籍
- **方法**: POST
- **URL**: `/books`
- **请求体**:
  ```json
  {
    "book_id": "book123",
    "book_name": "Python Programming",
    "book_image": "<base64_encoded_image_data>",
    "book_author": "Guido van Rossum",
    "book_location": "Library

 A",
    "book_score": 4.5,
    "book_storage": "Shelf B",
    "book_reservation_time": 3600.0,
    "book_reservation_location": "Desk 1"
  }
  ```
- **成功响应**:
  ```json
  {
    "message": "Book created successfully"
  }
  ```

##### 获取书籍信息
- **方法**: GET
- **URL**: `/books/<book_id>`
- **成功响应**:
  ```json
  {
    "book_id": "book123",
    "book_name": "Python Programming",
    "book_image": "<base64_encoded_image_data>",
    "book_author": "Guido van Rossum",
    "book_location": "Library A",
    "book_score": 4.5,
    "book_storage": "Shelf B",
    "book_reservation_time": 3600.0,
    "book_reservation_location": "Desk 1"
  }
  ```

##### 更新书籍信息
- **方法**: PUT
- **URL**: `/books/<book_id>`
- **请求体**:
  ```json
  {
    "book_name": "Updated Python Programming",
    "book_author": "Updated Author",
    "book_location": "Updated Library A",
    "book_score": 4.7,
    "book_storage": "Updated Shelf B",
    "book_reservation_time": 7200.0,
    "book_reservation_location": "Updated Desk 2"
  }
  ```
- **成功响应**:
  ```json
  {
    "message": "Book updated successfully"
  }
  ```

##### 删除书籍
- **方法**: DELETE
- **URL**: `/books/<book_id>`
- **成功响应**:
  ```json
  {
    "message": "Book deleted successfully"
  }
  ```

