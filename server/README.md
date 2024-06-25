# 项目简介

本系统为图书管理系统的后端实现，提供了完整的API服务，支持图书的添加、查询、借阅与归还功能。系统采用现代的后端架构设计，确保了高效的数据处理和稳定的性能表现。

# 后端环境配置指南

本文档提供了使用 `environment.yml` 和 `requirements.txt` 文件来设置 Python 环境的详细步骤，以及配置 SQLite 数据库的指南。这些步骤将帮助您确保 Python 环境和数据库环境的正确配置，以支持特定的开发需求。

## Python 环境配置

### 环境要求

- **Python 版本**: 3.8
- **管理工具**: Conda 和 pip

### 使用 Conda 创建环境

1. **创建环境**：
   使用 `environment.yml` 文件创建一个新的 Conda 环境。确保文件中指定的 Python 版本为 3.8。

   ```bash
   conda env create -f environment.yml

2. **激活环境**：
   环境创建完成后，使用以下命令激活该环境：

   ```bash
   conda activate myenv
   ```

### 使用 pip 安装依赖

在激活的 Conda 环境中，使用 pip 安装额外的依赖：

```bash
pip install -r requirements.txt
```

## SQLite3数据库环境配置

为了设置和使用数据库，需要遵循以下步骤来配置SQLite3数据库环境：

### 运行数据库初始化脚本

   - 使用Python运行`init_db.py`脚本来创建表格和插入初步数据。确保脚本文件的路径正确，然后在命令行中运行：
     ```bash
     python init_db.py
     ```
     
   - 运行脚本后，数据库将被初始化，表格将被创建，会在项目目录中创建一个名为 `database.sqlite` 的文件，该文件已经包含整个数据库的所有文件，并且会插入一些示例数据。

### 数据库初始化内容

在本项目中，已预先填充了以下几种类型的数据以便于快速启动和演示：

1. **用户数据**: 已经添加了三名用户，分别具有不同的角色：
   - 学生用户：用户名为 `student_user`，电子邮箱为 `student@example.com`，使用'password123'登录。
   - 教师用户：用户名为 `teacher_user`，电子邮箱为 `teacher@example.com`，使用'password123'登录。
   - 管理员用户：用户名为 `admin_user`，电子邮箱为 `admin@example.com`，使用'password123'登录。
2. **书籍数据**: 从一个预设的文本文件中读取书籍信息，并批量插入数据库。这些书籍包括各种详细信息，如书名、作者、出版社、出版日期、ISBN编号及当前状态（如可借、已预订等）。书籍信息也包含书籍封面的图片数据，以二进制形式存储。

# 后端运行方式指南

## 启动后端服务

使用 

```
run.py
```

 文件来启动后端服务器。该脚本配置了所有必要的环境，并启动Flask应用程序。

## 运行测试

- 项目中包含了一套完整的单元测试，覆盖了不同的模块（例如用户、书籍、评论等）。运行这些测试以确保后端服务的每个部分都按预期工作：

  ```
  bash
  复制代码
  python -m unittest discover -s tests
  ```

- 详细测试：

  - 每个测试文件例如 

    ```
    test_user.py 
    ```

     等，都可以单独运行，以测试相关模块的功能。例如，要单独运行书籍的测试：

    ```
    python -m unittest tests/test_book.py
    ```

> ⚠️ 测试代码最后会直接清空数据库！

## API 使用

- 启动服务器后，API 将在本地运行，默认是在 `http://localhost:5000/`。
- 保证在运行测试或使用API前，您已经通过运行 `init_db.py` 初始化了数据库，确保所有数据表和必要的数据已经就绪。

这样，您就可以开始使用后端服务器进行开发或测试了。

## API文档

### **3.1 用户管理服务**

#### **功能描述**

- 用户注册
- 用户登录
- 查看/修改个人信息
- 管理用户（管理员权限）

#### **接口设计**

