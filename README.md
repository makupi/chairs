## Chairs

CLI tool to compute the number of chairs per room from an ascii floor plan


### Installation
```
pipx install git+https://github.com/makupi/chairs.git
```

### Usage


```
chairs --plan plan.txt
```

> `--plan` defaults to `plan.txt` and can be omitted


### Assumed Restrictions

A plan may only use `+-` for horizontal lines and `+|\/` for vertical lines.
Room names must be written in parenthesis and lowercase like `(kitchen)`.