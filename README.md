# Hello world docker action
aa
asd
das
eThis action prints "Hello World 2" or "Hello" + the name of a person to greet to the log.
das
## Inputs

### `who-to-greet`

**Required** The name of the person to greet. Default `"World"`.

## Outputs

### `time`

The time we greeted you.

## Example usage

uses: naturalett/playgroundactions@v1
with:
  who-to-greet: 'Mona the Octocat'