| 接口名       | 请求方法 | URL                    | 描述                       | 请求参数                                                     | 返回值                                                       | 异常                                                         |
| ------------ | -------- | ---------------------- | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 注册用户     | POST     | /api/users/register    | 注册新用户                 | `{username, password, email, role}`                          | `{message: "User registered successfully", userId: int}`,201 | `{error: "Username already exists"}`,400                     |
| 用户登录     | POST     | /api/users/login       | 用户登录                   | `{username, password}`                                       | `{token: "jwt_token", userId: int, role: "user_role"}`,200   | `{error: "Invalid username or password"}`,401                |
| 查看个人信息 | GET      | /api/users/{id}        | 查看用户信息               | `Headers: {Authorization: "Bearer jwt_token"}`               | `{userId, username, email, points, registration_date, role}`,200 | `{error: "User not found"}`,404                              |
| 查询用户积分 | GET      | /api/users/{id}/points | 查询用户积分               | `Headers: {Authorization: "Bearer jwt_token"}`               | `{points: int}`,200                                          | `{error: "User not found"}`，404                             |
| 修改个人信息 | PUT      | /api/users/{id}        | 修改用户基本信息           | `Headers: {Authorization: "Bearer jwt_token"}<br>``{email}`  | `{message: "User information updated successfully"}`,200     | `{error: "User not found"}<br>``,404``{error: "Unauthorized"}`,401 |
| 更改用户积分 | PUT      | /api/users/{id}/points | 更改用户积分（管理员权限） | `Headers: {Authorization: "Bearer jwt_token"}<br>``{points}` | `{message: "User points updated successfully"}`,200          | `{error: "User not found"}<br>`,404```{error: "Unauthorized"}`,401 |
| 新增用户     | POST     | /api/admin/users       | 新增用户（管理员权限）     | `Headers: {Authorization: "Bearer jwt_token"}<br>``{user_data}` | `{message: "User added successfully", userId: int}`,200      | `{error: "Unauthorized"}`,401                                |
| 删除用户     | DELETE   | /api/users/{id}        | 删除用户（管理员权限）     | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "User deleted successfully"}`,200                 | `{error: "User not found"}<br>``，404``{error: "Unauthorized"}`,401 |

### **3.2 图书管理服务**

#### **功能描述**

- 浏览图书
- 预约图书
- 查看/更新图书信息（管理员权限）
- 管理图书状态

#### **接口设计**

| 接口名             | 请求方法 | URL                                | 描述                                                         | 请求参数                                                     | 返回值                                                       | 异常                                                         |
| ------------------ | -------- | ---------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 浏览图书           | GET      | /api/books                         | 获取所有图书信息                                             | 无                                                           | `[ {bookId, title, author, publisher, publish_date, isbn, location, status, reservation_count, borrower_id, book_image,average_rating} ]`200 | `{error: "No books found"}`404                               |
| 搜索图书           | GET      | /api/books/search                  | 根据关键字获取相关图书列表                                   | `{query: string}`                                            | `[ {bookId, title, author, publisher, publish_date, isbn, location, status, reservation_count, borrower_id, book_image,average_rating} ]`200 | `{error: "No books found for the given query"}`404           |
| 查看图书详情       | GET      | /api/books/{id}                    | 获取单本图书信息                                             | 无                                                           | `{bookId, title, author, publisher, publish_date, isbn, location, status, reservation_count, borrower_id, book_image,average_rating}`200 | `{error: "Book not found"}`404                               |
| 查看图书状态       | GET      | /api/books/{id}/status             | 获取单本图书的当前状态                                       | 无                                                           | `{status: "available"}`200                                   | `{error: "Book not found"}`404                               |
| 查看用户已借阅图书 | GET      | /api/books/borrowed/user/{user_id} | 查看某个用户已借阅的图书                                     | 无                                                           | `[ {bookId, title, author, publisher, publish_date, isbn, location, status, borrower_id, book_image,average_rating} ]`200 | `{error: "No borrowed books found for the user"}`404         |
| 预约图书           | POST     | /api/books/{id}/reserve            | 预约图书,增加预约人数<br />(人数为0时要改变预约状态)<br />根据序列图可能要调用其他服务 | `Headers: {Authorization: "Bearer jwt_token"}<br>``{userId: int}` | `{message: "Book reserved successfully"}`                    | `{error: "Book not available for reservation"}`              |
| 添加图书           | POST     | /api/books                         | 添加新图书（管理员权限）                                     | `Headers: {Authorization: "Bearer jwt_token"}<br>``{title, author, publisher, publish_date, isbn, location, book_image}` | `{message: "Book added successfully", bookId: int}`201       | `{error: "Unauthorized"}`401                                 |
| 更新图书信息       | PUT      | /api/books/{id}                    | 更新图书信息（管理员权限）                                   | `Headers: {Authorization: "Bearer jwt_token"}<br>``{title, author, publisher, publish_date, isbn, location, book_image}` | `{message: "Book information updated successfully"}`200      | `{error: "Book not found"}<br>```404```{error: "Unauthorized"}`401 |
| 更新图书状态       | PUT      | /api/books/{id}/status             | 更新单本图书的当前状态（管理员权限）                         | `Headers: {Authorization: "Bearer jwt_token"}<br>``{status: "available"}` | `{message: "Book status updated successfully"}`200           | `{error: "Book not found"}<br>``404````{error: "Unauthorized"}`401 |
| 删除图书           | DELETE   | /api/books/{id}                    | 删除图书（管理员权限）                                       | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "Book deleted successfully"}`200                  | `{error: "Book not found"}<br>``404````{error: "Unauthorized"}`401 |
| 借阅图书           | PUT      | /api/books/{id}/borrow             | 借阅图书（管理员权限）更改图书状态，设置借书人               | `Headers: {Authorization: "Bearer jwt_token"}<br>``{userId: int}` | `{message: "Book borrowed successfully"}``                   | ``{error: "Book not available for borrowing"}<br>``{error: "Unauthorized"}` |

