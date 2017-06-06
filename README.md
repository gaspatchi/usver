**Usver** - сервис для работы с профилем пользователя

**Примеры запросов и ответов**

----------
- `GET` / - Получение профиля пользователя
>Для выполнения этого запроса требуется **токен**

- `Response`
```
{
{
  "info": {
    "profile": {
      "firstname": "Никита",
      "lastname": "Бережной"
    },
    "meta": {
      "type": "Студент",
      "image": "..."
    },
    "contacts": {
      "email": "nikitoshi@gaspatchi.ru",
      "number": "..."
    }
  },
  "subscription": {
    "dispatch": {
      "sms": {
        "activated": false
      },
      "email": {
        "activated": true
      }
    },
    "schedule": {
      "groups": [],
      "teachers": []
    }
  }
}
```

- `POST` / - Обновление профиля пользователя
>Для выполнения этого запроса требуется **токен**

- `Request`

| Параметр  | Тип    | Требуется | Описание                       |
| --------- | ------ | --------- | ------------------------------ |
| firstname | string | false     | Имя пользователя               |
| lastname  | string | false     | Фамилия пользователя           |
| image     | string | false     | Аватарка пользователя в base64 |
| number    | string | false     | Номер телефона пользователя    |
| password  | string | false     | Новый пароль к аккаунту        |

- `Response`
```
{
  "message": "Профиль успешно обновлен"
}
```

- `POST` /login - Вход в профиль
- `Request`

| Параметр | Тип    | Требуется | Описание                       |
| -------- | ------ | --------- | ------------------------------ |
| email    | string | true      | Почта пользователя             |
| password | string | true      | Пароль к аккаунту              |

- `Response`
```
{
"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoi0KHRgtGD0LTQtdC90YIiLCJmaXJzdG5hbWUiOiJOWtpdGEiLCJsYXN0bmFtZSI6IkJlcmV6aG5veSIsImlhdCI6MTQ5Njc2NjkyNCwiZXhwIjoxNDk3OTc2NTI0LCJzdWIiOiJuaWtpdG9zaGlAZ2FzcGF0Y2hpLnJ1In0.vvrD8WY3dJQwYGbIwP2HYjO7VzFQC7njWF3bo1ZmIcY"
}
```

- `POST` /register - Регистрация аккаунта
- `Request`

| Параметр  | Тип    | Требуется | Описание                |
| --------- | ------ | --------- | ----------------------- |
| firstname | string | true      | Имя пользователя        |
| lastname  | string | true      | Фамилия пользователя    |
| email     | string | true      | Почта пользователя      |
| password  | string | true      | Пароль к аккаунту       |

- `Response`
```
{
  "message": "Успешная регистрация"
}
```

- `GET` /verification/{token} - Подтверждение действий пользователя
- `Response`
```
{
  "message": "Успешное подтверждение регистрации"
}
```

- `POST` /reset - Сброс пароля
- `Request`

| Параметр  | Тип    | Требуется | Описание                |
| --------- | ------ | --------- | ----------------------- |
| email     | string | true      | Почта пользователя      |

- `Response`
```
{
  "message": "Письмо с подтверждением сброса пароля отправлено на вашу почту"
}
```

**HTTP коды ответа**

----------
| HTTP Код | Описание                         |
| -------- | -------------------------------- |
| 200      | Успешное выполнение запроса      |
| 400      | Сервер не смог обработать запрос |
| 403      | Токен оказался невалидным        |
| 404      | Пользователь не найден           |
| 409      | Пользователь уже существует      |
| 500      | Ошибка сервера                   |