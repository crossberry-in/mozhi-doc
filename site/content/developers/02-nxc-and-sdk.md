---
title: nxc installer and the NxDB SDK
description: Install the nxc CLI, search and install packages from the registry, and connect to NxDB with the nxmirror-db SDK.
---

# nxc installer and the NxDB SDK

## Install nxc

`nxc` is the NxMirror command-line tool. It talks to the public package
registry and the NxDB platform.

```sh
curl -fsSL https://nxmirror.netlify.app/install.sh | sh
```

The installer verifies the script with a Python syntax check, installs it
as `nxc` (default `~/.local/bin`) and prints the `PATH` hint.

First-time setup:

```sh
nxc register        # create an account (only needed to publish)
nxc login           # sign in (only needed to publish)
```

Searching and installing are public — no account required.

## Search the nxc package library

```sh
nxc pkg search http          # search packages (alias: nxc pkg find)
nxc pkg search --kind package --sort downloads
nxc info owner/name          # details for one package
```

## Install any package

```sh
nxc pkg install owner/name              # latest version
nxc pkg install owner/name@1.2.0        # pinned version
nxc pkg install owner/name -d vendor    # custom destination (default nx_modules)
```

Installed packages land in the destination folder and are ready to use
from your code.

## The nxmirror-db SDK (NxDB)

NxDB is the cloud SQL database + hybrid file storage behind the NxMirror
platform. Every database is a real, isolated SQLite engine behind the
API gateway — genuine SQL with prepared statements, transactions, JOINs
and DDL.

```sh
npm install nxmirror-db
```

Server-side connect (Node.js, CI — full access):

```js
import NxDB from "nxmirror-db";

const db = await NxDB.connect({
  databaseId: process.env.NXDB_ID,       // nxdb-...
  password:   process.env.NXDB_PASSWORD  // keep secrets in the environment!
});

const result = await db.query("SELECT * FROM users WHERE active = ?", [true]);
console.log(result.rows);
```

Key rules:

- **Never hardcode credentials.** Read them from environment variables.
- **Browsers** use an application token (origin-restricted) instead of
  the password.
- **Servers / CI** can use a scoped token from the API Tokens tab as an
  alternative to the password.

CommonJS works too: `const NxDB = require("nxmirror-db");` (the SDK
ships both ESM and CJS builds).

Useful entry points:

```js
await db.exec("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)");
await db.table("notes").insert({ body: "hello" });
const info = await db.connectInfo();
```

API base: `https://nxmirror.netlify.app/api` — platform docs live at
`https://nxmirror.netlify.app/docs`. The SDK has zero dependencies and
works in Node.js 18+ and modern browsers.

## mz ↔ nxc in one paragraph

`mz` runs your Mozhi code; `nxc` publishes and installs packages. A
typical loop: build and check your package with `mz pkg` (next page),
publish it with `nxc pkg push`, and your users install it with
`nxc pkg install owner/name`. See the next page for the full deploy
walkthrough.
