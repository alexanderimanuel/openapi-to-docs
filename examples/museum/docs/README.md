# Redocly Museum API

Version `1.2.1` · [Terms of service](https://redocly.com/subscription-agreement/) · Contact: [team@redocly.com](mailto:team@redocly.com) · License: [MIT](https://opensource.org/license/mit/)

Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.

## Servers

| URL | Description |
|---|---|
| `https://redocly.com/_mock/docs/openapi/museum-api` |  |

## Authentication

- **`MuseumPlaceholderAuth`**: HTTP basic.

Unless an endpoint says otherwise, requests need: `MuseumPlaceholderAuth` (HTTP basic).

## Endpoints

### [Operations](operations.md)

Operational information about the museum.

| Method | Path | Summary |
|---|---|---|
| `GET` | [`/museum-hours`](operations.md#get-museum-hours) | Get museum hours |

### [Events](events.md)

Special events hosted by the museum.

| Method | Path | Summary |
|---|---|---|
| `POST` | [`/special-events`](events.md#post-special-events) | Create special events |
| `GET` | [`/special-events`](events.md#get-special-events) | List special events |
| `GET` | [`/special-events/{eventId}`](events.md#get-special-eventseventid) | Get special event |
| `PATCH` | [`/special-events/{eventId}`](events.md#patch-special-eventseventid) | Update special event |
| `DELETE` | [`/special-events/{eventId}`](events.md#delete-special-eventseventid) | Delete special event |

### [Tickets](tickets.md)

Museum tickets for general entrance or special events.

| Method | Path | Summary |
|---|---|---|
| `POST` | [`/tickets`](tickets.md#post-tickets) | Buy museum tickets |
| `GET` | [`/tickets/{ticketId}/qr`](tickets.md#get-ticketsticketidqr) | Get ticket QR code |

## Schemas

[TicketType](schemas.md#tickettype), [Date](schemas.md#date), [Email](schemas.md#email), [BuyMuseumTickets](schemas.md#buymuseumtickets), [TicketMessage](schemas.md#ticketmessage), [TicketId](schemas.md#ticketid), [TicketConfirmation](schemas.md#ticketconfirmation), [Ticket](schemas.md#ticket), [MuseumTicketsConfirmation](schemas.md#museumticketsconfirmation), [TicketCodeImage](schemas.md#ticketcodeimage), [MuseumHours](schemas.md#museumhours), [MuseumDailyHours](schemas.md#museumdailyhours), [EventId](schemas.md#eventid), [EventName](schemas.md#eventname), [EventLocation](schemas.md#eventlocation), [EventDescription](schemas.md#eventdescription), [EventDates](schemas.md#eventdates), [EventPrice](schemas.md#eventprice), [SpecialEventFields](schemas.md#specialeventfields), [SpecialEvent](schemas.md#specialevent), [SpecialEventCollection](schemas.md#specialeventcollection), [Error](schemas.md#error)

---

Generated from `openapi.yaml` with [openapi-to-docs](https://github.com/alexanderimanuel/openapi-to-docs).
