# Swagger Petstore - OpenAPI 3.0

Version `1.0.27` · [Terms of service](https://swagger.io/terms/) · Contact: [apiteam@swagger.io](mailto:apiteam@swagger.io) · License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.html)

This is a sample Pet Store Server based on the OpenAPI 3.0 specification.  You can find out more about
Swagger at [https://swagger.io](https://swagger.io). In the third iteration of the pet store, we've switched to the design first approach!
You can now help us improve the API whether it's by making changes to the definition itself or to the code.
That way, with time, we can improve the API in general, and expose some of the new features in OAS3.

Some useful links:
- [The Pet Store repository](https://github.com/swagger-api/swagger-petstore)
- [The source API definition for the Pet Store](https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml)

More information: [Find out more about Swagger](https://swagger.io)

## Servers

| URL | Description |
|---|---|
| `/api/v3` |  |

## Authentication

- **`petstore_auth`**: OAuth 2.0, implicit flow.
  - Implicit flow: authorize at https://petstore3.swagger.io/oauth/authorize
  - Scopes: `write:pets` (modify pets in your account), `read:pets` (read your pets)
- **`api_key`**: API key in header `api_key`.

Each endpoint lists the scheme it accepts under **Auth**.

## Endpoints

### [pet](pet.md)

Everything about your Pets

| Method | Path | Summary |
|---|---|---|
| `PUT` | [`/pet`](pet.md#put-pet) | Update an existing pet. |
| `POST` | [`/pet`](pet.md#post-pet) | Add a new pet to the store. |
| `GET` | [`/pet/findByStatus`](pet.md#get-petfindbystatus) | Finds Pets by status. |
| `GET` | [`/pet/findByTags`](pet.md#get-petfindbytags) | Finds Pets by tags. |
| `GET` | [`/pet/{petId}`](pet.md#get-petpetid) | Find pet by ID. |
| `POST` | [`/pet/{petId}`](pet.md#post-petpetid) | Updates a pet in the store with form data. |
| `DELETE` | [`/pet/{petId}`](pet.md#delete-petpetid) | Deletes a pet. |
| `POST` | [`/pet/{petId}/uploadImage`](pet.md#post-petpetiduploadimage) | Uploads an image. |

### [store](store.md)

Access to Petstore orders

| Method | Path | Summary |
|---|---|---|
| `GET` | [`/store/inventory`](store.md#get-storeinventory) | Returns pet inventories by status. |
| `POST` | [`/store/order`](store.md#post-storeorder) | Place an order for a pet. |
| `GET` | [`/store/order/{orderId}`](store.md#get-storeorderorderid) | Find purchase order by ID. |
| `DELETE` | [`/store/order/{orderId}`](store.md#delete-storeorderorderid) | Delete purchase order by identifier. |

### [user](user.md)

Operations about user

| Method | Path | Summary |
|---|---|---|
| `POST` | [`/user`](user.md#post-user) | Create user. |
| `POST` | [`/user/createWithList`](user.md#post-usercreatewithlist) | Creates list of users with given input array. |
| `GET` | [`/user/login`](user.md#get-userlogin) | Logs user into the system. |
| `GET` | [`/user/logout`](user.md#get-userlogout) | Logs out current logged in user session. |
| `GET` | [`/user/{username}`](user.md#get-userusername) | Get user by user name. |
| `PUT` | [`/user/{username}`](user.md#put-userusername) | Update user resource. |
| `DELETE` | [`/user/{username}`](user.md#delete-userusername) | Delete user resource. |

## Schemas

[Order](schemas.md#order), [Category](schemas.md#category), [User](schemas.md#user), [Tag](schemas.md#tag), [Pet](schemas.md#pet), [ApiResponse](schemas.md#apiresponse)

---

Generated from `openapi.json` with [openapi-to-docs](https://github.com/alexanderimanuel/openapi-to-docs).
