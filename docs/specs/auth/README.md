# Module: `auth` — Authentication

Module auth handle đăng nhập, đăng ký, password reset, session management cho hệ thống IMS.

## Features

| Feature ID | Name | Status | Owner | Sprint |
|---|---|---|---|---|
| [IMS_AUTH_01](IMS_AUTH_01_login/spec.md) | User Login | 🟡 DRAFT | @cuongbx | — |

## Dependencies

- Upstream: IMS_USER_01 (user management — required for login)
- Downstream: Mọi feature cần auth guard

## Conventions

- JWT RS256 asymmetric signing
- bcrypt 12 rounds cho password hash
- Lockout policy: 5 attempts / 15 min
- Rate limit: 10 req/phút/IP

## Contacts

- BA Lead: @cuongbx
- Tech Lead: (TBD)
- Security reviewer: (TBD)