### **3.3 预约管理服务**

#### **功能描述**

- 提交预约请求
- 查看预约状态
- 管理预约（管理员权限）

#### **接口设计**

| 接口名                        | 请求方法 | URL                              | 描述                                                         | 请求参数                                                     | 返回值                                                       | 异常                                                         |
| ----------------------------- | -------- | -------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 提交预约                      | POST     | /api/reservations                | 提交预约请求<br />(根据bookId查找book_location)              | `Headers: {Authorization: "Bearer jwt_token"}<br>``{userId, bookId, reservation_location}` | `{message: "Reservation submitted successfully", reservationId: int}` | `{error: "Book not available for reservation"}`              |
| 查看预约                      | GET      | /api/reservations/{id}           | 查看预约                                                     | `Headers: {Authorization: "Bearer jwt_token"}`               | `{reservationId, userId, bookId, reservation_date, status, book_location, reservation_location}` | `{error: "Reservation not found"}`                           |
| 查看所有已确认预约(confirmed) | GET      | /api/reservations/confirmed      | 查看所有已确认的预约帖子                                     | `Headers: {Authorization: "Bearer jwt_token"}`               | `[ {reservationId, userId, bookId, reservation_date, status, book_location, reservation_location} ]` | `{error: "No confirmed reservations found"}`                 |
| 查看用户所有预约书籍          | GET      | /api/reservations/user/{user_id} | 查看某个用户所有预约的书籍                                   | `Headers: {Authorization: "Bearer jwt_token"}`               | `[ {reservationId, userId, bookId, reservation_date, status, book_location, reservation_location} ]` | `{error: "No reservations found for the user"}`              |
| 查看书籍预约信息              | GET      | /api/reservations/book/{book_id} | 查看某本书所有的预约信息                                     | `Headers: {Authorization: "Bearer jwt_token"}`               | `[ {reservationId, userId, bookId, reservation_date, status, book_location, reservation_location} ]` | `{error: "No reservations found for the book"}`              |
| 取消预约                      | PUT      | /api/reservations/{id}/cancel    | 取消预约<br />(改变预约状态)                                 | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "Reservation cancelled successfully"}`            | `{error: "Reservation not found"}`                           |
| 修改预约信息                  | PUT      | /api/reservations/{id}           | 修改预约信息（管理员权限）<br />(这里需要一条预约的全部信息) | `Headers: {Authorization: "Bearer jwt_token"}<br>``{reservation_data}` | `{message: "Reservation information updated successfully"}`  | `{error: "Reservation not found"}<br>``{error: "Unauthorized"}` |
| 删除预约                      | DELETE   | /api/reservations/{id}           | 删除预约（管理员权限）                                       | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "Reservation deleted successfully"}`              | `{error: "Reservation not found"}<br>``{error: "Unauthorized"}` |
| 完成预约                      | PUT      | /api/reservations/{id}/complete  | 完成预约（管理员权限）                                       | `Headers: {Authorization: "Bearer jwt_token"}<br>``{user``_i``d: int}` | `{message: "Reservation completed successfully"}`            | `{error: "Reservation not found"}<br>``{error: "Unauthorized"}` |

### **3.4 活动管理服务**

#### **功能描述**

- 查看活动
- 管理活动（管理员权限）

#### **接口设计**

