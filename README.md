# shopping-list-bot

This is the source code for the Telegram Shopping List manager tutorial.

# What this application does?

The `shopping-list-bot` is a [Telegram bot](https://core.telegram.org/bots) that manages your shopping list.
It means that to use this application, you must have a Telegram acccount open and use Telegram.

**How do you interact with the bot?**

The bot accepts the following _commands_ as an input in the CLI style:

| Command | Flags | Comment | 
| --- | --- | --- |
| `/add` | `--item [string; an item's name] --unit [string; units, such as kg, gr, unit] --amount [int; the amount of an item in units]` | Add an item to the shopping list. If there's not shopping list, one is created for you. |
| `/update` | `--item [string; an item's name] --amount [int; the amount by which to update an existing item]` | Updates an existing item. The amount can be both negative or positive |
| `/remove` | `--item [string; an item's name]` | Remove an item from the shopping list |
| `/clear` | | Resets the shopping list. |

## Directory Structure

All the source code goes into the `lambdas` directory. There's it's divided into two subsections:
- `src`: the source code for Lambda handlers. Each directory represents a lambda, which is named the same.
- `layers`: the source code for Lambda layers (should we need them). Shared layers between lambdas.

# Build and deployment

We'll use the [uv]() tool to manage our dependencies. Eac

## Logging

We'll use the Powertools 