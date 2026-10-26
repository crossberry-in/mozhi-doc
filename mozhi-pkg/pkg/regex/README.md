# regex

Regular expression helpers for Mozhi. Uses grep/sed under the hood.

## Usage
```mozhi
import mod from "regex"
echo(mod.is_email("user@example.com"))
echo(mod.replace_all("hello world", " ", "_"))
```