| 接口名       | 请求方法 | URL                  | 描述                       | 请求参数                                                     | 返回值                                                       | 异常                                                         |
| ------------ | -------- | -------------------- | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 查看活动     | GET      | /api/activities      | 获取所有活动信息           | 无                                                           | `[ {activityId, name, description, start_time, end_time, location, link} ]` | `{error: "No activities found"}`                             |
| 查看活动详情 | GET      | /api/activities/{id} | 获取单个活动信息           | 无                                                           | `{activityId, name, description, start_time, end_time, location, link}` | `{error: "Activity not found"}`                              |
| 添加活动     | POST     | /api/activities      | 添加新活动（管理员权限）   | `Headers: {Authorization: "Bearer jwt_token"}<br>``{name, description, start_time, end_time, location, link}` | `{message: "Activity added successfully", activityId: int}`  | `{error: "Unauthorized"}`                                    |
| 更新活动信息 | PUT      | /api/activities/{id} | 更新活动信息（管理员权限） | `Headers: {Authorization: "Bearer jwt_token"}<br>``{name, description, start_time, end_time, location, link}` | `{message: "Activity information updated successfully"}`     | `{error: "Activity not found"}<br>``{error: "Unauthorized"}` |
| 删除活动     | DELETE   | /api/activities/{id} | 删除活动（管理员权限）     | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "Activity deleted successfully"}`                 | `{error: "Activity not found"}<br>``{error: "Unauthorized"}` |

### **3.5 评价管理服务**

#### **功能描述**

- 查看评价
- 发表评价
- 管理评价（管理员权限）

#### **接口设计**

| 接口名       | 请求方法 | URL                         | 描述                       | 请求参数                                                     | 返回值                                                       | 异常                                                       |
| ------------ | -------- | --------------------------- | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------- |
| 查看评价     | GET      | /api/reviews                | 获取所有评价信息           | 无                                                           | `[ {reviewId, userId, bookId, content, rating, review_date} ]` | `{error: "No reviews found"}`                              |
| 查看评价详情 | GET      | /api/reviews/{id}           | 获取单个评价信息           | 无                                                           | `{reviewId, userId, bookId, content, rating, review_date}`   | `{error: "Review not found"}`                              |
| 查看书籍评价 | GET      | /api/books/{bookId}/reviews | 获取某本书的全部评价信息   | 无                                                           | `[ {reviewId, userId, bookId, content, rating, review_date} ]` | `{error: "No reviews found for the book"}`                 |
| 查看图书评分 | GET      | /api/books/{bookId}/rating  | 获取某本书的平均评分       | 无                                                           | `{bookId, average_rating: float}`                            | `{error: "Book not found"}`                                |
| 发表评价     | POST     | /api/reviews                | 发表新评价                 | `Headers: {Authorization: "Bearer jwt_token"}<br>``{userId, bookId, content, rating}` | `{message: "Review added successfully", reviewId: int}`      | `{error: "Unauthorized"}`                                  |
| 更新评价     | PUT      | /api/reviews/{id}           | 更新评价信息（管理员权限） | `Headers: {Authorization: "Bearer jwt_token"}<br>``{content, rating}` | `{message: "Review information updated successfully"}`       | `{error: "Review not found"}<br>``{error: "Unauthorized"}` |
| 删除评价     | DELETE   | /api/reviews/{id}           | 删除评价（管理员权限）     | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "Review deleted successfully"}`                   | `{error: "Review not found"}<br>``{error: "Unauthorized"}` |

### **3.6 积分管理服务**

#### **功能描述**

- 查看积分记录
- 更新积分（管理员权限）

#### **接口设计**

| 接口名       | 请求方法 | URL              | 描述                         | 请求参数                                                     | 返回值                                                    | 异常                                                      |
| ------------ | -------- | ---------------- | ---------------------------- | ------------------------------------------------------------ | --------------------------------------------------------- | --------------------------------------------------------- |
| 查看积分记录 | GET      | /api/scores      | 获取所有积分记录             | 无                                                           | `[ {scoreId, userId, points, change_date, description} ]` | `{error: "No scores found"}`                              |
| 查看单条积分 | GET      | /api/scores/{id} | 获取单条积分记录             | 无                                                           | `{scoreId, userId, points, change_date, description}`     | `{error: "Score not found"}`                              |
| 添加积分记录 | POST     | /api/scores      | 添加新积分记录（管理员权限） | `Headers: {Authorization: "Bearer jwt_token"}<br>``{userId, points, description}` | `{message: "Score added successfully", scoreId: int}`     | `{error: "Unauthorized"}`                                 |
| 更新积分记录 | PUT      | /api/scores/{id} | 更新积分记录（管理员权限）   | `Headers: {Authorization: "Bearer jwt_token"}<br>``{points, description}` | `{message: "Score information updated successfully"}`     | `{error: "Score not found"}<br>``{error: "Unauthorized"}` |
| 删除积分记录 | DELETE   | /api/scores/{id} | 删除积分记录（管理员权限）   | `Headers: {Authorization: "Bearer jwt_token"}`               | `{message: "Score deleted successfully"}`                 | `{error: "Score not found"}<br>``{error: "Unauthorized"}` |
