# Events

Part of the [Redocly Museum API](README.md) documentation.

Special events hosted by the museum.

## POST /special-events

**Create special events**

Creates a new special event for the museum.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `createSpecialEvent`

### Request body

**Required.**

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "name": "Mermaid Treasure Identification and Analysis",
  "location": "Under the seaaa 🦀 🎶 🌊.",
  "eventDescription": "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.",
  "dates": [
    "2023-09-05",
    "2023-09-08"
  ],
  "price": 0
}
```

### Responses

**201**: Created.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "eventId": "dad4bce8-f5cb-4078-a211-995864315e39",
  "name": "Mermaid Treasure Identification and Analysis",
  "location": "Under the seaaa 🦀 🎶 🌊.",
  "eventDescription": "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.",
  "dates": [
    "2023-09-05",
    "2023-09-08"
  ],
  "price": 30
}
```

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

## GET /special-events

**List special events**

Return a list of upcoming special events at the museum.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `listSpecialEvents`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `startDate` | query | string (date) | no | Starting date to retrieve future operating hours from. Defaults to today's date. Example: `"2023-02-23"` |
| `endDate` | query | string (date) | no | End of a date range to retrieve special events for. Defaults to 7 days after `startDate`. Example: `"2023-04-18"` |
| `page` | query | integer | no | Page number to retrieve. Default: `1`. Example: `2` |
| `limit` | query | integer | no | Number of days per page. Default: `10`. Maximum: 30. Example: `15` |

### Responses

**200**: Success.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `[].name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `[].location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `[].eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `[].dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `[].price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
[
  {
    "eventId": "f3e0e76e-e4a8-466e-ab9c-ae36c15b8e97",
    "name": "Sasquatch Ballet",
    "location": "Seattle... probably",
    "eventDescription": "They're big, they're hairy, but they're also graceful. Come learn how the biggest feet can have the lightest touch.",
    "dates": [
      "2023-12-15",
      "2023-12-22"
    ],
    "price": 40
  },
  {
    "eventId": "2f14374a-9c65-4ee5-94b7-fba66d893483",
    "name": "Solar Telescope Demonstration",
    "location": "Far from the sun.",
    "eventDescription": "Look at the sun without going blind!",
    "dates": [
      "2023-09-07",
      "2023-09-14"
    ],
    "price": 50
  },
  {
    "eventId": "6aaa61ba-b2aa-4868-b803-603dbbf7bfdb",
    "name": "Cook like a Caveman",
    "location": "Fire Pit on East side",
    "eventDescription": "Learn to cook on an open flame.",
    "dates": [
      "2023-11-10",
      "2023-11-17",
      "2023-11-24"
    ],
    "price": 5
  },
  {
    "eventId": "602b75e1-5696-4ab8-8c7a-f9e13580f910",
    "name": "Underwater Basket Weaving",
    "location": "Rec Center Pool next door.",
    "eventDescription": "Learn to weave baskets underwater.",
    "dates": [
      "2023-09-12",
      "2023-09-15"
    ],
    "price": 15
  },
  {
    "eventId": "dad4bce8-f5cb-4078-a211-995864315e39",
    "name": "Mermaid Treasure Identification and Analysis",
    "location": "Room Sea-12",
    "eventDescription": "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits — kindly donated by Ariel.",
    "dates": [
      "2023-09-05",
      "2023-09-08"
    ],
    "price": 30
  },
  {
    "eventId": "6744a0da-4121-49cd-8479-f8cc20526495",
    "name": "Time Traveler Tea Party",
    "location": "Temporal Tearoom",
    "eventDescription": "Sip tea with important historical figures.",
    "dates": [
      "2023-11-18",
      "2023-11-25",
      "2023-12-02"
    ],
    "price": 60
  },
  {
    "eventId": "3be6453c-03eb-4357-ae5a-984a0e574a54",
    "name": "Pirate Coding Workshop",
    "location": "Computer Room",
    "eventDescription": "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
    "dates": [
      "2023-10-29",
      "2023-10-30",
      "2023-10-31"
    ],
    "price": 45
  },
  {
    "eventId": "9d90d29a-2af5-4206-97d9-9ea9ceadcb78",
    "name": "Llama Street Art Through the Ages",
    "location": "Auditorium",
    "eventDescription": "Llama street art?! Alpaca my bags -- let's go!",
    "dates": [
      "2023-10-29",
      "2023-10-30",
      "2023-10-31"
    ],
    "price": 45
  },
  {
    "eventId": "a3c7b2c4-b5fb-4ef7-9322-00a919864957",
    "name": "The Great Parrot Debate",
    "location": "Outdoor Amphitheatre",
    "eventDescription": "See leading parrot minds discuss important geopolitical issues.",
    "dates": [
      "2023-11-03",
      "2023-11-10"
    ],
    "price": 35
  },
  {
    "eventId": "b92d46b7-4c5d-422b-87a5-287767e26f29",
    "name": "Eat a Bunch of Corn",
    "location": "Cafeteria",
    "eventDescription": "We accidentally bought too much corn. Please come eat it.",
    "dates": [
      "2023-11-10",
      "2023-11-17",
      "2023-11-24"
    ],
    "price": 5
  }
]
```

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

## GET /special-events/{eventId}

**Get special event**

Get details about a special event.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `getSpecialEvent`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `eventId` | path | string (uuid) | yes | Identifier for a special event. Example: `"dad4bce8-f5cb-4078-a211-995864315e39"` |

### Responses

**200**: Success.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "eventId": "6744a0da-4121-49cd-8479-f8cc20526495",
  "name": "Time Traveler Tea Party",
  "location": "Temporal Tearoom",
  "eventDescription": "Sip tea with important historical figures.",
  "dates": [
    "2023-11-18",
    "2023-11-25",
    "2023-12-02"
  ],
  "price": 60
}
```

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

## PATCH /special-events/{eventId}

**Update special event**

Update the details of a special event.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `updateSpecialEvent`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `eventId` | path | string (uuid) | yes | Identifier for a special event. Example: `"dad4bce8-f5cb-4078-a211-995864315e39"` |

### Request body

**Required.**

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `name` | string | no | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | no | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | no | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | no | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | no | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "location": "On the beach.",
  "price": 15
}
```

### Responses

**200**: Success.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "eventId": "dad4bce8-f5cb-4078-a211-995864315e39",
  "name": "Mermaid Treasure Identification and Analysis",
  "location": "On the beach.",
  "eventDescription": "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.",
  "dates": [
    "2023-09-05",
    "2023-09-08"
  ],
  "price": 15
}
```

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

## DELETE /special-events/{eventId}

**Delete special event**

Delete a special event from the collection. Allows museum to cancel planned events.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `deleteSpecialEvent`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `eventId` | path | string (uuid) | yes | Identifier for a special event. Example: `"dad4bce8-f5cb-4078-a211-995864315e39"` |

### Responses

**204**: Success - no content.

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**401**: Unauthorized.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```
