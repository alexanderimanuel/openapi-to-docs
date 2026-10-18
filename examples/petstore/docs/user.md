# user

Part of the [Swagger Petstore - OpenAPI 3.0](README.md) documentation.

Operations about user

## POST /user

**Create user.**

This can only be done by the logged in user.

- **Operation ID:** `createUser`

### Request body

Optional. Created user object

Content types: `application/json`, `application/xml`, `application/x-www-form-urlencoded`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `username` | string | no |  | `"theUser"` |
| `firstName` | string | no |  | `"John"` |
| `lastName` | string | no |  | `"James"` |
| `email` | string | no |  | `"john@email.com"` |
| `password` | string | no |  | `"12345"` |
| `phone` | string | no |  | `"12345"` |
| `userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
{
  "id": 10,
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "john@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": 1
}
```

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `username` | string | no |  | `"theUser"` |
| `firstName` | string | no |  | `"John"` |
| `lastName` | string | no |  | `"James"` |
| `email` | string | no |  | `"john@email.com"` |
| `password` | string | no |  | `"12345"` |
| `phone` | string | no |  | `"12345"` |
| `userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
{
  "id": 10,
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "john@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": 1
}
```

**default**: Unexpected error

## POST /user/createWithList

**Creates list of users with given input array.**

- **Operation ID:** `createUsersWithListInput`

### Request body

Optional.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].id` | integer (int64) | no |  | `10` |
| `[].username` | string | no |  | `"theUser"` |
| `[].firstName` | string | no |  | `"John"` |
| `[].lastName` | string | no |  | `"James"` |
| `[].email` | string | no |  | `"john@email.com"` |
| `[].password` | string | no |  | `"12345"` |
| `[].phone` | string | no |  | `"12345"` |
| `[].userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
[
  {
    "id": 10,
    "username": "theUser",
    "firstName": "John",
    "lastName": "James",
    "email": "john@email.com",
    "password": "12345",
    "phone": "12345",
    "userStatus": 1
  }
]
```

### Responses

**200**: Successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `username` | string | no |  | `"theUser"` |
| `firstName` | string | no |  | `"John"` |
| `lastName` | string | no |  | `"James"` |
| `email` | string | no |  | `"john@email.com"` |
| `password` | string | no |  | `"12345"` |
| `phone` | string | no |  | `"12345"` |
| `userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
{
  "id": 10,
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "john@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": 1
}
```

**default**: Unexpected error

## GET /user/login

**Logs user into the system.**

Log into the system.

- **Operation ID:** `loginUser`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `username` | query | string | no | The user name for login. |
| `password` | query | string | no | The password for login in clear text. |

### Responses

**200**: successful operation

| Header | Type | Description |
|---|---|---|
| `X-Rate-Limit` | integer (int32) | calls per hour allowed by the user |
| `X-Expires-After` | string (date-time) | date in UTC when token expires |

Content types: `application/xml`, `application/json`

Type: string.

**400**: Invalid username/password supplied

**default**: Unexpected error

## GET /user/logout

**Logs out current logged in user session.**

Log user out of the system.

- **Operation ID:** `logoutUser`

### Responses

**200**: successful operation

**default**: Unexpected error

## GET /user/{username}

**Get user by user name.**

Get user detail based on username.

- **Operation ID:** `getUserByName`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `username` | path | string | yes | The name that needs to be fetched. Use user1 for testing. |

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `username` | string | no |  | `"theUser"` |
| `firstName` | string | no |  | `"John"` |
| `lastName` | string | no |  | `"James"` |
| `email` | string | no |  | `"john@email.com"` |
| `password` | string | no |  | `"12345"` |
| `phone` | string | no |  | `"12345"` |
| `userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
{
  "id": 10,
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "john@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": 1
}
```

**400**: Invalid username supplied

**404**: User not found

**default**: Unexpected error

## PUT /user/{username}

**Update user resource.**

This can only be done by the logged in user.

- **Operation ID:** `updateUser`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `username` | path | string | yes | name that need to be deleted. |

### Request body

Optional. Update an existent user in the store

Content types: `application/json`, `application/xml`, `application/x-www-form-urlencoded`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `username` | string | no |  | `"theUser"` |
| `firstName` | string | no |  | `"John"` |
| `lastName` | string | no |  | `"James"` |
| `email` | string | no |  | `"john@email.com"` |
| `password` | string | no |  | `"12345"` |
| `phone` | string | no |  | `"12345"` |
| `userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
{
  "id": 10,
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "john@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": 1
}
```

### Responses

**200**: successful operation

**400**: bad request

**404**: user not found

**default**: Unexpected error

## DELETE /user/{username}

**Delete user resource.**

This can only be done by the logged in user.

- **Operation ID:** `deleteUser`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `username` | path | string | yes | The name that needs to be deleted. |

### Responses

**200**: User deleted

**400**: Invalid username supplied

**404**: User not found

**default**: Unexpected error
