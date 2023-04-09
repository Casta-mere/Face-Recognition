# Database Design

## 用户信息
| Attribute | Translation | Type    | Note  |
| :-------- | :---------- | :------ | :---: |
| Id        | 编号        | int     | 主键  |
| Name      | 名字        | varchar |       |
| email     | 邮箱        | varchar |       |

## 打卡信息
| Attribute | Translation | Type    | Note  |
| :-------- | :---------- | :------ | :---: |
| Id        | 编号        | int     | 主键  |
| Name      | 名字        | varchar |       |
| Date      | 日期        | date    |       |
| TimeS     | 上班时间    | time    |       |
| TimeE     | 下班时间    | time    |       |
| Bool      | 是否违规    | boolean |       |

